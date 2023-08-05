# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DashboardEdit(Model):
    """DashboardEdit.

    All required parameters must be populated in order to send to Azure.

    :param dashboard_info: Required. The Dashboard Title <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 255 characters</span>
    :type dashboard_info: str
    :param description: The dashboard description <span
     class='property-internal'>Must be between 0 and 255 characters</span>
     <span class='property-internal'>Required (defined)</span>
    :type description: str
    :param type: The dashboard type <span class='property-internal'>One of
     User, Map </span> <span class='property-internal'>Required
     (defined)</span>
    :type type: str
    :param public: Required. Flag to indicate if the dashboard is public <span
     class='property-internal'>Required</span>
    :type public: bool
    """

    _validation = {
        'dashboard_info': {'required': True, 'max_length': 255, 'min_length': 0},
        'description': {'max_length': 255, 'min_length': 0},
        'public': {'required': True},
    }

    _attribute_map = {
        'dashboard_info': {'key': 'dashboardInfo', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'public': {'key': 'public', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(DashboardEdit, self).__init__(**kwargs)
        self.dashboard_info = kwargs.get('dashboard_info', None)
        self.description = kwargs.get('description', None)
        self.type = kwargs.get('type', None)
        self.public = kwargs.get('public', None)
