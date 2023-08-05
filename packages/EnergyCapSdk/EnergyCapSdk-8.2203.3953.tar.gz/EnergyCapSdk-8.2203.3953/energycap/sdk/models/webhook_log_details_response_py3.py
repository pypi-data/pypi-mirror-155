# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class WebhookLogDetailsResponse(Model):
    """WebhookLogDetailsResponse.

    :param url: The URL that the webhook is configured for <span
     class='property-internal'>Required (defined)</span>
    :type url: str
    :param request: The request that was sent from the webhook (headers and
     body) <span class='property-internal'>Required (defined)</span>
    :type request: str
    :param response: The response that was received from the configured url
     (headers and body) <span class='property-internal'>Required
     (defined)</span>
    :type response: str
    :param result: The HTTP status code that was received from the configured
     url
     0 indicates no response was received from the configured url <span
     class='property-internal'>Required (defined)</span>
    :type result: str
    :param user:
    :type user: ~energycap.sdk.models.UserChild
    """

    _attribute_map = {
        'url': {'key': 'url', 'type': 'str'},
        'request': {'key': 'request', 'type': 'str'},
        'response': {'key': 'response', 'type': 'str'},
        'result': {'key': 'result', 'type': 'str'},
        'user': {'key': 'user', 'type': 'UserChild'},
    }

    def __init__(self, *, url: str=None, request: str=None, response: str=None, result: str=None, user=None, **kwargs) -> None:
        super(WebhookLogDetailsResponse, self).__init__(**kwargs)
        self.url = url
        self.request = request
        self.response = response
        self.result = result
        self.user = user
