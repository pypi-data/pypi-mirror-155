# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ListIds(Model):
    """ListIds.

    :param ids:  <span class='property-internal'>Required (defined)</span>
    :type ids: list[int]
    """

    _attribute_map = {
        'ids': {'key': 'ids', 'type': '[int]'},
    }

    def __init__(self, **kwargs):
        super(ListIds, self).__init__(**kwargs)
        self.ids = kwargs.get('ids', None)
