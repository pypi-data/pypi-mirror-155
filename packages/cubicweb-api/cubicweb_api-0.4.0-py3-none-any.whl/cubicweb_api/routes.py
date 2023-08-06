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
from enum import Enum

from cubicweb import AuthenticationError, QueryError, Unauthorized, Forbidden
from cubicweb.schema_exporters import JSONSchemaExporter
from rql import RQLException
from yams import ValidationError, UnknownType
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPError
import logging

from cubicweb_api.api_transaction import ApiTransactionsRepository
from cubicweb_api.constants import (
    DEFAULT_ROUTE_PARAMS,
    API_ROUTE_NAME_PREFIX,
)
from cubicweb_api.httperrors import get_http_error, get_http_500_error
from cubicweb_api.jwt_auth import setup_jwt
from cubicweb_api.openapi.openapi import register_openapi_routes
from cubicweb_api.util import get_cw_repo, get_cw_request, get_api_path_prefix

log = logging.getLogger(__name__)


class ApiRoutes(str, Enum):
    schema = "schema"
    rql = "rql"
    login = "login"
    transaction_begin = "transaction/begin"
    transaction_execute = "transaction/execute"
    transaction_commit = "transaction/commit"
    transaction_rollback = "transaction/rollback"
    help = "help"


def is_user_allowed(request: Request):
    return (
        request.authenticated_userid is not None
        or get_cw_repo(request).config["anonymous-user"] is not None
    )


def cw_view_config(route_name: str, **kwargs):
    return view_config(
        route_name=f"{API_ROUTE_NAME_PREFIX}{route_name}",
        **dict(DEFAULT_ROUTE_PARAMS, **kwargs),
    )


def view_exception_handler(func):
    """
    Use it as a decorator for any pyramid view to catch AuthenticationError to raise HTTP 401
    and any other leftover exceptions to raise HTTP 500.

    :param func: The pyramid view function
    :return:
    """

    def request_wrapper(request: Request):
        try:
            return func(request)
        except HTTPError as e:
            return e
        except (AuthenticationError, Unauthorized) as e:
            log.info(e.__class__.__name__, exc_info=True)
            return get_http_error(401, e.__class__.__name__, str(e))
        except Forbidden as e:
            log.info(e.__class__.__name__, exc_info=True)
            return get_http_error(403, e.__class__.__name__, str(e))
        except Exception:
            log.info("ServerError", exc_info=True)
            raise get_http_500_error()

    return request_wrapper


def authorized_users_only(func):
    """
    Raise an AuthenticationError if no user is detected and anonymous access is disabled.

    :param func:  The pyramid view function
    :return:
    """

    def request_wrapper(request: Request):
        if is_user_allowed(request):
            return func(request)
        raise AuthenticationError

    return request_wrapper


@cw_view_config(route_name=ApiRoutes.schema, request_method="GET")
@view_exception_handler
@authorized_users_only
def schema_route(request: Request):
    """
    Returns this instance's Schema
    """
    repo = get_cw_repo(request)
    exporter = JSONSchemaExporter()
    exported_schema = exporter.export_as_dict(repo.schema)
    return exported_schema


@cw_view_config(route_name=ApiRoutes.rql)
@view_exception_handler
@authorized_users_only
def rql_route(request: Request):
    """
    Executes the given rql query
    """
    request_params = request.openapi_validated.body
    query: str = request_params["query"]
    params: dict = request_params["params"]
    try:
        result = get_cw_request(request).execute(query, params)
    except (RQLException, QueryError, ValidationError, UnknownType) as e:
        log.info(e.__class__.__name__, exc_info=True)
        raise get_http_error(400, e.__class__.__name__, str(e))
    else:
        return result.rows


@cw_view_config(route_name=ApiRoutes.login)
@view_exception_handler
def login_route(request: Request):
    """
    Tries to log in the user
    """
    request_params = request.openapi_validated.body
    login: str = request_params["login"]
    pwd: str = request_params["password"]

    repo = get_cw_repo(request)
    with repo.internal_cnx() as cnx:
        try:
            cwuser = repo.authenticate_user(cnx, login, password=pwd)
        except AuthenticationError:
            raise get_http_error(
                401, "AuthenticationFailure", "Login and/or password invalid."
            )
        else:
            headers = request.authentication_policy.remember(
                request,
                cwuser.eid,
                login=cwuser.login,
                firstname=cwuser.firstname,
                lastname=cwuser.surname,
            )
            return Response(headers=headers, status=204)


@cw_view_config(route_name=ApiRoutes.transaction_begin)
@view_exception_handler
@authorized_users_only
def transaction_begin_route(request: Request):
    """
    Starts a new transaction
    """
    transactions = get_cw_repo(request).api_transactions
    user = get_cw_request(request).user
    return transactions.begin_transaction(user)


@cw_view_config(route_name=ApiRoutes.transaction_execute)
@view_exception_handler
@authorized_users_only
def transaction_execute_route(request: Request):
    """
    Executes the given rql query as part of a transaction
    """
    transactions = get_cw_repo(request).api_transactions
    request_params = request.openapi_validated.body
    uuid: str = request_params["uuid"]
    query: str = request_params["query"]
    params: dict = request_params["params"]
    try:
        result = transactions[uuid].execute(query, params)
    except (RQLException, QueryError, ValidationError, UnknownType) as e:
        log.info(e.__class__.__name__, exc_info=True)
        raise get_http_error(400, e.__class__.__name__, str(e))
    else:
        return result.rows


@cw_view_config(route_name=ApiRoutes.transaction_commit)
@view_exception_handler
@authorized_users_only
def transaction_commit_route(request: Request):
    """
    Commits a transaction
    """
    transactions = get_cw_repo(request).api_transactions
    request_params = request.openapi_validated.body
    uuid: str = request_params["uuid"]
    try:
        commit_result = transactions[uuid].commit()
    except (RQLException, QueryError, ValidationError, UnknownType) as e:
        log.info(e.__class__.__name__, exc_info=True)
        raise get_http_error(400, e.__class__.__name__, str(e))
    else:
        transactions[uuid].rollback()
        return commit_result


@cw_view_config(route_name=ApiRoutes.transaction_rollback)
@view_exception_handler
@authorized_users_only
def transaction_rollback_route(request: Request):
    """
    Rollback a transaction
    """
    transactions = get_cw_repo(request).api_transactions
    request_params = request.openapi_validated.body
    uuid: str = request_params["uuid"]
    rollback_result = transactions[uuid].rollback()
    transactions.end_transaction(uuid)
    return rollback_result


def includeme(config: Configurator):
    setup_jwt(config)
    repo = get_cw_repo(config)
    repo.api_transactions = ApiTransactionsRepository(repo)
    route_prefix = get_api_path_prefix(config)
    register_openapi_routes(config, route_prefix)
    config.pyramid_openapi3_register_routes()
    config.scan()
