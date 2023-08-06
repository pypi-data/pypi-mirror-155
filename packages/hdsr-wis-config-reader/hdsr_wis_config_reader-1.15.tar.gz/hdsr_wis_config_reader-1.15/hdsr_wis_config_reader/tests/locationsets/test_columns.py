from hdsr_wis_config_reader.location_sets.columns import LocSetSharedCols
from hdsr_wis_config_reader.tests.fixtures import loc_sets


# silence flake8
loc_sets = loc_sets


def test_loc_set_columns(loc_sets):
    expected_hoofd_cols = [
        "ALLE_TYPES",
        "FOTO_ID",
        "GAFCODE",
        "GPGIDENT",
        "KOMPAS",
        "LOC_NAME",
        "RAYON",
        "RBGID",
        "SYSTEEM",
        "X",
        "Y",
        "Z",
        "end",
        "geometry",
        "internalLocation",
        "schema",
        "start",
    ]
    for col_name in expected_hoofd_cols:
        if LocSetSharedCols.must_exist(col_name=col_name):
            assert col_name in loc_sets.hoofd_loc.geo_df.columns

    # test must_exists cols (in all location sets)
    for loc_set in loc_sets.all():
        existing_cols = loc_set.geo_df.columns
        for col in LocSetSharedCols.get_all():
            if LocSetSharedCols.must_exist(col_name=col):
                assert col in existing_cols
