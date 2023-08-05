# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class VendorContractResponse(Model):
    """VendorContractResponse.

    :param contract_id: The contract identifier
    :type contract_id: int
    :param contract_code: The contract code
    :type contract_code: str
    :param contract_info: The contract info
    :type contract_info: str
    :param start_date: The start date of the contract
    :type start_date: datetime
    :param expiration_date: The expiration date of the contract
    :type expiration_date: datetime
    :param notes: Contract notes
    :type notes: str
    :param vendor:
    :type vendor: ~energycap.sdk.models.VendorChild
    :param commodity:
    :type commodity: ~energycap.sdk.models.CommodityChild
    :param renewal_reminder_date: The date a reminder will be sent for the
     contract expiration
    :type renewal_reminder_date: datetime
    :param is_green_energy: Is this a Green Energy contract
    :type is_green_energy: bool
    """

    _attribute_map = {
        'contract_id': {'key': 'contractId', 'type': 'int'},
        'contract_code': {'key': 'contractCode', 'type': 'str'},
        'contract_info': {'key': 'contractInfo', 'type': 'str'},
        'start_date': {'key': 'startDate', 'type': 'iso-8601'},
        'expiration_date': {'key': 'expirationDate', 'type': 'iso-8601'},
        'notes': {'key': 'notes', 'type': 'str'},
        'vendor': {'key': 'vendor', 'type': 'VendorChild'},
        'commodity': {'key': 'commodity', 'type': 'CommodityChild'},
        'renewal_reminder_date': {'key': 'renewalReminderDate', 'type': 'iso-8601'},
        'is_green_energy': {'key': 'isGreenEnergy', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(VendorContractResponse, self).__init__(**kwargs)
        self.contract_id = kwargs.get('contract_id', None)
        self.contract_code = kwargs.get('contract_code', None)
        self.contract_info = kwargs.get('contract_info', None)
        self.start_date = kwargs.get('start_date', None)
        self.expiration_date = kwargs.get('expiration_date', None)
        self.notes = kwargs.get('notes', None)
        self.vendor = kwargs.get('vendor', None)
        self.commodity = kwargs.get('commodity', None)
        self.renewal_reminder_date = kwargs.get('renewal_reminder_date', None)
        self.is_green_energy = kwargs.get('is_green_energy', None)
