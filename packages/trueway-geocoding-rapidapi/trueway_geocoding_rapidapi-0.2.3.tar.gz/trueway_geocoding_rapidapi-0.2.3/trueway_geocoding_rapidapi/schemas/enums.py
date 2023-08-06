import enum


class ReverseGeocodeItemLocationType(enum.Enum):
    exact = "exact"
    approximate = "approximate"
    centroid = "centroid"


class ReverseGeocodeItemType(enum.Enum):
    building = "building"
    street_address = "street_address"
    poi = "poi"
    route = "route"
