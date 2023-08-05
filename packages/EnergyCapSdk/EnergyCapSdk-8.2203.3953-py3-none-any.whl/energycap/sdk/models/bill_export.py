# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillExport(Model):
    """BillExport.

    All required parameters must be populated in order to send to Azure.

    :param bill_ids:  <span class='property-internal'>Cannot be Empty</span>
     <span class='property-internal'>NULL Valid</span> <span
     class='property-internal'>Required (defined)</span>
    :type bill_ids: list[int]
    :param export_mode: Required.  <span
     class='property-internal'>Required</span> <span
     class='property-internal'>One of ap, gl </span>
    :type export_mode: str
    :param mark_as_exported: Required.  <span
     class='property-internal'>Required</span>
    :type mark_as_exported: bool
    :param export_note: Optional note/comment. <span
     class='property-internal'>Required (defined)</span>
    :type export_note: str
    """

    _validation = {
        'export_mode': {'required': True},
        'mark_as_exported': {'required': True},
    }

    _attribute_map = {
        'bill_ids': {'key': 'billIds', 'type': '[int]'},
        'export_mode': {'key': 'exportMode', 'type': 'str'},
        'mark_as_exported': {'key': 'markAsExported', 'type': 'bool'},
        'export_note': {'key': 'exportNote', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(BillExport, self).__init__(**kwargs)
        self.bill_ids = kwargs.get('bill_ids', None)
        self.export_mode = kwargs.get('export_mode', None)
        self.mark_as_exported = kwargs.get('mark_as_exported', None)
        self.export_note = kwargs.get('export_note', None)
