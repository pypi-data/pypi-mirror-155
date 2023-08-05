# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Commodity(Model):
    """Commodity.

    :param commodity_id: The Commodity ID
    :type commodity_id: int
    :param commodity_code: The Commodity Code
    :type commodity_code: str
    :param commodity_info: The Commodity Info
    :type commodity_info: str
    :param in_use_by_vendor: Flag to indicate if the commodity is assigned to
     any meters
    :type in_use_by_vendor: bool
    :param common_use_unit:
    :type common_use_unit: ~energycap.sdk.models.UnitChild
    :param common_demand_unit:
    :type common_demand_unit: ~energycap.sdk.models.UnitChild
    """

    _attribute_map = {
        'commodity_id': {'key': 'commodityId', 'type': 'int'},
        'commodity_code': {'key': 'commodityCode', 'type': 'str'},
        'commodity_info': {'key': 'commodityInfo', 'type': 'str'},
        'in_use_by_vendor': {'key': 'inUseByVendor', 'type': 'bool'},
        'common_use_unit': {'key': 'commonUseUnit', 'type': 'UnitChild'},
        'common_demand_unit': {'key': 'commonDemandUnit', 'type': 'UnitChild'},
    }

    def __init__(self, **kwargs):
        super(Commodity, self).__init__(**kwargs)
        self.commodity_id = kwargs.get('commodity_id', None)
        self.commodity_code = kwargs.get('commodity_code', None)
        self.commodity_info = kwargs.get('commodity_info', None)
        self.in_use_by_vendor = kwargs.get('in_use_by_vendor', None)
        self.common_use_unit = kwargs.get('common_use_unit', None)
        self.common_demand_unit = kwargs.get('common_demand_unit', None)
