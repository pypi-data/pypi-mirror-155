import logging
from os import path
from typing import Union, Dict, Optional

from cubicweb import ConfigurationError
from openapi_spec_validator.schemas import read_yaml_file
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response
from pyramid_openapi3 import (
    RequestValidationError,
    ResponseValidationError,
    openapi_validation_error,
)
from yaml import dump

from cubicweb_api.constants import API_ROUTE_NAME_PREFIX
from cubicweb_api.httperrors import get_http_error, get_http_500_error
from cubicweb_api.util import get_cw_repo

log = logging.getLogger(__name__)

OPENAPI_PYRAMID_KEY = "x-pyramid-route-name"


def get_template_file_path() -> str:
    return path.join(path.dirname(__file__), "openapi_template.yaml")


def get_production_file_path(config: Configurator) -> str:
    return path.join(get_cw_repo(config).config.apphome, "openapi.yaml")


def generate_openapi_file(config: Configurator, path_prefix: str):
    spec_dict: Dict = read_yaml_file(get_template_file_path())
    paths_dict: Optional[Dict[str, Dict]] = spec_dict.get("paths")
    edited_path_dict = {}
    if paths_dict is None:
        raise ConfigurationError("Missing 'paths' object in openapi yaml template")
    for path_str, path_item in paths_dict.items():
        path_item[
            OPENAPI_PYRAMID_KEY
        ] = f"{API_ROUTE_NAME_PREFIX}{path_item[OPENAPI_PYRAMID_KEY]}"
        edited_path_dict[f"{path_prefix}{path_str}"] = path_item
    spec_dict["paths"] = edited_path_dict
    with open(get_production_file_path(config), "w") as file:
        dump(spec_dict, file)


def register_openapi_routes(config: Configurator, path_prefix: str):
    config.include("pyramid_openapi3")
    generate_openapi_file(config, path_prefix)
    # TODO block access if anonymous access is disabled and user is not connected
    config.pyramid_openapi3_spec(
        get_production_file_path(config),
        route=f"{path_prefix}/openapi.yaml",
    )
    config.pyramid_openapi3_add_explorer(route=f"{path_prefix}/openapi")
    config.registry.settings["pyramid_openapi3.enable_endpoint_validation"] = True
    config.registry.settings["pyramid_openapi3.enable_request_validation"] = True
    # Do not validate responses as it could slow down the server
    config.registry.settings["pyramid_openapi3.enable_response_validation"] = False
    config.add_exception_view(
        view=custom_openapi_validation_error, context=RequestValidationError
    )
    config.add_exception_view(
        view=custom_openapi_validation_error, context=ResponseValidationError
    )


def custom_openapi_validation_error(
    context: Union[RequestValidationError, ResponseValidationError], request: Request
) -> Response:
    """Overrides default pyramid_openapi3 errors to match the API format."""
    error_response = openapi_validation_error(context, request)

    status = error_response.status_code
    body = error_response.json_body
    if status == 500:
        return get_http_500_error()
    if status == 400:
        return get_http_error(
            error_response.status_code,
            "OpenApiValidationError",
            "Your request could not be validated against the openapi specification.",
            body,
        )

    return get_http_error(error_response.status_code, "OpenAPI Error", "", body)
