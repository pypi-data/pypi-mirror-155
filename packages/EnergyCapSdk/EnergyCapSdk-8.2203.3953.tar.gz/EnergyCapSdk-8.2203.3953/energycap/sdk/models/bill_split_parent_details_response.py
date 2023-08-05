# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillSplitParentDetailsResponse(Model):
    """BillSplitParentDetailsResponse.

    :param split_parent_account:
    :type split_parent_account: ~energycap.sdk.models.AccountChild
    :param split_parent_meter:
    :type split_parent_meter: ~energycap.sdk.models.MeterChild
    :param begin_period: First billing period that the bill split was active
     for
    :type begin_period: int
    :param end_period: Last billing period that the bill split was active for
    :type end_period: int
    """

    _attribute_map = {
        'split_parent_account': {'key': 'splitParentAccount', 'type': 'AccountChild'},
        'split_parent_meter': {'key': 'splitParentMeter', 'type': 'MeterChild'},
        'begin_period': {'key': 'beginPeriod', 'type': 'int'},
        'end_period': {'key': 'endPeriod', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(BillSplitParentDetailsResponse, self).__init__(**kwargs)
        self.split_parent_account = kwargs.get('split_parent_account', None)
        self.split_parent_meter = kwargs.get('split_parent_meter', None)
        self.begin_period = kwargs.get('begin_period', None)
        self.end_period = kwargs.get('end_period', None)
