# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MeterTypeChild(Model):
    """MeterTypeChild.

    :param meter_type_id:
    :type meter_type_id: int
    :param meter_type_code:
    :type meter_type_code: str
    :param meter_type_info:
    :type meter_type_info: str
    """

    _attribute_map = {
        'meter_type_id': {'key': 'meterTypeId', 'type': 'int'},
        'meter_type_code': {'key': 'meterTypeCode', 'type': 'str'},
        'meter_type_info': {'key': 'meterTypeInfo', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(MeterTypeChild, self).__init__(**kwargs)
        self.meter_type_id = kwargs.get('meter_type_id', None)
        self.meter_type_code = kwargs.get('meter_type_code', None)
        self.meter_type_info = kwargs.get('meter_type_info', None)
