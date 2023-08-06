import shutil


class Configuration(object):
    def __init__(self, cloud_sql_path):
        self.cloud_sql_path = cloud_sql_path


def default_configuration():
    return Configuration(shutil.which("cloud_sql_proxy"))