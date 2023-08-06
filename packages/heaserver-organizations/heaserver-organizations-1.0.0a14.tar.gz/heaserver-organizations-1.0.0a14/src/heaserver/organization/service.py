"""
The HEA Server Organization provides ...
"""
import asyncio

from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import mongo, mongoservicelib
from heaserver.service.wstl import builder_factory, action
from heaserver.service.appproperty import HEA_DB
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.heaobjectsupport import type_to_resource_url
from heaserver.service import response, client
from heaobject.organization import Organization
from heaobject.account import AWSAccount
from heaobject.volume import AWSFileSystem, Volume
from heaobject.person import Person
from yarl import URL
from asyncio import gather
from typing import Optional, Dict
import logging

_logger = logging.getLogger(__name__)

MONGODB_ORGANIZATION_COLLECTION = 'organizations'


@routes.get('/organizations/{id}')
@action('heaserver-organizations-organization-get-properties', rel='properties')
@action('heaserver-organizations-organization-get-open-choices', rel='hea-opener-choices', path='/organizations/{id}/opener')
@action('heaserver-organizations-organization-duplicate', rel='duplicator', path='/organizations/{id}/duplicator')
async def get_organization(request: web.Request) -> web.Response:
    """
    Gets the organization with the specified id.
    :param request: the HTTP request.
    :return: the requested organization or Not Found.
    ---
    summary: A specific organization.
    tags:
        - heaserver-organizations-get-organization
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    #todo 'user = request.headers.get(SUB)' need find if lab belongs to user or they apart of
    #todo not sure if at this point we initalize the session for aws
    _logger.debug('Requested organization by id %s', request.match_info["id"])
    return await mongoservicelib.get(request, MONGODB_ORGANIZATION_COLLECTION)


@routes.get('/organizations/byname/{name}')
async def get_organization_by_name(request: web.Request) -> web.Response:
    """
    Gets the organization with the specified id.
    :param request: the HTTP request.
    :return: the requested organization or Not Found.
    ---
    summary: A specific organization, by name.
    tags:
        - heaserver-organizations-get-organization-by-name
    parameters:
        - $ref: '#/components/parameters/name'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.get_by_name(request, MONGODB_ORGANIZATION_COLLECTION)


@routes.get('/organizations')
@routes.get('/organizations/')
@action('heaserver-organizations-organization-get-properties', rel='properties')
@action('heaserver-organizations-organization-get-open-choices', rel='hea-opener-choices', path='/organizations/{id}/opener')
@action('heaserver-organizations-organization-duplicate', rel='duplicator', path='/organizations/{id}/duplicator')
async def get_all_organizations(request: web.Request) -> web.Response:
    """
    Gets all organizations.
    :param request: the HTTP request.
    :return: all organizations.
    ---
    summary: All organizations.
    tags:
        - heaserver-organizations-get-all-organizations
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    return await mongoservicelib.get_all(request, MONGODB_ORGANIZATION_COLLECTION)


@routes.get('/organizations/{id}/duplicator')
@action(name='heaserver-organizations-organization-duplicate-form', path='/organizations/{id}')
async def get_organization_duplicate_form(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested organization.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested organization was not found.
    """
    return await mongoservicelib.get(request, MONGODB_ORGANIZATION_COLLECTION)


@routes.post('/organizations/duplicator')
async def post_organization_duplicator(request: web.Request) -> web.Response:
    """
    Posts the provided organization for duplication.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    """
    return await mongoservicelib.post(request, MONGODB_ORGANIZATION_COLLECTION, Organization)


@routes.post('/organizations')
@routes.post('/organizations/')
async def post_organization(request: web.Request) -> web.Response:
    """
    Posts the provided organization.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the Location header.
    ---
    summary: Organization creation
    tags:
        - heaserver-organizations-post-organization
    requestBody:
      description: A new organization object.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: Organization example
              value: {
                "template": {
                  "data": [{
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
                    "value": "Joe"
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
                    "name": "name",
                    "value": "joe"
                  },
                  {
                    "name": "owner",
                    "value": "system|none"
                  },
                  {
                    "name": "shared_with",
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
                    "name": "aws_account_ids",
                    "value": ["1234", "5678"]
                  },
                  {
                    "name": "principal_investigator_id",
                    "value": "1",
                  },
                  {
                    "name": "manager_ids",
                    "value": ["4321", "8765"]
                  },
                  {
                    "name": "member_ids",
                    "value": ["1", "2"]
                  }]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: Organization example
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
                "shared_with": [],
                "source": null,
                "type": "heaobject.registry.Component",
                "version": null,
                "aws_account_ids": ["1234", "5678"],
                "principal_investigator_id": "1",
                "manager_ids": ["4321", "8765"],
                "member_ids": ["1", "2"]
              }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.post(request, MONGODB_ORGANIZATION_COLLECTION, Organization)


@routes.put('/organizations/{id}')
async def put_organization(request: web.Request) -> web.Response:
    """
    Updates the organization with the specified id.
    :param request: the HTTP request.
    :return: a Response object with a status of No Content or Not Found.
     ---
    summary: Organization updates
    tags:
        - heaserver-organizations-put-organization
    parameters:
        - $ref: '#/components/parameters/id'
    requestBody:
      description: An updated organization object.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: Organization example
              value: {
                "template": {
                  "data": [{
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
                    "name": "name",
                    "value": "reximus"
                  },
                  {
                    "name": "owner",
                    "value": "system|none"
                  },
                  {
                    "name": "shared_with",
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
                    "name": "aws_account_ids",
                    "value": ["1234", "5678"]
                  },
                  {
                    "name": "principal_investigator_id",
                    "value": "1",
                  },
                  {
                    "name": "manager_ids",
                    "value": ["4321", "8765"]
                  },
                  {
                    "name": "member_ids",
                    "value": ["1", "2"]
                  },
                  {
                  "name": "id",
                  "value": "666f6f2d6261722d71757578"
                  }]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: Organization example
              value: {
                "id": "666f6f2d6261722d71757578",
                "created": null,
                "derived_by": null,
                "derived_from": [],
                "description": null,
                "display_name": "Reximus Max",
                "invited": [],
                "modified": null,
                "name": "reximus",
                "owner": "system|none",
                "shared_with": [],
                "source": null,
                "type": "heaobject.registry.Component",
                "version": null,
                "aws_account_ids": ["1234", "5678"],
                "principal_investigator_id": "1",
                "manager_ids": ["4321", "8765"],
                "member_ids": ["1", "2"]
              }
    responses:
      '204':
        $ref: '#/components/responses/204'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.put(request, MONGODB_ORGANIZATION_COLLECTION, Organization)


@routes.delete('/organizations/{id}')
async def delete_organization(request: web.Request) -> web.Response:
    """
    Deletes the organization with the specified id.
    :param request: the HTTP request.
    :return: A Response object with a status of No Content or Not Found.
    ---
    summary: Organization deletion
    tags:
        - heaserver-organizations-delete-organization
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.delete(request, MONGODB_ORGANIZATION_COLLECTION)


@routes.get('/organizations/{id}/opener')
@action('heaserver-organizations-organization-open-aws-accounts', rel=f'hea-opener hea-context-aws hea-default {AWSAccount.get_mime_type()}', path='/organizations/{id}/awsaccounts')
async def get_organization_opener(request: web.Request) -> web.Response:
    """

    :param request: the HTTP Request.
    :return: A Response object with a status of Multiple Choices or Not Found.
    ---
    summary: Organization opener choices
    tags:
        - heaserver-organizations-organization-get-open-choices
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.opener(request, MONGODB_ORGANIZATION_COLLECTION)


@routes.get('/organizations/{id}/awsaccounts')
@routes.get('/organizations/{id}/awsaccounts/')
@action('heaserver-organizations-aws-account-get-open-choices', rel='hea-opener-choices', path='/awsaccounts/{id}/opener')
async def get_organization_aws_accounts(request: web.Request) -> web.Response:
    """

    :param request: the HTTP Request.
    :return: a Response object with a status code of 200.
    ---
    summary: An organization's AWS accounts.
    tags:
        - heaserver-organizations-organization-get-aws-accounts
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    org_dict = await request.app[HEA_DB].get(request, MONGODB_ORGANIZATION_COLLECTION, var_parts='id')
    if org_dict is None:
        return response.status_not_found()
    org = Organization()
    org.from_dict(org_dict)
    headers = {SUB: request.headers.get(SUB, '')} if SUB in request.headers else None

    volume_url = await type_to_resource_url(request, Volume)
    if volume_url is None:
        raise ValueError('No Volume service registered')
    get_volumes_url = URL(volume_url) / 'byfilesystemtype' / AWSFileSystem.get_type_name()

    aws_account_url = await type_to_resource_url(request, AWSAccount, file_system_type_or_type_name=AWSFileSystem)
    if aws_account_url is None:
        raise ValueError('No AWSAccount service registered')

    async def get_one(volume_id):
        return await client.get(request.app, URL(aws_account_url) / volume_id / 'awsaccounts' / 'me', AWSAccount, headers=headers)

    result = [a.to_dict() for a in await gather(*[get_one(v.id) async for v in client.get_all(request.app, get_volumes_url, Volume, headers=headers)]) if a is not None and a.id in org.aws_account_ids]
    return await response.get_all(request, result)


@routes.get('/organizations/{id}/members')
@routes.get('/organizations/{id}/members/')
# @action('heaserver-organizations-members-get-open-choices', rel='hea-opener-choices', path='/people/{id}/opener')
async def get_organization_members(request: web.Request) -> web.Response:
    """
    Gets the S3 buckets in the provided account.

    :param request: the HTTP Request.
    :return: a Response object with status code 200 and a body containing either an empty list or a list of buckets.
    ---
    summary: the buckets in an AWS account.
    tags:
        - heaserver-get-members
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
        '200':
            $ref: '#/components/responses/200'
    """
    headers = {SUB: request.headers.get(SUB, '')} if SUB in request.headers else None

    org_dict = await request.app[HEA_DB].get(request, MONGODB_ORGANIZATION_COLLECTION, var_parts='id')
    if org_dict is None:
        return response.status_not_found()
    org = Organization()
    org.from_dict(org_dict)
    org_members = org.manager_ids + org.member_ids

    url = URL(await type_to_resource_url(request=request, type_or_type_name=Person))

    def get_one_member_dict(m):
        _logger.info("People names  %s returning" % m.display_name)
        return m.to_dict()

    people_dictionaries = [get_one_member_dict(p_obj) for p_obj in await gather(
        *[client.get(app=request.app, url=url / m_id, type_or_obj=Person, headers=headers) for m_id in org_members])]

    return await response.get_all(request, people_dictionaries)


def main() -> None:
    config = init_cmd_line(description='a service for managing organization information for research laboratories and other research groups',
                           default_port=8087)
    start(db=mongo.MongoManager, wstl_builder_factory=builder_factory(__package__), config=config)
