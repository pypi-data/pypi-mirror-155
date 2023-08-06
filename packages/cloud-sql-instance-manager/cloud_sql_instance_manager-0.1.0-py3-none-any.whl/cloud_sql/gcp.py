from typing import Optional

import google
from googleapiclient import discovery

from cloud_sql.instances import Instance, Site


def get_credentials_and_project():
    return google.auth.default()


def get_google_service(credentials):
    return discovery.build('sqladmin', 'v1beta4')


def obtain_instances(site: Site, override_project: Optional[str]):
    credentials, project = get_credentials_and_project()
    service = get_google_service(credentials)
    if override_project:
        project = override_project
    req = service.instances().list(project=project)
    resp = req.execute()
    instances = [Instance(item.get("name"), item.get("region"), item.get("project"), item.get("connectionName"))
                 for item in resp.get("items") if item.get("instanceType") == 'CLOUD_SQL_INSTANCE']
    for instance in instances:
        site.update(instance)
    site.set_up_nicknames()
