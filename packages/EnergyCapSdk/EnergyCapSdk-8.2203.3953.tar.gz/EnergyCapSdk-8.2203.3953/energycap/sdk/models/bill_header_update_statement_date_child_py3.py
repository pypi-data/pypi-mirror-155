# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillHeaderUpdateStatementDateChild(Model):
    """Statement Date.

    All required parameters must be populated in order to send to Azure.

    :param statement_date:  <span class='property-internal'>Must be between
     12/31/1899 and 1/1/3000</span> <span class='property-internal'>Required
     (defined)</span>
    :type statement_date: datetime
    :param update: Required. Indicates whether or not the header value is
     being updated <span class='property-internal'>Required</span>
    :type update: bool
    """

    _validation = {
        'update': {'required': True},
    }

    _attribute_map = {
        'statement_date': {'key': 'statementDate', 'type': 'iso-8601'},
        'update': {'key': 'update', 'type': 'bool'},
    }

    def __init__(self, *, update: bool, statement_date=None, **kwargs) -> None:
        super(BillHeaderUpdateStatementDateChild, self).__init__(**kwargs)
        self.statement_date = statement_date
        self.update = update
