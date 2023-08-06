from hdsr_wis_config_reader.idmappings.utils import get_class_attributes
from typing import Dict


class LocSetSharedCols:
    """Each location set (e.g hoofd_loc, sub_loc, etc) csv has it own columns.
     However, some columns are shared by all csvs."""

    loc_id = "LOC_ID"
    loc_name = "LOC_NAME"
    x = "X"
    y = "Y"
    z = "Z"  # only in hoof_loc and waterstand_loc
    gpgident = "GPGIDENT"
    gafcode = "GAFCODE"
    rbgid = "RBGID"
    start = "START"  # in all loc_set except for msw_loc
    eind = "EIND"  # in all loc_set except for msw_loc

    @classmethod
    def must_exist(cls, col_name: str) -> bool:
        """Columns 'start' and 'eind' are in all loc_sets except for msw_loc.
        Column 'z''is only in hoofd_loc and waterstand_loc."""
        return col_name in {cls.loc_id, cls.loc_name, cls.x, cls.y, cls.gpgident, cls.gafcode, cls.rbgid}

    @classmethod
    def get_all(cls) -> Dict:
        return get_class_attributes(the_class=cls)
