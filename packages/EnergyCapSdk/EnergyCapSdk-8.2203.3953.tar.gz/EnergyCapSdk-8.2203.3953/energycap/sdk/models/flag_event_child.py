# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class FlagEventChild(Model):
    """FlagEventChild.

    :param flag_event_id: The flag event identifier
    :type flag_event_id: int
    :param created_by:
    :type created_by: ~energycap.sdk.models.UserChild
    :param created_date: Date that this flag event was created
    :type created_date: datetime
    :param comment: Comment about the flag event
    :type comment: str
    :param description: Description of the flag event
    :type description: str
    :param flag_action:
    :type flag_action: ~energycap.sdk.models.FlagActionChild
    """

    _attribute_map = {
        'flag_event_id': {'key': 'flagEventId', 'type': 'int'},
        'created_by': {'key': 'createdBy', 'type': 'UserChild'},
        'created_date': {'key': 'createdDate', 'type': 'iso-8601'},
        'comment': {'key': 'comment', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'flag_action': {'key': 'flagAction', 'type': 'FlagActionChild'},
    }

    def __init__(self, **kwargs):
        super(FlagEventChild, self).__init__(**kwargs)
        self.flag_event_id = kwargs.get('flag_event_id', None)
        self.created_by = kwargs.get('created_by', None)
        self.created_date = kwargs.get('created_date', None)
        self.comment = kwargs.get('comment', None)
        self.description = kwargs.get('description', None)
        self.flag_action = kwargs.get('flag_action', None)
