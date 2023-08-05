# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class FailedReadingResponse(Model):
    """FailedReadingResponse.

    :param channel_id:
    :type channel_id: int
    :param channel_import_id:
    :type channel_import_id: str
    :param meter_import_id:
    :type meter_import_id: str
    :param observation_type_code:
    :type observation_type_code: str
    :param unit_code:
    :type unit_code: str
    :param channel_interval_in_seconds:
    :type channel_interval_in_seconds: int
    :param readings:
    :type readings: list[~energycap.sdk.models.FailedReadings]
    :param error:
    :type error: str
    """

    _attribute_map = {
        'channel_id': {'key': 'channelId', 'type': 'int'},
        'channel_import_id': {'key': 'channelImportId', 'type': 'str'},
        'meter_import_id': {'key': 'meterImportId', 'type': 'str'},
        'observation_type_code': {'key': 'observationTypeCode', 'type': 'str'},
        'unit_code': {'key': 'unitCode', 'type': 'str'},
        'channel_interval_in_seconds': {'key': 'channelIntervalInSeconds', 'type': 'int'},
        'readings': {'key': 'readings', 'type': '[FailedReadings]'},
        'error': {'key': 'error', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(FailedReadingResponse, self).__init__(**kwargs)
        self.channel_id = kwargs.get('channel_id', None)
        self.channel_import_id = kwargs.get('channel_import_id', None)
        self.meter_import_id = kwargs.get('meter_import_id', None)
        self.observation_type_code = kwargs.get('observation_type_code', None)
        self.unit_code = kwargs.get('unit_code', None)
        self.channel_interval_in_seconds = kwargs.get('channel_interval_in_seconds', None)
        self.readings = kwargs.get('readings', None)
        self.error = kwargs.get('error', None)
