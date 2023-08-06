"""cubicweb-api application package

This cube is the new api which will be integrated in CubicWeb 4.
"""
from datetime import datetime, date, time
from typing import Union

from pyramid.config import Configurator
from pyramid.renderers import JSON


def datetime_adapter(obj: Union[datetime, date, time], request):
    """
    Converts datetime, date and time object to an ISO string for JSON serialization
    :param obj: the object to convert
    :param request: the current request
    :return:
    """
    return obj.isoformat()


def includeme(config: Configurator):
    json_renderer = JSON()
    json_renderer.add_adapter(datetime, datetime_adapter)
    json_renderer.add_adapter(date, datetime_adapter)
    json_renderer.add_adapter(time, datetime_adapter)

    config.add_renderer("json", json_renderer)
    config.include(".routes")
