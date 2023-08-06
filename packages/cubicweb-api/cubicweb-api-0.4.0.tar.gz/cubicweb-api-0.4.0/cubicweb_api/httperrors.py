from pyramid.httpexceptions import exception_response

import logging

log = logging.getLogger(__name__)


def get_http_error(code: int, title: str, message: str, data: dict = None):
    return exception_response(
        code,
        json_body={
            "title": title,
            "message": message,
            "data": data,
        },
    )


def get_http_500_error():
    """
    Returns an HTTP 500 error without content as it could lead to security leaks
    """
    return get_http_error(
        500,
        "ServerError",
        "The server encountered an error. Please contact support.",
    )
