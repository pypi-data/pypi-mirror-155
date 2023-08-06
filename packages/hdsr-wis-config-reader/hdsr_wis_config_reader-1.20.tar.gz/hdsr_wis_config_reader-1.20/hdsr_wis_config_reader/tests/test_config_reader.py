from hdsr_pygithub import GithubDirDownloader
from hdsr_wis_config_reader import constants
from hdsr_wis_config_reader.readers.config_reader import FewsConfigReader
from hdsr_wis_config_reader.tests.fixtures import fews_config_local
from hdsr_wis_config_reader.tests.helpers import _remove_dir_recursively
from pathlib import Path

import datetime
import logging
import pandas as pd  # noqa


# silence flake8
fews_config_local = fews_config_local

logger = logging.getLogger(__name__)


expected_parameters = [
    "A",
    "A.15",
    "AREA",
    "B.d",
    "B.m",
    "B.y",
    "BG.A",
    "BG.V.tot",
    "BG.b.0",
    "BG.fd.0",
    "BG.ka.0",
    "BG.o.0",
    "BG.tot.0",
    "BGf.tot",
    "BegFD.a",
    "BegFD.s",
    "BegKl",
    "BegKrA.a",
    "BegKrA.s",
    "BegOnd.a",
    "BegOnd.s",
    "BegOpv.a",
    "BegOpv.s",
    "BegOvs.a",
    "BegTot.a",
    "BegTot.s",
    "C.0",
    "C.15",
    "C2.0",
    "CF",
    "CTS_M_GMT+01:00",
    "CTS_Y_GMT+01:00",
    "DD.15",
    "DD.AA.m",
    "DD.AD.m",
    "DD.AM.m",
    "DD.AR.m",
    "DD.AU.m",
    "DD.d",
    "DD.h",
    "DD.m",
    "DDH.15",
    "DDH.d",
    "DDH.h",
    "DDH.m",
    "DDHM.d",
    "DDL.15",
    "DDL.d",
    "DDL.h",
    "DDL.m",
    "DDLM.d",
    "DDM.d",
    "DDU.d",
    "DIFF",
    "DMaai.0",
    "DRAAIDUUR_DAY1",
    "DRAAIDUUR_DAY2",
    "DRAAIDUUR_DAY3",
    "DRAAIDUUR_DAY4",
    "DRAAIDUUR_UUR_CUM",
    "DRAAIDUUR_UUR_NONCUM",
    "DZm.0",
    "DaysOld.d",
    "DaysOld.m",
    "DaysOld.w",
    "DaysOld.y",
    "DbAug1.a",
    "ES.0",
    "ES.15",
    "ES2.0",
    "ES2.15",
    "EV.15",
    "EV.m",
    "Eact.d",
    "Eact.m",
    "Eact.y",
    "Edef.C.d",
    "Edef.d",
    "Edef.m",
    "Edef.y",
    "EowF",
    "Epot.d",
    "Epot.m",
    "Epot.y",
    "Eref.d",
    "Eref.m",
    "Eref.y",
    "F.0",
    "F.15",
    "F.AA.m",
    "F.AD.m",
    "F.AM.m",
    "F.AR.m",
    "F.AU.m",
    "F.d",
    "F.h",
    "F.m",
    "FRC",
    "G.dino",
    "GFG",
]

expected_df_parameter_column_names = [
    "DESCRIPTION",
    "GROUP",
    "ID",
    "NAME",
    "PARAMETERTYPE",
    "SHORTNAME",
    "UNIT",
    "USESDATUM",
    "VALUERESOLUTION",
]


def test_local_fews_config(fews_config_local):
    # test FewsConfigReader
    fews_config = fews_config_local
    fews_config.MapLayerFiles  # noqa
    fews_config.RegionConfigFiles  # noqa
    fews_config.IdMapFiles  # noqa
    loc_sets = fews_config.location_sets
    for loc_set in loc_sets:
        try:
            fews_config.get_locations(location_set_key=loc_set)
        except Exception as err:
            logger.error(f"got error in get_locations() for loc_set {loc_set}, err={err}")

    # test FewsConfigReader parameters (special case that works different for old configs and new configs)
    df_parameters = fews_config_local.get_parameters()
    assert isinstance(df_parameters, pd.DataFrame)
    assert len(df_parameters) > 100
    assert sorted(df_parameters.columns) == expected_df_parameter_column_names


def test_github_fews_config_prd():

    target_dir = Path("FEWS/Config")
    github_downloader = GithubDirDownloader(
        target_dir=target_dir,
        only_these_extensions=[".csv", ".xml"],
        allowed_period_no_updates=datetime.timedelta(weeks=52 * 2),
        repo_name=constants.GITHUB_WIS_CONFIG_REPO_NAME,
        branch_name=constants.GITHUB_WIS_CONFIG_BRANCH_NAME,
        repo_organisation=constants.GITHUB_ORGANISATION_NAME,
    )
    download_dir = github_downloader.download_files(use_tmp_dir=True)
    config_dir = download_dir / target_dir
    fews_config = FewsConfigReader(path=config_dir)
    assert fews_config.path == config_dir

    # test FewsConfigReader
    fews_config.MapLayerFiles  # noqa
    fews_config.RegionConfigFiles  # noqa
    fews_config.IdMapFiles  # noqa
    loc_sets = fews_config.location_sets
    for loc_set in loc_sets:
        try:
            fews_config.get_locations(location_set_key=loc_set)
        except Exception as err:
            logger.error(f"got error in get_locations() for loc_set {loc_set}, err={err}")

    # test FewsConfigReader parameters (special case that works different for old configs and new configs)
    df_parameters = fews_config.get_parameters()
    assert sorted(df_parameters.columns) == expected_df_parameter_column_names
    assert len(df_parameters) > 100
    assert sorted(df_parameters.columns) == expected_df_parameter_column_names

    # clean up
    _remove_dir_recursively(dir_path=download_dir)
