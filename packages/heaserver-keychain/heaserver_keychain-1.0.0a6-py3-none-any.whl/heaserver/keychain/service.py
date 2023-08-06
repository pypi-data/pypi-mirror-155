"""
The HEA Keychain provides ...
"""

from heaserver.service import response, appproperty
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import mongo, mongoservicelib
from heaserver.service.wstl import builder_factory, action
from heaobject.keychain import Credentials
import logging
import copy

_logger = logging.getLogger(__name__)
MONGODB_CREDENTIALS_COLLECTION = 'credentials'


@routes.get('/credentials/{id}')
@action('heaserver-keychain-credentials-get-properties', rel='properties')
@action('heaserver-keychain-credentials-open', rel='opener', path='/credentials/{id}/opener')
@action('heaserver-keychain-credentials-duplicate', rel='duplicator', path='/credentials/{id}/duplicator')
async def get_credentials(request: web.Request) -> web.Response:
    """
    Gets the credentials with the specified id.

    :param request: the HTTP request.
    :return: the requested credentials or Not Found.
    ---
    summary: A specific credentials.
    tags:
        - heaserver-keychain-get-credentials
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    _logger.debug('Requested credentials by id %s' % request.match_info["id"])
    return await mongoservicelib.get(request, MONGODB_CREDENTIALS_COLLECTION)


@routes.get('/credentials/byname/{name}')
async def get_credentials_by_name(request: web.Request) -> web.Response:
    """
    Gets the credentials with the specified name.

    :param request: the HTTP request.
    :return: the requested credentials or Not Found.
    ---
    summary: Specific credentials queried by name.
    tags:
        - heaserver-keychain-get-credentials-by-name
    parameters:
        - $ref: '#/components/parameters/name'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.get_by_name(request, MONGODB_CREDENTIALS_COLLECTION)


@routes.get('/credentials')
@routes.get('/credentials/')
@action('heaserver-keychain-credentials-get-properties', rel='properties')
@action('heaserver-keychain-credentials-open', rel='opener', path='/credentials/{id}/opener')
@action('heaserver-keychain-credentials-duplicate', rel='duplicator', path='/credentials/{id}/duplicator')
async def get_all_credentials(request: web.Request) -> web.Response:
    """
    Gets all credentials.

    :param request: the HTTP request.
    :return: all credentials.

    ---
    summary: All credentials.
    tags:
        - heaserver-keychain-get-all-credentials
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    return await mongoservicelib.get_all(request, MONGODB_CREDENTIALS_COLLECTION)


@routes.get('/credentials/{id}/duplicator')
@action(name='heaserver-keychain-credentials-duplicate-form')
async def get_credentials_duplicate_form(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested credentials.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested credentials was not found.
    """
    return await mongoservicelib.get(request, MONGODB_CREDENTIALS_COLLECTION)


@routes.post('/credentials/duplicator')
async def post_credentials_duplicator(request: web.Request) -> web.Response:
    """
    Posts the provided credentials for duplication.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    """
    return await mongoservicelib.post(request, MONGODB_CREDENTIALS_COLLECTION, Credentials)


@routes.post('/credentials')
@routes.post('/credentials/')
async def post_credentials(request: web.Request) -> web.Response:
    """
    Posts the provided credentials.

    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the Location header.
    ---
    summary: Credentials creation
    tags:
        - heaserver-keychain-post-credentials
    requestBody:
      description: A new credentials object.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: Credentials
              value: {
                "template": {
                  "data": [
                    {
                      "name": "created",
                      "value": null,
                      "prompt": "created",
                      "display": true
                    },
                    {
                      "name": "derived_by",
                      "value": null,
                      "prompt": "derived_by",
                      "display": true
                    },
                    {
                      "name": "derived_from",
                      "value": [],
                      "prompt": "derived_from",
                      "display": true
                    },
                    {
                      "name": "description",
                      "value": null,
                      "prompt": "description",
                      "display": true
                    },
                    {
                      "name": "display_name",
                      "value": "Joe",
                      "prompt": "display_name",
                      "display": true
                    },
                    {
                      "name": "invited",
                      "value": [],
                      "prompt": "invited",
                      "display": true
                    },
                    {
                      "name": "modified",
                      "value": null,
                      "prompt": "modified",
                      "display": true
                    },
                    {
                      "name": "name",
                      "value": "joe",
                      "prompt": "name",
                      "display": true
                    },
                    {
                      "name": "owner",
                      "value": "system|none",
                      "prompt": "owner",
                      "display": true
                    },
                    {
                      "name": "shares",
                      "value": [],
                      "prompt": "shares",
                      "display": true
                    },
                    {
                      "name": "source",
                      "value": null,
                      "prompt": "source",
                      "display": true
                    },
                    {
                      "name": "version",
                      "value": null,
                      "prompt": "version",
                      "display": true
                    }
                  ]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: Credentials
              value: {
                "created": null,
                "derived_by": null,
                "derived_from": [],
                "description": null,
                "display_name": "Joe",
                "invited": [],
                "modified": null,
                "name": "joe",
                "owner": "system|none",
                "shares": [],
                "source": null,
                "type": "heaobject.keychain.Credentials",
                "version": null
              }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.post(request, MONGODB_CREDENTIALS_COLLECTION, Credentials)


@routes.put('/credentials/{id}')
async def put_credentials(request: web.Request) -> web.Response:
    """
    Updates the credentials with the specified id.
    :param request: the HTTP request.
    :return: a Response object with a status of No Content or Not Found.
    ---
    summary: Credentials updates
    tags:
        - heaserver-keychain-put-credentials
    parameters:
        - $ref: '#/components/parameters/id'
    requestBody:
      description: An updated credentials object.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: Credentials
              value: {
                "template": {
                  "data": [
                    {
                      "name": "created",
                      "value": null
                    },
                    {
                      "name": "derived_by",
                      "value": null
                    },
                    {
                      "name": "derived_from",
                      "value": []
                    },
                    {
                      "name": "description",
                      "value": null
                    },
                    {
                      "name": "display_name",
                      "value": "Reximus Max"
                    },
                    {
                      "name": "invited",
                      "value": []
                    },
                    {
                      "name": "modified",
                      "value": null
                    },
                    {
                      "name": "owner",
                      "value": "system|none"
                    },
                    {
                      "name": "shares",
                      "value": []
                    },
                    {
                      "name": "source",
                      "value": null
                    },
                    {
                      "name": "version",
                      "value": null
                    },
                    {
                      "name": "id",
                      "value": "666f6f2d6261722d71757578"
                    }
                  ]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: An updated credentials object
              value: {
                "created": None,
                "derived_by": None,
                "derived_from": [],
                "description": None,
                "display_name": "Reximus Max",
                "invited": [],
                "modified": None,
                "owner": NONE_USER,
                "shares": [],
                "source": None,
                "type": "heaobject.keychain.Credentials",
                "version": None,
                "id": "666f6f2d6261722d71757578"
              }
    responses:
      '204':
        $ref: '#/components/responses/204'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.put(request, MONGODB_CREDENTIALS_COLLECTION, Credentials)


@routes.delete('/credentials/{id}')
async def delete_credentials(request: web.Request) -> web.Response:
    """
    Deletes the credentials with the specified id.
    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Credentials deletion
    tags:
        - heaserver-keychain-delete-credentials
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.delete(request, MONGODB_CREDENTIALS_COLLECTION)


def main() -> None:
    config = init_cmd_line(description='a service for managing laboratory/user credentials',
                           default_port=8080)
    start(db=mongo.MongoManager, wstl_builder_factory=builder_factory(__package__), config=config)
