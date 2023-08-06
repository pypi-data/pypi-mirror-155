from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from trueway_geocoding_rapidapi.schemas.base import BaseModelORM
from trueway_geocoding_rapidapi.schemas.enums import ReverseGeocodeItemLocationType
from trueway_geocoding_rapidapi.schemas.enums import ReverseGeocodeItemType


class ReverseGeocodeLocation(BaseModelORM):
    lat: int
    lng: int


class ReverseGeocodeItem(BaseModelORM):
    type: ReverseGeocodeItemType
    location_type: ReverseGeocodeItemLocationType
    location: ReverseGeocodeLocation
    address: str
    country: str
    locality: str
    region: Optional[str]
    area: Optional[str]
    neighborhood: Optional[str]
    postal_code: Optional[str]
    street: Optional[str]
    house: Optional[str]


class ReverseGeocodeModel(object):
    exact_building: ReverseGeocodeItem
    exact_street_address: ReverseGeocodeItem
    approximate_street_address: ReverseGeocodeItem
    centroid_poi: ReverseGeocodeItem
    centroid_route: ReverseGeocodeItem

    def parse_obj(self, obj: List[ReverseGeocodeItem]):
        for el in obj:
            if el.location_type == ReverseGeocodeItemLocationType.exact and \
                el.type == ReverseGeocodeItemType.building:
                self.exact_building = el
                continue

            if el.location_type == ReverseGeocodeItemLocationType.exact and \
                el.type == ReverseGeocodeItemType.street_address:
                self.exact_street_address = el
                continue

            if el.location_type == ReverseGeocodeItemLocationType.approximate and \
                el.type == ReverseGeocodeItemType.street_address:
                self.approximate_street_address = el
                continue

            if el.location_type == ReverseGeocodeItemLocationType.centroid and \
                el.type == ReverseGeocodeItemType.poi:
                self.centroid_poi = el
                continue

            if el.location_type == ReverseGeocodeItemLocationType.centroid and \
                el.type == ReverseGeocodeItemType.route:
                self.centroid_route = el
                continue

        return self
