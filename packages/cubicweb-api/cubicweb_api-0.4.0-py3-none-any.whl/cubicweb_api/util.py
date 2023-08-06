# -*- coding: utf-8 -*-
# copyright 2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
import re
from typing import Union

from cubicweb import ConfigurationError
from cubicweb.pyramid.config import AllInOneConfiguration
from cubicweb.pyramid.core import CubicWebPyramidRequest
from cubicweb.server.repository import Repository
from pyramid.config import Configurator
from pyramid.request import Request

from cubicweb_api.constants import API_PATH_DEFAULT_PREFIX


def get_cw_request(request: Request) -> CubicWebPyramidRequest:
    return request.cw_request


def get_cw_repo(req_or_conf: Union[Request, Configurator]) -> Repository:
    return req_or_conf.registry["cubicweb.repository"]


def get_cw_all_in_one_config(config: Configurator) -> AllInOneConfiguration:
    return get_cw_repo(config).config


def get_api_server_base(config: Configurator):
    repo = get_cw_repo(config)
    server_name: str = (
        repo.get_option_value("api-server-name")
        or get_cw_all_in_one_config(config).default_base_url()
    )
    match = re.match("^[a-zA-Z0-9-_@.&+!*(),/:]{1,60}$", server_name)
    if match:
        return server_name
    else:
        if len(server_name) > 60:
            raise ConfigurationError(
                f"api-server-name '{server_name}' is too long. "
                f"Max size allowed is 60 characters. "
                f"Current size is {len(server_name)}."
            )
        raise ConfigurationError(
            f"api-server-name '{server_name}' contains invalid characters. "
            "Allowed characters are: a-zA-Z0-9-_@.&+!*(),/:"
        )


def get_api_path_prefix(config: Configurator) -> str:
    repo = get_cw_repo(config)
    path_prefix: str = (
        repo.get_option_value("api-path-prefix") or API_PATH_DEFAULT_PREFIX
    )
    match = re.match("^/[a-zA-Z0-9-_@.&+!*(),/]{1,29}$", path_prefix)
    if match:
        return f"{path_prefix.rstrip('/')}/v1"
    else:
        if len(path_prefix) > 30:
            raise ConfigurationError(
                f"api-path-prefix '{path_prefix}' is too long. "
                f"Max size allowed is 30 characters. "
                f"Current size is {len(path_prefix)}."
            )
        if not path_prefix.startswith("/"):
            raise ConfigurationError(
                f"api-path-prefix '{path_prefix}' does not start with '/'. "
                "Prefix should start with '/' to be validated by openapi"
            )

        raise ConfigurationError(
            f"api-path-prefix '{path_prefix}' contains invalid characters. "
            "Allowed characters are: a-zA-Z0-9-_@.&+!*(),/"
        )
