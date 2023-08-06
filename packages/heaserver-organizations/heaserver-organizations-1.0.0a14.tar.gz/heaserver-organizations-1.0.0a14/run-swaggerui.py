#!/usr/bin/env python3

from heaserver.organization import service
from heaserver.service.testcase import swaggerui
from heaserver.service.testcase.testenv import DockerContainerConfig, DockerVolumeMapping
from heaserver.service.wstl import builder_factory
from heaserver.service.db.mongo import MongoManager
from integrationtests.heaserver.organizationintegrationtest.testcase import db_store
from aiohttp.web import get, put, post, delete, view
from heaobject.registry import Resource
from heaobject.volume import AWSFileSystem
from heaobject.person import Person
from heaobject.account import AWSAccount
from pathlib import Path
import logging
from copy import deepcopy
import argparse

logging.basicConfig(level=logging.DEBUG)

HEASERVER_REGISTRY_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-registry:1.0.0a24'
HEASERVER_VOLUMES_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-volumes:1.0.0a10'
HEASERVER_PEOPLE_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-people:1.0.0a3'
HEASERVER_ACCOUNTS_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-accounts:1.0.0a9'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Runs SwaggerUI with an optional AWS account id to add to organization 666f6f2d6261722d71757578.')
    parser.add_argument('-a', '--account', nargs='?', help='the AWS account id to add')
    args = parser.parse_args()
    db_store_ = deepcopy(db_store)
    aws_account = args.account
    if aws_account is not None:
        my_org = next(org for org in db_store_.get('organizations', []) if org['id'] == '666f6f2d6261722d71757578')
        if my_org is not None:
            my_org.setdefault('aws_account_ids', []).append(aws_account)
            print(f'Added AWS account id {aws_account} to organization 666f6f2d6261722d71757578.')
    swaggerui.run(project_slug='heaserver-organizations', desktop_objects=db_store_,
                  wstl_builder_factory=builder_factory(service.__package__), routes=[
            (get, '/organizations/{id}', service.get_organization),
            (get, '/organizations/byname/{name}', service.get_organization_by_name),
            (get, '/organizations/', service.get_all_organizations),
            (put, '/organizations/{id}', service.put_organization),
            (post, '/organizations/', service.post_organization),
            (delete, '/organizations/{id}', service.delete_organization),
            (get, '/organizations/{id}/members', service.get_organization_members),
            (view, '/organizations/{id}/opener', service.get_organization_opener),
            (get, '/organizations/{id}/awsaccounts/', service.get_organization_aws_accounts)
        ], registry_docker_image=HEASERVER_REGISTRY_IMAGE,
                  other_microservice_images=[DockerContainerConfig(image=HEASERVER_VOLUMES_IMAGE,
                                                                   port=8080,
                                                                   check_path='/volumes',
                                                                   db_manager_cls=MongoManager,
                                                                   resources=[
                                                                       Resource(
                                                                           resource_type_name='heaobject.volume.Volume',
                                                                           base_path='/volumes/'),
                                                                       Resource(
                                                                           resource_type_name='heaobject.volume.FileSystem',
                                                                           base_path='/filesystems')
                                                                   ]),
                                             DockerContainerConfig(image=HEASERVER_PEOPLE_IMAGE,
                                                                   port=8080,
                                                                   check_path='/ping',
                                                                   db_manager_cls=MongoManager,
                                                                   resources=[Resource(
                                                                       resource_type_name=Person.get_type_name(),
                                                                       base_path='/people')]),
                                             DockerContainerConfig(image=HEASERVER_ACCOUNTS_IMAGE,
                                                                   port=8080,
                                                                   check_path='/ping',
                                                                   db_manager_cls=MongoManager,  # Change to S3Manager for heaserver-accounts version 1.0.0a10 or greater.
                                                                   resources=[Resource(
                                                                       resource_type_name=AWSAccount.get_type_name(),
                                                                       file_system_type=AWSFileSystem.get_type_name(),
                                                                       base_path='/awsaccounts')],
                                                                   volumes=[DockerVolumeMapping(
                                                                       host=str(Path.home() / '.aws'),
                                                                       container='/home/app/.aws')])]
                  )
