# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class EnergyStarPmMeter(Model):
    """EnergyStarPmMeter.

    :param pm_meter_id: The Portfolio Manager meter identifier
    :type pm_meter_id: long
    :param pm_meter_name: The Portfolio Manager meter name
    :type pm_meter_name: str
    :param pm_commodity_code: The Portfolio Manager commodity
    :type pm_commodity_code: str
    :param pm_unit_code: The Portfolio Manager unit of measure
    :type pm_unit_code: str
    :param meter:
    :type meter: ~energycap.sdk.models.MeterChild
    :param unit:
    :type unit: ~energycap.sdk.models.UnitChild
    """

    _attribute_map = {
        'pm_meter_id': {'key': 'pmMeterId', 'type': 'long'},
        'pm_meter_name': {'key': 'pmMeterName', 'type': 'str'},
        'pm_commodity_code': {'key': 'pmCommodityCode', 'type': 'str'},
        'pm_unit_code': {'key': 'pmUnitCode', 'type': 'str'},
        'meter': {'key': 'meter', 'type': 'MeterChild'},
        'unit': {'key': 'unit', 'type': 'UnitChild'},
    }

    def __init__(self, *, pm_meter_id: int=None, pm_meter_name: str=None, pm_commodity_code: str=None, pm_unit_code: str=None, meter=None, unit=None, **kwargs) -> None:
        super(EnergyStarPmMeter, self).__init__(**kwargs)
        self.pm_meter_id = pm_meter_id
        self.pm_meter_name = pm_meter_name
        self.pm_commodity_code = pm_commodity_code
        self.pm_unit_code = pm_unit_code
        self.meter = meter
        self.unit = unit
