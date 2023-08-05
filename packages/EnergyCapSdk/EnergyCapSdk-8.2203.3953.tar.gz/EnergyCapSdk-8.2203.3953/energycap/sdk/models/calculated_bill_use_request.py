# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CalculatedBillUseRequest(Model):
    """Defines how use is calculated for a calculated bill distribution.

    :param readings_channel_id: Use monthly channel data readings to calculate
     bill use <span class='property-internal'>Required (defined)</span>
    :type readings_channel_id: int
    :param fixed_amount:
    :type fixed_amount: ~energycap.sdk.models.FixedUseRequest
    :param copy_use_from_meter:
    :type copy_use_from_meter: ~energycap.sdk.models.CopyMeterRequest
    :param use_calculation:
    :type use_calculation: ~energycap.sdk.models.CalculationRequest
    :param calendarized_use_calculation:
    :type calendarized_use_calculation:
     ~energycap.sdk.models.CalendarizedCalculationRequest
    """

    _attribute_map = {
        'readings_channel_id': {'key': 'readingsChannelId', 'type': 'int'},
        'fixed_amount': {'key': 'fixedAmount', 'type': 'FixedUseRequest'},
        'copy_use_from_meter': {'key': 'copyUseFromMeter', 'type': 'CopyMeterRequest'},
        'use_calculation': {'key': 'useCalculation', 'type': 'CalculationRequest'},
        'calendarized_use_calculation': {'key': 'calendarizedUseCalculation', 'type': 'CalendarizedCalculationRequest'},
    }

    def __init__(self, **kwargs):
        super(CalculatedBillUseRequest, self).__init__(**kwargs)
        self.readings_channel_id = kwargs.get('readings_channel_id', None)
        self.fixed_amount = kwargs.get('fixed_amount', None)
        self.copy_use_from_meter = kwargs.get('copy_use_from_meter', None)
        self.use_calculation = kwargs.get('use_calculation', None)
        self.calendarized_use_calculation = kwargs.get('calendarized_use_calculation', None)
