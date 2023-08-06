from enum import Enum


class IdMapChoices(Enum):
    idmap_opvl_water = "IdOPVLWATER"
    idmap_opvl_water_hymos = "IdOPVLWATER_HYMOS"
    idmap_hdsr_nsc = "IdHDSR_NSC"
    idmap_opvl_water_wq = "IdOPVLWATER_WQ"
    idmap_grondwater_caw = "IdGrondwaterCAW"

    @classmethod
    def get_all(cls):
        return [x.value for x in cls.__members__.values()]
