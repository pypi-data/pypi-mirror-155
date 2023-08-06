from datetime import timedelta
from hdsr_pygithub.exceptions import GithubFileTooOldError
from hdsr_wis_config_reader import IdMappingCollection
from hdsr_wis_config_reader.startenddate import merge_startenddate_github_with_idmap
from hdsr_wis_config_reader.startenddate import merge_startenddate_idmap
from hdsr_wis_config_reader.startenddate import StartEndDateReaderGithub
from hdsr_wis_config_reader.tests.fixtures import fews_config_local
from hdsr_wis_config_reader.tests.fixtures import startenddate_local
from pathlib import Path

import pandas as pd  # noqa
import pytest


# silence flake8
fews_config_local = fews_config_local
startenddate_local = startenddate_local


def test_merge_local_startenddate_local_idmapping(fews_config_local, startenddate_local):
    id_mappings = IdMappingCollection(fews_config=fews_config_local)
    df_startenddate = startenddate_local.df_startenddate
    df = merge_startenddate_idmap(df_idmap=id_mappings.idmap_opvl_water, df_startenddate=df_startenddate)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 6287


def test_merge_github_startenddate_local_idmapping(fews_config_local):
    id_mappings = IdMappingCollection(fews_config=fews_config_local)

    target_file = Path("data/output/results/caw_oppervlaktewater_short.csv")
    startenddate_github = StartEndDateReaderGithub(target_file=target_file)
    df_startenddate = startenddate_github.df_startenddate

    df = merge_startenddate_idmap(df_idmap=id_mappings.idmap_opvl_water, df_startenddate=df_startenddate)
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 6287


def test_github_startenddate_too_old():
    target_file = Path("data/output/results/caw_oppervlaktewater_short.csv")
    startenddate_github = StartEndDateReaderGithub(target_file=target_file, allowed_period_no_updates=timedelta(days=1))
    with pytest.raises(GithubFileTooOldError):
        df = startenddate_github.df_startenddate  # noqa


def test_xx(fews_config_local):
    id_map_collection = IdMappingCollection(fews_config=fews_config_local)
    df = merge_startenddate_github_with_idmap(df_idmap=id_map_collection.idmap_all)
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 8215
