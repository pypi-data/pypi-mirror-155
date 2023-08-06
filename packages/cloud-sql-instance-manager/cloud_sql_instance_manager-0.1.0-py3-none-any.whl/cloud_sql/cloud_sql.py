import sys
from typing import Dict, Optional

from cloud_sql.gcp import obtain_instances
from cloud_sql.cloudsqlproxy import run_cloud_sql_proxy, stop_cloud_sql_proxy, check_if_proxy_is_running
from cloud_sql.commandline import get_parameters
from cloud_sql.config import Configuration
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


def execute_command(parameters: Dict[str, str], config: Configuration, site: Site, running_instances: RunningInstances):
    command = parameters['command']

    if command == 'list':
        lines = site.print_list(parameters['project'])
        for line in lines:
            print(line)

    elif command == 'list-running':
        running = running_instances.get_all_running()
        for connection_name in running.keys():
            instance = site.instances[connection_name]
            print(instance.print(running[connection_name]))
        if len(running) == 0:
            print("No running instances")

    elif command == 'start':
        instance = get_instance_from_nick(site, parameters['name'], parameters['project'])
        if instance:
            if running_instances.get_running(instance.connection_name):
                print(f"{instance.shortname} is already running.")
            else:
                pid = run_cloud_sql_proxy(config.cloud_sql_path, instance.connection_name, instance.port, instance.iam)
                running_instances.add_running(pid, instance.connection_name)
                print(f"Started {instance.name} on port {instance.port}")

    elif command == 'stop':
        instance = get_instance_from_nick(site, parameters['name'], parameters['project'])
        if instance:
            pid = running_instances.get_running(instance.connection_name)
            if pid:
                if stop_cloud_sql_proxy(pid, instance.connection_name):
                    print(f"Stopped {instance.name} on port {instance.port}")
                else:
                    print("Could not locate process to stop, it has been removed from the running list")
                running_instances.remove_running(instance.connection_name)
            else:
                print(f"{instance.shortname} is not running")

    elif command == 'update':
        instance = get_instance_from_nick(site, parameters['name'], parameters['project'])
        if instance:

            new_iam = parameters['iam']
            if new_iam:
                instance.set_iam(new_iam == 'true')

            new_nick = parameters['nick']
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
            print('Instance updated:')
            print(instance.print(None))

    elif command == 'import':
        prev_instances = len(site.instances);
        obtain_instances(site, parameters['project'])
        print(f"Imported {len(site.instances) - prev_instances} instances.")

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
