import json
from typing import Dict, Optional, List

import jsonpickle


class InstanceNotFoundError(Exception):
    pass


class DuplicateInstanceError(Exception):
    pass


class Instance(object):
    def __init__(self, name: str, region: str, project: str, connection_name: str):
        self.port = None
        self.iam = False
        self.default = False
        self.name = name
        self.shortname = name[:name.find("-instance-")]
        self.region = region
        self.project = project
        self.connection_name = connection_name

    def __repr__(self):  # pragma: no cover
        return json.dumps(self.__dict__)

    def assign_port(self, port: int):
        self.port = port

    def print(self, pid: Optional[int]) -> str:
        if not pid:
            return f'Project: {self.project}, Nick: {self.shortname}, Port {self.port or "N/A"}, Name: {self.name}, Region: {self.region}, IAM Enabled: {self.iam}, Default: {self.default}'
        else:
            return f'Pid: {pid}, Project: {self.project}, Nick: {self.shortname}, Port {self.port or "N/A"}, Name: {self.name}, Region: {self.region}, IAM Enabled: {self.iam}, Default: {self.default}'

    def set_iam(self, iam: bool):
        self.iam = iam

    def set_default(self, default: bool):
        self.default = default

    def check(self):
        if not hasattr(self, 'default'):
            self.default = False


class Site(object):
    def __init__(self, instances: Dict[str, Instance]):
        self.nicknames = {}
        self.instances = instances
        self.nextPort = 0
        ports = [instance.port for instance in instances.values() if instance.port is not None]
        ports.insert(0, 5433)
        self.nextPort = max(ports) + 1

    def __repr__(self):  # pragma: no cover
        return jsonpickle.encode(self)

    def set_up_nicknames(self):
        self.nicknames = {}
        for instance in self.instances.values():
            if instance.shortname in self.nicknames.keys():
                if instance not in self.nicknames[instance.shortname]:
                    self.nicknames[instance.shortname].append(instance)
            else:
                self.nicknames[instance.shortname] = [instance]

    def update(self, instance: Instance):
        if instance.connection_name not in self.instances.keys():
            if instance.port is None:
                instance.port = self.nextPort
                self.nextPort += 1
            self.instances[instance.connection_name] = instance

    def print_list(self, project: Optional[str]) -> List[str]:
        return [instance.print(None) for instance in
                sorted(self.instances.values(), key=lambda instance: f'{instance.project}{instance.shortname}')
                if (not project) or (instance.project == project)]

    def get_instance_by_nick_name(self, name, project) -> Optional[Instance]:

        if name not in self.nicknames:
            raise InstanceNotFoundError("No instance found with that nickname")

        possibles = self.nicknames[name]

        if project:
            possibles = [possible for possible in possibles if possible.project == project]

        if not possibles:
            raise InstanceNotFoundError("No instance found with that nickname for that project")
        else:
            if len(possibles) == 1:
                return possibles[0]
            else:
                raise DuplicateInstanceError(
                    "More than one instance with that nick - specify a project, or change the nickname"
                )

    def get_default_instances(self, project) -> List[Instance]:
        return [instance for instance in self.instances.values() if
                (not project or instance.project == project) and instance.default]

    def check(self):
        for instance in self.instances.values():
            instance.check()
