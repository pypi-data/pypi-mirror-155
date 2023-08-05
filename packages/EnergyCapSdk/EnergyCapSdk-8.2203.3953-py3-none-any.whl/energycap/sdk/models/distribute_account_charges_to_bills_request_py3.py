# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DistributeAccountChargesToBillsRequest(Model):
    """DistributeAccountChargesToBillsRequest.

    :param bill_ids: Bill IDs for which account charges will be proportionally
     distributed to the meters <span class='property-internal'>Cannot be
     Empty</span> <span class='property-internal'>Required (defined)</span>
    :type bill_ids: list[int]
    :param split_basis:
    :type split_basis: int
    """

    _attribute_map = {
        'bill_ids': {'key': 'billIds', 'type': '[int]'},
        'split_basis': {'key': 'splitBasis', 'type': 'int'},
    }

    def __init__(self, *, bill_ids=None, split_basis: int=None, **kwargs) -> None:
        super(DistributeAccountChargesToBillsRequest, self).__init__(**kwargs)
        self.bill_ids = bill_ids
        self.split_basis = split_basis
