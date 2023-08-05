# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SpecialAdjustmentType(Model):
    """SpecialAdjustmentType.

    :param special_adjustment_type_id: Special Adjustment type identifier
    :type special_adjustment_type_id: int
    :param special_adjustment_type_code: Special Adjustment type code
    :type special_adjustment_type_code: str
    :param special_adjustment_type_info: Special Adjustment type name
    :type special_adjustment_type_info: str
    """

    _attribute_map = {
        'special_adjustment_type_id': {'key': 'specialAdjustmentTypeId', 'type': 'int'},
        'special_adjustment_type_code': {'key': 'specialAdjustmentTypeCode', 'type': 'str'},
        'special_adjustment_type_info': {'key': 'specialAdjustmentTypeInfo', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(SpecialAdjustmentType, self).__init__(**kwargs)
        self.special_adjustment_type_id = kwargs.get('special_adjustment_type_id', None)
        self.special_adjustment_type_code = kwargs.get('special_adjustment_type_code', None)
        self.special_adjustment_type_info = kwargs.get('special_adjustment_type_info', None)
