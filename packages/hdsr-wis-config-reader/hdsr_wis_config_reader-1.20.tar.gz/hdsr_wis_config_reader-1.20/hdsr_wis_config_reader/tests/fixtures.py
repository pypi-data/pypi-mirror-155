from hdsr_wis_config_reader import constants
from hdsr_wis_config_reader.location_sets.collection import LocationSetCollection
from hdsr_wis_config_reader.readers.config_reader import FewsConfigReader
from hdsr_wis_config_reader.startenddate import StartEndDateReaderLocal

import pytest


@pytest.fixture(scope="session")  # 'session', so we cache the fixture for all tests (instead of default 'function')
def fews_config_local() -> FewsConfigReader:
    # we use config saved in this repo (=static), instead of downloading from repo 'wis_config'
    assert constants.TEST_DIR_WIS_CONFIG.is_dir()
    fews_config = FewsConfigReader(path=constants.TEST_DIR_WIS_CONFIG)
    return fews_config


@pytest.fixture(scope="session")  # 'session', so we cache the fixture for all tests (instead of default 'function')
def loc_sets() -> LocationSetCollection:
    fews_config = FewsConfigReader(path=constants.TEST_DIR_WIS_CONFIG)
    loc_sets = LocationSetCollection(fews_config=fews_config)
    return loc_sets


@pytest.fixture(scope="session")  # 'session', so we cache the fixture for all tests (instead of default 'function')
def startenddate_local() -> StartEndDateReaderLocal:
    return StartEndDateReaderLocal(startenddate_csv_path=constants.TEST_PATH_STARTENDDATE_CAW_OPP_SHORT)
