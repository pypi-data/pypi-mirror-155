# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MeterSerialNumberHistoryRequest(Model):
    """MeterSerialNumberHistoryRequest.

    All required parameters must be populated in order to send to Azure.

    :param new_serial_number: Required. Serial number that will replace the
     existing one <span class='property-internal'>Required</span>
    :type new_serial_number: str
    :param serial_number_change_date: Date that serial number changed <span
     class='property-internal'>Required (defined)</span>
    :type serial_number_change_date: datetime
    """

    _validation = {
        'new_serial_number': {'required': True},
    }

    _attribute_map = {
        'new_serial_number': {'key': 'newSerialNumber', 'type': 'str'},
        'serial_number_change_date': {'key': 'serialNumberChangeDate', 'type': 'iso-8601'},
    }

    def __init__(self, **kwargs):
        super(MeterSerialNumberHistoryRequest, self).__init__(**kwargs)
        self.new_serial_number = kwargs.get('new_serial_number', None)
        self.serial_number_change_date = kwargs.get('serial_number_change_date', None)
