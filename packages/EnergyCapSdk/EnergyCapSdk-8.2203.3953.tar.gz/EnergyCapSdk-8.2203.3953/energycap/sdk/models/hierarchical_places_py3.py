# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class HierarchicalPlaces(Model):
    """HierarchicalPlaces.

    :param parent_id: The place's parent
    :type parent_id: int
    :param place_id: The place's primary ID
    :type place_id: int
    :param place_info: PlaceInfo
    :type place_info: str
    :param place_code: PlaceCode
    :type place_code: str
    :param place_type_id: PlaceTypeID
    :type place_type_id: int
    :param has_children: If this place has any children, either meters or
     places
    :type has_children: bool
    :param has_place_children: If this place has any place children
    :type has_place_children: bool
    :param has_meter_children: If this place has any meter children
    :type has_meter_children: bool
    :param has_active_children: If this place has any place children or active
     meter children
    :type has_active_children: bool
    :param has_active_meter_children: If this place has any active meter
     children
    :type has_active_meter_children: bool
    :param meter_children: List of meter children
    :type meter_children: list[~energycap.sdk.models.MeterChild]
    :param place_children: List of place children
    :type place_children: list[~energycap.sdk.models.HierarchicalPlaces2]
    """

    _attribute_map = {
        'parent_id': {'key': 'parentId', 'type': 'int'},
        'place_id': {'key': 'placeId', 'type': 'int'},
        'place_info': {'key': 'placeInfo', 'type': 'str'},
        'place_code': {'key': 'placeCode', 'type': 'str'},
        'place_type_id': {'key': 'placeTypeId', 'type': 'int'},
        'has_children': {'key': 'hasChildren', 'type': 'bool'},
        'has_place_children': {'key': 'hasPlaceChildren', 'type': 'bool'},
        'has_meter_children': {'key': 'hasMeterChildren', 'type': 'bool'},
        'has_active_children': {'key': 'hasActiveChildren', 'type': 'bool'},
        'has_active_meter_children': {'key': 'hasActiveMeterChildren', 'type': 'bool'},
        'meter_children': {'key': 'meterChildren', 'type': '[MeterChild]'},
        'place_children': {'key': 'placeChildren', 'type': '[HierarchicalPlaces2]'},
    }

    def __init__(self, *, parent_id: int=None, place_id: int=None, place_info: str=None, place_code: str=None, place_type_id: int=None, has_children: bool=None, has_place_children: bool=None, has_meter_children: bool=None, has_active_children: bool=None, has_active_meter_children: bool=None, meter_children=None, place_children=None, **kwargs) -> None:
        super(HierarchicalPlaces, self).__init__(**kwargs)
        self.parent_id = parent_id
        self.place_id = place_id
        self.place_info = place_info
        self.place_code = place_code
        self.place_type_id = place_type_id
        self.has_children = has_children
        self.has_place_children = has_place_children
        self.has_meter_children = has_meter_children
        self.has_active_children = has_active_children
        self.has_active_meter_children = has_active_meter_children
        self.meter_children = meter_children
        self.place_children = place_children
