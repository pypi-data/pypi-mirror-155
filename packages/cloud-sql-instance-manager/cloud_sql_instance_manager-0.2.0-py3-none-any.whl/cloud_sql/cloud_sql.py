import sys
from typing import Dict, Optional

from cloud_sql.gcp import obtain_instances
from cloud_sql.cloudsqlproxy import run_cloud_sql_proxy, stop_cloud_sql_proxy, check_if_proxy_is_running
from cloud_sql.commandline import get_parameters
from cloud_sql.config import Configuration, PathNotFoundError
from cloud_sql.instances import Site, InstanceNotFoundError, DuplicateInstanceError, Instance
from cloud_sql.persistence import save_site, load_site, load_config, save_config, load_running, save_running
from cloud_sql.running_instances import RunningInstances


def refresh_running(running_instances: RunningInstances):
    running = running_instances.get_all_running()
    old_running = list(running.items())
    for (connection_name, pid) in old_running:
        if not check_if_proxy_is_running(pid, connection_name):
            running_instances.remove_running(connection_name)


def get_instance_from_nick(site: Site, nick: str, project: Optional[str]) -> Optional[Instance]:
    try:
        return site.get_instance_by_nick_name(nick, project)
    except (InstanceNotFoundError, DuplicateInstanceError) as err:
        print(err)
        return None


def print_list(site: Site, project: Optional[str]):
    lines = site.print_list(project)
    for line in lines:
        print(line)


def print_list_running(site: Site, running_instances: RunningInstances):
    running = running_instances.get_all_running()
    for connection_name in running.keys():
        instance = site.instances[connection_name]
        print(instance.print(running[connection_name]))
    if len(running) == 0:
        print("No running instances")


def start(config: Configuration, site: Site, running_instances: RunningInstances, name: str, project: Optional[str]):
    if name == 'default':
        instances = site.get_default_instances(project)
        if len(instances) == 0:
            print("No default instances found")
    else:
        instances = [get_instance_from_nick(site, name, project)]
    for instance in instances:
        if running_instances.get_running(instance.connection_name):
            print(f"{instance.shortname} is already running.")
        else:
            pid = run_cloud_sql_proxy(config.cloud_sql_path, instance.connection_name, instance.port, instance.iam)
            running_instances.add_running(pid, instance.connection_name)
            print(f"Started {instance.name} on port {instance.port}")


def stop(site: Site, running_instances: RunningInstances, nickname: str, project: Optional[str]):
    if nickname == 'all':
        instances = [site.instances[name] for name in running_instances.instances.keys() if
                     (not project or project == site.instances[name].project)]
        if len(instances) == 0:
            print("No running instances found")
    else:
        instances = [get_instance_from_nick(site, nickname, project)]

    for instance in instances:
        pid = running_instances.get_running(instance.connection_name)
        if pid:
            if stop_cloud_sql_proxy(pid, instance.connection_name):
                print(f"Stopped {instance.name} on port {instance.port}")
            else:
                print(
                    f'Could not locate process to stop for {instance.shortname}, it has been removed from the running list')
            running_instances.remove_running(instance.connection_name)
        else:
            print(f"{instance.shortname} is not running")


def import_instances(site: Site, project: Optional[str]):
    prev_instances = len(site.instances);
    obtain_instances(site, project)
    print(f"Imported {len(site.instances) - prev_instances} instances.")


def update(site: Site, name: str, project: Optional[str], new_iam: Optional[str], new_nick: Optional[str],
           new_default: Optional[str]):
    instance = get_instance_from_nick(site, name, project)
    if instance:

        if new_iam:
            instance.set_iam(new_iam.lower() == 'true')

        if new_nick:
            try:
                other_instance = site.get_instance_by_nick_name(new_nick, instance.project)
            except (InstanceNotFoundError, DuplicateInstanceError):
                other_instance = None
            if other_instance:
                print('That nick would not be unique, pick another.')
            else:
                instance.shortname = new_nick
                site.set_up_nicknames()

        if new_default:
            instance.set_default(new_default.lower() == 'true')

        print('Instance updated:')
        print(instance.print(None))


def update_config(config: Configuration, new_path: Optional[str]):
    if new_path:
        try:
            config.new_path(new_path)
            print(f"Updated cloud_sql_proxy path to {new_path}")
        except PathNotFoundError:
            print("That file appears not to exist. It needs to be the fully qualified path.")
    else:
        print("Provide the location of the cloud_sql_proxy executable as parameter --path")


def execute_command(parameters: Dict[str, str], config: Configuration, site: Site, running_instances: RunningInstances):
    command = parameters['command']

    if command == 'list':
        print_list(site, parameters['project'])

    elif command == 'list-running':
        print_list_running(site, running_instances)

    elif command == 'start':
        start(config, site, running_instances, parameters['name'], parameters['project'])

    elif command == 'stop':
        stop(site, running_instances, parameters['name'], parameters['project'])

    elif command == 'update':
        update(site, parameters['name'], parameters['project'], parameters['iam'], parameters['nick'],
               parameters['default'])

    elif command == 'import':
        import_instances(site, parameters['project'])

    elif command == 'config':
        update_config(config, parameters['path'])

    else:
        print("Specify a command or ask for help with --help")


def run():
    app_config = load_config()
    app_parameters = get_parameters()
    site_info = load_site()
    running = load_running()
    refresh_running(running)
    execute_command(app_parameters, app_config, site_info, running)
    save_running(running)
    save_site(site_info)
    save_config(app_config)
    sys.exit()
