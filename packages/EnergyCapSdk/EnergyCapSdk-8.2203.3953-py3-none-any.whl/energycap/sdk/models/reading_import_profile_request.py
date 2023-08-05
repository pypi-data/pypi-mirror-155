# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ReadingImportProfileRequest(Model):
    """ReadingImportProfileRequest.

    All required parameters must be populated in order to send to Azure.

    :param profile_code: Required. The profile code <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 64 characters</span>
    :type profile_code: str
    :param channel_interval_in_seconds: The interval of the readings in
     seconds
    :type channel_interval_in_seconds: int
    :param delimiter: Required. The string that represents how the file
     contents are delimited.  Valid options are "\\t" for tab, " " for space
     and "," for comma. <span class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 1 and 2 characters</span> <span
     class='property-internal'>One of 	,  , , </span>
    :type delimiter: str
    :param number_of_header_rows: Required. Number of header rows before the
     data begins <span class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 2147483647</span>
    :type number_of_header_rows: int
    :param timestamp_column_number: The number of the column that holds the
     timestamp <span class='property-internal'>Must be between 1 and
     2147483647</span>
    :type timestamp_column_number: int
    :param timestamp_format: The format for the timestamp of the readings. An
     example is MM/dd/yyyy mm:hh:ss:zzz
    :type timestamp_format: str
    :param date_column_number: The number of the column that holds the date
     <span class='property-internal'>Must be between 1 and 2147483647</span>
    :type date_column_number: int
    :param time_column_number: The number of the column that holds the time
     <span class='property-internal'>Must be between 1 and 2147483647</span>
    :type time_column_number: int
    :param date_format: The format for the date of the readings. An example is
     MM/dd/yyyy
    :type date_format: str
    :param time_format: The format for the time of the readings. An example is
     mm:hh:ss:zzz
    :type time_format: str
    :param time_zone_id: The time zone for the readings
    :type time_zone_id: int
    :param meter_import_id_column_number: The number of the column that holds
     the meter import identifier <span class='property-internal'>Must be
     between 1 and 2147483647</span>
    :type meter_import_id_column_number: int
    :param channel_import_id_column_number: The number of the column that
     holds the channel import identifier <span class='property-internal'>Must
     be between 1 and 2147483647</span>
    :type channel_import_id_column_number: int
    :param number_of_columns: Required. The minimum number of columns in the
     import sheet <span class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 1 and 2147483647</span>
    :type number_of_columns: int
    :param data_mapping: A list of columns from the import sheet with their
     observation type and unit
    :type data_mapping: list[~energycap.sdk.models.ReadingImportProfileColumn]
    :param estimated:
    :type estimated: ~energycap.sdk.models.Estimated
    :param note_column_number: Column number that holds a note to be stored
     with the reading <span class='property-internal'>Must be between 1 and
     2147483647</span>
    :type note_column_number: int
    """

    _validation = {
        'profile_code': {'required': True, 'max_length': 64, 'min_length': 0},
        'delimiter': {'required': True, 'max_length': 2, 'min_length': 1},
        'number_of_header_rows': {'required': True, 'maximum': 2147483647, 'minimum': 0},
        'timestamp_column_number': {'maximum': 2147483647, 'minimum': 1},
        'date_column_number': {'maximum': 2147483647, 'minimum': 1},
        'time_column_number': {'maximum': 2147483647, 'minimum': 1},
        'meter_import_id_column_number': {'maximum': 2147483647, 'minimum': 1},
        'channel_import_id_column_number': {'maximum': 2147483647, 'minimum': 1},
        'number_of_columns': {'required': True, 'maximum': 2147483647, 'minimum': 1},
        'note_column_number': {'maximum': 2147483647, 'minimum': 1},
    }

    _attribute_map = {
        'profile_code': {'key': 'profileCode', 'type': 'str'},
        'channel_interval_in_seconds': {'key': 'channelIntervalInSeconds', 'type': 'int'},
        'delimiter': {'key': 'delimiter', 'type': 'str'},
        'number_of_header_rows': {'key': 'numberOfHeaderRows', 'type': 'int'},
        'timestamp_column_number': {'key': 'timestampColumnNumber', 'type': 'int'},
        'timestamp_format': {'key': 'timestampFormat', 'type': 'str'},
        'date_column_number': {'key': 'dateColumnNumber', 'type': 'int'},
        'time_column_number': {'key': 'timeColumnNumber', 'type': 'int'},
        'date_format': {'key': 'dateFormat', 'type': 'str'},
        'time_format': {'key': 'timeFormat', 'type': 'str'},
        'time_zone_id': {'key': 'timeZoneId', 'type': 'int'},
        'meter_import_id_column_number': {'key': 'meterImportIdColumnNumber', 'type': 'int'},
        'channel_import_id_column_number': {'key': 'channelImportIdColumnNumber', 'type': 'int'},
        'number_of_columns': {'key': 'numberOfColumns', 'type': 'int'},
        'data_mapping': {'key': 'dataMapping', 'type': '[ReadingImportProfileColumn]'},
        'estimated': {'key': 'estimated', 'type': 'Estimated'},
        'note_column_number': {'key': 'noteColumnNumber', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(ReadingImportProfileRequest, self).__init__(**kwargs)
        self.profile_code = kwargs.get('profile_code', None)
        self.channel_interval_in_seconds = kwargs.get('channel_interval_in_seconds', None)
        self.delimiter = kwargs.get('delimiter', None)
        self.number_of_header_rows = kwargs.get('number_of_header_rows', None)
        self.timestamp_column_number = kwargs.get('timestamp_column_number', None)
        self.timestamp_format = kwargs.get('timestamp_format', None)
        self.date_column_number = kwargs.get('date_column_number', None)
        self.time_column_number = kwargs.get('time_column_number', None)
        self.date_format = kwargs.get('date_format', None)
        self.time_format = kwargs.get('time_format', None)
        self.time_zone_id = kwargs.get('time_zone_id', None)
        self.meter_import_id_column_number = kwargs.get('meter_import_id_column_number', None)
        self.channel_import_id_column_number = kwargs.get('channel_import_id_column_number', None)
        self.number_of_columns = kwargs.get('number_of_columns', None)
        self.data_mapping = kwargs.get('data_mapping', None)
        self.estimated = kwargs.get('estimated', None)
        self.note_column_number = kwargs.get('note_column_number', None)
