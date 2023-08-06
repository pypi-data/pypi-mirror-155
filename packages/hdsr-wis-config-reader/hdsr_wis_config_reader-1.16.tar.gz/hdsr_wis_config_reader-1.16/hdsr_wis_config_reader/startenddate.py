from abc import ABC
from datetime import timedelta
from hdsr_pygithub import GithubFileDownloader
from hdsr_wis_config_reader import constants
from hdsr_wis_config_reader.idmappings.columns import ExLocChoices
from hdsr_wis_config_reader.idmappings.columns import IdMapCols
from hdsr_wis_config_reader.idmappings.columns import StartEndDateCols
from hdsr_wis_config_reader.idmappings.custom_dataframe import IdMappingDataframe
from hdsr_wis_config_reader.idmappings.files import IdMapChoices
from hdsr_wis_config_reader.utils import PdReadFlexibleCsv
from pathlib import Path

import logging
import numpy as np


logger = logging.getLogger(__name__)


import pandas as pd  # noqa pandas comes with geopandas


class StartEndDateReaderBase(ABC):
    def __init__(self):
        self._df_startenddate = None

    @staticmethod
    def _validate_input_df_startenddate(df: pd.DataFrame) -> pd.DataFrame:
        # check minimal columns exist
        for expected_column in StartEndDateCols.get_all():
            assert expected_column in df.columns, f"expected_column {expected_column} is not in df_startenddate"

        # check dtype date_type_columns
        date_type_columns = [
            StartEndDateCols.start,
            StartEndDateCols.end,
        ]
        for date_type_column in date_type_columns:
            if not pd.api.types.is_datetime64_dtype(arr_or_dtype=df[date_type_column]):
                msg = f"'pd.read_csv(parse_dates=...)' will not work for column {date_type_column}."
                try:
                    pd.to_datetime(df[date_type_column])
                    msg += " However, pd.to_datetime() succeeds?!"
                except Exception as err:
                    msg += f": pd.to_datetime() does not succeed, err={err}."
                msg += (
                    f"date_type_column {date_type_column} in startenddate dataframe "
                    f"can not be converted to np.datetime64. Check if values are dates."
                )
                raise AssertionError(msg)

        # strip string columns
        df_obj = df.select_dtypes(["object"])
        df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

        # remove '#' from column series ('#001_FQ1' to '001_FQ1')
        df[StartEndDateCols.series] = df[StartEndDateCols.series].str.replace("#", "")

        assert sorted(df.columns) == sorted(StartEndDateCols.get_all())
        return df

    @property
    def df_startenddate(self) -> pd.DataFrame:
        raise NotImplementedError


class StartEndDateReaderLocal(StartEndDateReaderBase):
    def __init__(self, startenddate_csv_path: Path):
        self.startenddate_csv_path = startenddate_csv_path
        super().__init__()

    @property
    def df_startenddate(self) -> pd.DataFrame:
        if self._df_startenddate is not None:
            return self._df_startenddate
        # set startenddate to test .csv instead of downloading latest github file
        date_type_columns = [
            StartEndDateCols.start,
            StartEndDateCols.end,
        ]
        df = PdReadFlexibleCsv(path=self.startenddate_csv_path, sep=",", parse_dates=date_type_columns).df
        self._df_startenddate = self._validate_input_df_startenddate(df=df)
        return self._df_startenddate


class StartEndDateReaderGithub(StartEndDateReaderBase):
    def __init__(
        self,
        target_file: Path,
        branch_name: str = constants.GITHUB_STARTENDDATE_BRANCH_NAME,
        allowed_period_no_updates: timedelta = constants.GITHUB_STARTENDDATE_ALLOWED_PERIOD_NO_UPDATES,
    ):
        self.allowed_period_no_updates = allowed_period_no_updates
        self.target_file = target_file
        self.branch_name = branch_name
        super().__init__()

    @property
    def df_startenddate(self) -> pd.DataFrame:
        """Get startenddate file from github for caw oppervlakte_short"""
        if self._df_startenddate is not None:
            return self._df_startenddate

        github_downloader = GithubFileDownloader(
            allowed_period_no_updates=self.allowed_period_no_updates,
            target_file=self.target_file,
            branch_name=self.branch_name,
            repo_name=constants.GITHUB_STARTENDDATE_REPO_NAME,
            repo_organisation=constants.GITHUB_ORGANISATION_NAME,
        )

        # NOTE1: caw startenddate long is the new_name for old_name = caw get_series
        # NOTE2: caw startenddate short is the new_name for old_name = caw get_histtags
        logger.info(f"reading github file {github_downloader.downloadable_content.name}")
        date_type_columns = [
            StartEndDateCols.start,
            StartEndDateCols.end,
        ]
        reader = PdReadFlexibleCsv(path=github_downloader.get_download_url(), sep=",", parse_dates=date_type_columns,)
        df = reader.df
        self._df_startenddate = self._validate_input_df_startenddate(df=df)
        return self._df_startenddate


def merge_startenddate_idmap(df_idmap: IdMappingDataframe, df_startenddate: pd.DataFrame,) -> pd.DataFrame:
    """Add 5 idmap columns ('ex_loc', 'ex_par', 'int_loc', 'int_par', ídmap_source') to df_startenddate."""
    logger.info("merging startendate csv with idmapping xml")

    # check args
    assert sorted(df_startenddate.columns) == sorted(StartEndDateCols.get_all())
    assert isinstance(df_idmap, IdMappingDataframe)
    idmap_source = "idmap_source"
    # from '8808_IB1' to '8808' and 'IB1'
    df_startenddate[[IdMapCols.ex_loc, IdMapCols.ex_par]] = df_startenddate[StartEndDateCols.series].str.split(
        pat="_", n=1, expand=True
    )
    int_loc_collector = []
    int_par_collector = []
    idmap_source_collector = []

    # Create a list of dictionaries in which each dictionary corresponds to an input data row
    for _, row in df_startenddate.iterrows():
        filter_df = df_idmap.get_filtered_df(ex_loc=row[IdMapCols.ex_loc], ex_par=row[IdMapCols.ex_par],)
        if filter_df.empty:
            int_loc_collector.append([""])
            idmap_source_collector.append("")
            int_par_collector.append("")
            continue
        idmap_intlocs = filter_df[IdMapCols.int_loc].to_list()
        nr_int_locs = len(idmap_intlocs)
        if nr_int_locs > 1:
            # raise an error, except for 2 cornercases:
            # 1) stuurpeil
            #    the combo {ex_par, ex_loc} should be unique, except for 'stuurpeil': soms wordt een
            #    stuurpeil aan meerdere interne (verschillende) locaties wordt gekoppeld. Bijv 1
            #    stuurpeil voor 2 pompen, of 2 stuwen, of 2 schuiven
            # 2) opgesplitste locatie
            # TODO: verfiy with Roger:
            #  zijn er 1 of twee uitzonderingen op "the combo {ex_par, ex_loc} should be unique" ?
            #  1) stuurpeil (hierboven)
            #  2) opgesplitste locaties dan? zoals:
            # noqa <map externalLocation="2805" externalParameter="HS2" internalLocation="KW219120" internalParameter="H.S.0"/>
            # noqa <map externalLocation="2805" externalParameter="HS2" internalLocation="KW219130" internalParameter="H.S.0"/>
            # noqa als opgesplitste locatie ook uitzondering is, kunnen we deze verder specificeren (bijv alleen met streefpeil)
            is_stuurpeil_loc = row[IdMapCols.ex_par].startswith("HR")
            is_split_loc = ExLocChoices.is_split(ex_loc=row[IdMapCols.ex_loc])
            is_unique_int_loc = len(set(idmap_intlocs)) == 1
            is_only_in_hymos_and_idopvl_water = sorted(set(filter_df["source"])) == sorted(
                [IdMapChoices.idmap_opvl_water.value, IdMapChoices.idmap_opvl_water_hymos.value]
            )
            exceptions = (
                is_stuurpeil_loc,
                is_split_loc,
                is_unique_int_loc,
                is_only_in_hymos_and_idopvl_water,
            )
            if not any(exceptions):
                raise AssertionError(
                    f"cannot continue, fix this first as multi int_locs are not allowed: found {nr_int_locs} int_locs"
                    f" {idmap_intlocs} in idmap with (ex_loc={row[IdMapCols.ex_loc]}, ex_par={row[IdMapCols.ex_par]})"
                )

        # example after 4 iterations:
        # int_loc_collector =  [[''], [''], ['KW100111', 'KW100111'], ['OW100102', 'OW100102']]
        # idmap_source_collector = ['', '', 'IdOPVLWATER', 'IdOPVLWATER_HYMOS', 'IdOPVLWATER', 'IdOPVLWATER_HYMOS']
        int_loc_collector.append(idmap_intlocs)
        [int_par_collector.append(x) for x in filter_df[IdMapCols.int_par].to_list()]
        [idmap_source_collector.append(x) for x in filter_df["source"].to_list()]

    assert len(df_startenddate) == len(int_loc_collector) != len(idmap_source_collector) == len(int_par_collector)
    df_startenddate[IdMapCols.int_loc] = int_loc_collector
    # Example explode nested columns to rows
    # df = pd.DataFrame({'A': [1, 2, 3, 4],'B': [[1, 2], [1, 2], [], np.nan]})
    #           A       B
    #        0  1  [1, 2]
    #        1  3      []
    #        2  4     NaN
    # df = df.explode('B')
    #           A       B
    #        0  1       1
    #        0  1       2
    #        1  3     NaN
    #        2  4     NaN
    df_startenddate_exploded = df_startenddate.explode(column=IdMapCols.int_loc).reset_index(drop=True)
    assert (
        len(int_loc_collector) != len(df_startenddate_exploded) == len(idmap_source_collector) == len(int_par_collector)
    )
    df_startenddate_exploded[idmap_source] = idmap_source_collector
    df_startenddate_exploded[IdMapCols.int_par] = int_par_collector
    df_startenddate_exploded.drop_duplicates(keep="first", inplace=True)
    df_startenddate_exploded.reset_index(drop=True, inplace=False)
    # replace space/empty strings with NaN
    df_startenddate_exploded.replace(to_replace=r"^\s*$", value=np.nan, regex=True, inplace=True)
    df = df_startenddate_exploded[StartEndDateCols.get_all() + IdMapCols.get_all() + [idmap_source]]
    return df


def merge_startenddate_github_with_idmap(df_idmap: IdMappingDataframe) -> pd.DataFrame:
    startenddate_github_reader = StartEndDateReaderGithub(
        target_file=constants.GITHUB_STARTENDDATE_CAW_OPPERVLAKTEWATER_SHORT
    )
    df_startenddate = startenddate_github_reader.df_startenddate
    df = merge_startenddate_idmap(df_idmap=df_idmap, df_startenddate=df_startenddate)
    return df
