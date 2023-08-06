import jsonpickle
import os
import os.path

from cloud_sql.config import Configuration, default_configuration
from cloud_sql.instances import Site
from cloud_sql.running_instances import RunningInstances

base_path = os.path.join(os.getenv("HOME"), ".cloudsql")
instance_filename = os.path.join(base_path, "instances.json")
config_filename =  os.path.join(base_path, "config.json")
running_instances_filename = os.path.join(base_path, "running.json")


def save_site(site : Site):
    if not os.path.exists(os.path.dirname(instance_filename)):
        os.makedirs(os.path.dirname(instance_filename))

    with open(instance_filename, 'w') as f:
        f.write(jsonpickle.encode(site))


def load_site() -> Site:
    if not os.path.exists(instance_filename):
        return Site({})
    else:
        with open(instance_filename, 'r') as f:
            json_str = f.read()
            site = jsonpickle.decode(json_str)
            site.check()
            return site


def save_config(config: Configuration):
    if not os.path.exists(os.path.dirname(config_filename)):
        os.makedirs(os.path.dirname(config_filename))

    with open(config_filename, 'w') as f:
        f.write(jsonpickle.encode(config))


def load_config() -> Configuration:
    if not os.path.exists(config_filename):
        return default_configuration()
    else:
        with open(config_filename, 'r') as f:
            json_str = f.read()
            return jsonpickle.decode(json_str)


def save_running(running_instances: RunningInstances):
    if not os.path.exists(os.path.dirname(running_instances_filename)):
        os.makedirs(os.path.dirname(running_instances_filename))

    with open(running_instances_filename, 'w') as f:
        f.write(jsonpickle.encode(running_instances))


def load_running() -> RunningInstances:
    if not os.path.exists(running_instances_filename):
        return RunningInstances({})
    else:
        with open(running_instances_filename, 'r') as f:
            json_str = f.read()
            return jsonpickle.decode(json_str)
