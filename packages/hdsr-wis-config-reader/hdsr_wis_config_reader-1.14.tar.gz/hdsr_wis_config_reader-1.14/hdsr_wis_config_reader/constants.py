from datetime import timedelta
from pathlib import Path


# Handy constant for building relative paths
BASE_DIR = Path(__file__).parent
TEST_INPUT_DIR = BASE_DIR / "tests" / "data" / "input"

if BASE_DIR.name != "hdsr_wis_config_reader":
    raise AssertionError(f"BASE_DIR {BASE_DIR.name} must be project name 'hdsr_wis_config_reader'")

TEST_DIR_WIS_CONFIG = TEST_INPUT_DIR / "config_wis60prd_202002"
TEST_PATH_STARTENDDATE_CAW_OPP_SHORT = TEST_INPUT_DIR / "startenddate" / "caw_oppervlaktewater_short.csv"

# Github wis mpt config repo (only for testing)
GITHUB_ORGANISATION_NAME = "hdsr-mid"
GITHUB_WIS_CONFIG_REPO_NAME = "FEWS-WIS_HKV"
GITHUB_WIS_CONFIG_BRANCH_NAME = "202002-prd"

# Github startendate repo
GITHUB_STARTENDDATE_REPO_NAME = "startenddate"
GITHUB_STARTENDDATE_BRANCH_NAME = "main"
GITHUB_STARTENDDATE_ALLOWED_PERIOD_NO_UPDATES = timedelta(weeks=52 / 4)
GITHUB_STARTENDDATE_CAW_OPPERVLAKTEWATER_SHORT = Path("data/output/results/caw_oppervlaktewater_short.csv")
GITHUB_STARTENDDATE_CAW_OPPERVLAKTEWATER_LONG = Path("data/output/results/caw_oppervlaktewater_long.csv")
GITHUB_STARTENDDATE_CAW_OPPERVLAKTEWATER_HYMOS_SHORT = Path("data/output/results/caw_oppervlaktewater_hymos_short.csv")
