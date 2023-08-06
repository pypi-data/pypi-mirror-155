import os
import shutil


class PathNotFoundError(Exception):
    pass


class Configuration(object):
    def __init__(self, cloud_sql_path):
        self.cloud_sql_path = cloud_sql_path

    def new_path(self, new_path):
        if os.path.exists(new_path):
            self.cloud_sql_path = new_path
        else:
            raise PathNotFoundError


def default_configuration():
    return Configuration(shutil.which("cloud_sql_proxy"))