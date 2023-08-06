from hdsr_wis_config_reader.location_sets.base import LocationSetBase
from hdsr_wis_config_reader.location_sets.hoofd import HoofdLocationSet
from hdsr_wis_config_reader.location_sets.msw import MswLocationSet
from hdsr_wis_config_reader.location_sets.ow import WaterstandLocationSet
from hdsr_wis_config_reader.location_sets.ps import PeilschaalLocationSet
from hdsr_wis_config_reader.location_sets.sub import SubLocationSet
from hdsr_wis_config_reader.readers.config_reader import FewsConfigReader
from typing import List

import pandas as pd  # noqa pandas comes with geopandas


class LocationSetCollection:
    def __init__(self, fews_config: FewsConfigReader):
        self.fews_config = fews_config
        self._hoofd_loc_new = None
        self._hoofd_loc = None
        self._sub_loc = None
        self._waterstand_loc = None
        self._msw_loc = None
        self._ps_loc = None

    def all(self) -> List[LocationSetBase]:
        return [self.hoofd_loc, self.sub_loc, self.waterstand_loc, self.msw_loc, self.ps_loc]

    @property
    def hoofd_loc(self) -> HoofdLocationSet:
        """Get HoofdLocationSet. The property .geo_df has eventually been updated."""
        if self._hoofd_loc_new is not None:
            assert self._hoofd_loc and isinstance(self._hoofd_loc, HoofdLocationSet)
            assert isinstance(self._hoofd_loc_new, pd.DataFrame)
            self._hoofd_loc._geo_df = self._hoofd_loc_new
        if self._hoofd_loc is not None:
            return self._hoofd_loc
        self._hoofd_loc = HoofdLocationSet(fews_config=self.fews_config)
        return self._hoofd_loc

    @property
    def sub_loc(self) -> SubLocationSet:
        if self._sub_loc is not None:
            return self._sub_loc
        self._sub_loc = SubLocationSet(fews_config=self.fews_config)
        return self._sub_loc

    @property
    def waterstand_loc(self) -> WaterstandLocationSet:
        if self._waterstand_loc is not None:
            return self._waterstand_loc
        self._waterstand_loc = WaterstandLocationSet(fews_config=self.fews_config)
        return self._waterstand_loc

    @property
    def msw_loc(self) -> MswLocationSet:
        if self._msw_loc is not None:
            return self._msw_loc
        self._msw_loc = MswLocationSet(fews_config=self.fews_config)
        return self._msw_loc

    @property
    def ps_loc(self) -> PeilschaalLocationSet:
        if self._ps_loc is not None:
            return self._ps_loc
        self._ps_loc = PeilschaalLocationSet(fews_config=self.fews_config)
        return self._ps_loc
