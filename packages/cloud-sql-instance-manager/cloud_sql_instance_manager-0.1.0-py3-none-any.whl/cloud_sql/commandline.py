import argparse
from typing import Dict


def get_parameters() -> Dict[str, str]:
    parser = argparse.ArgumentParser(description='Cloud SQL Instance Manager',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    parser_list = subparsers.add_parser('list', help='list current instances')
    parser_list.add_argument('-p', '--project', help='project name')

    parser_list_running = subparsers.add_parser('list-running', help='list running instances')

    parser_start = subparsers.add_parser('start', help='start instance')
    parser_start.add_argument('name', help='instance name or nickname')
    parser_start.add_argument('-p', '--project', help='project name')

    parser_stop = subparsers.add_parser('stop', help='stop a running instance')
    parser_stop.add_argument('name', help='instance name or nickname')
    parser_stop.add_argument('-p', '--project', help='project name')

    parser_add = subparsers.add_parser('add', help='add a new instance')
    parser_add.add_argument('connection name', help='long connection name from gcp')
    parser_add.add_argument('-n', '--nick', help='set nickname')

    parser_import = subparsers.add_parser('import', help='import instances from gcp')
    parser_import.add_argument('-p', '--project', help='project name')

    parser_update = subparsers.add_parser('update', help='update an existing instance')
    parser_update.add_argument('name', help='nickname of connection')
    parser_update.add_argument('-p', '--project', help='specify which project name')
    parser_update.add_argument('-i', '--iam', help='set whether iam login is enabled')
    parser_update.add_argument('-n', '--nick', help='set a new nickname')

    parser_config = subparsers.add_parser('config', help='update configuration')
    parser_config.add_argument('-p', '--path', help='path to the cloud_sql_proxy executable')

    args = vars(parser.parse_args())
    return args
