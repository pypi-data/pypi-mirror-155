# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class RouteResponse(Model):
    """RouteResponse.

    :param number_of_meters: The number of meters assigned to this route
    :type number_of_meters: int
    :param route_id: The route identifier
    :type route_id: int
    :param route_info: The route info
    :type route_info: str
    :param route_code: The route code
    :type route_code: str
    """

    _attribute_map = {
        'number_of_meters': {'key': 'numberOfMeters', 'type': 'int'},
        'route_id': {'key': 'routeId', 'type': 'int'},
        'route_info': {'key': 'routeInfo', 'type': 'str'},
        'route_code': {'key': 'routeCode', 'type': 'str'},
    }

    def __init__(self, *, number_of_meters: int=None, route_id: int=None, route_info: str=None, route_code: str=None, **kwargs) -> None:
        super(RouteResponse, self).__init__(**kwargs)
        self.number_of_meters = number_of_meters
        self.route_id = route_id
        self.route_info = route_info
        self.route_code = route_code
