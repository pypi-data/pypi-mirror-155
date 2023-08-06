from enum import Enum
from hdsr_wis_config_reader.location_sets.hoofd import HoofdLocTypeChoices
from hdsr_wis_config_reader.location_sets.sub import SubLocTypeChoices

import logging
import re


logger = logging.getLogger(__name__)


class ValidationCsvChoices(Enum):
    # waterstandlocaties
    ow_ws_validatie = "ow_ws_validatie"
    # sublocaties
    ow_validatie_debiet = "ow_validatie_debiet"
    ow_validatie_kroos = "ow_validatie_kroos"
    ow_validatie_freq = "ow_validatie_freq"
    ow_validatie_hefh = "ow_validatie_hefh"
    ow_validatie_kruinh = "ow_validatie_kruinh"
    ow_validatie_schuifp = "ow_validatie_schuifp"
    ow_validatie_schuifp2 = "ow_validatie_schuifp2"
    ow_validatie_streef1 = "ow_validatie_streef1"
    ow_validatie_streef2 = "ow_validatie_streef2"
    ow_validatie_streef3 = "ow_validatie_streef3"
    ow_validatie_stuur1 = "ow_validatie_stuur1"
    ow_validatie_stuur2 = "ow_validatie_stuur2"
    ow_validatie_stuur3 = "ow_validatie_stuur3"
    ow_validatie_toert = "ow_validatie_toert"

    @classmethod
    def get_validation_csv_name(cls, int_par: str, loc_type: str) -> str:
        match = [
            int_par_regex
            for int_par_regex in INTPAR_2_VALIDATION_CSV.keys()
            if bool(re.match(pattern=int_par_regex, string=int_par))
        ]
        if not match:
            logger.debug(f"no validation csv found: int_par={int_par} not in INTPAR_2_VALIDATION_CSV.keys")
            return ""
        assert len(match) == 1
        mapper = INTPAR_2_VALIDATION_CSV[match[0]]
        filename = mapper.get(loc_type, None)
        if not filename:
            logger.debug(
                f"no validation csv found: int_par={int_par} has only loc_types={mapper.keys()}, no {loc_type}"
            )
        return filename


INTPAR_2_VALIDATION_CSV = {
    "H.G.": {
        HoofdLocTypeChoices.waterstand.value: ValidationCsvChoices.ow_ws_validatie.value,
        SubLocTypeChoices.krooshek.value: ValidationCsvChoices.ow_validatie_kroos.value,
    },
    "Hh.": {
        SubLocTypeChoices.schuif.value: ValidationCsvChoices.ow_validatie_hefh.value,
        SubLocTypeChoices.vispassage.value: ValidationCsvChoices.ow_validatie_hefh.value,
    },
    "Q.G.": {
        # we only validate it for debietmeters (not schuif, vispassage, pompvijzel, stuw)
        SubLocTypeChoices.debietmeter.value: ValidationCsvChoices.ow_validatie_debiet.value
    },
    "F.": {SubLocTypeChoices.pompvijzel.value: ValidationCsvChoices.ow_validatie_freq.value},
    "Hk.": {SubLocTypeChoices.stuw.value: ValidationCsvChoices.ow_validatie_kruinh.value},
    "POS.": {SubLocTypeChoices.schuif.value: ValidationCsvChoices.ow_validatie_schuifp.value},
    "POS2.": {SubLocTypeChoices.schuif.value: ValidationCsvChoices.ow_validatie_schuifp2.value},
    "H.S.": {HoofdLocTypeChoices.waterstand.value: ValidationCsvChoices.ow_validatie_streef1.value},
    "H2.S.": {HoofdLocTypeChoices.waterstand.value: ValidationCsvChoices.ow_validatie_streef2.value},
    "H3.S.": {HoofdLocTypeChoices.waterstand.value: ValidationCsvChoices.ow_validatie_streef3.value},
    "H.R.": {HoofdLocTypeChoices.waterstand.value: ValidationCsvChoices.ow_validatie_stuur1.value},
    "H2.R.": {HoofdLocTypeChoices.waterstand.value: ValidationCsvChoices.ow_validatie_stuur2.value},
    "H3.R.": {HoofdLocTypeChoices.waterstand.value: ValidationCsvChoices.ow_validatie_stuur3.value},
    "TT.": {SubLocTypeChoices.pompvijzel.value: ValidationCsvChoices.ow_validatie_toert.value},
}
