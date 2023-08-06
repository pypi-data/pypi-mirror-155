import os
from aws import util, cluster


def create_config(config_path: str):
    """
    Creates a config object to pass to create_cluster.

    :param config_path: absolute path to your config.yaml file

    :return: a dictionary with the required config structure
    """

    config = util.read_yaml(config_path)

    # add dbPassword and resourceName to each db object
    for db in config['databases']:
        # don't require user input on automated runs (set in test.sh)
        if os.getenv('automated') == '1':
            # don't store snapshots on jenkins test runs
            db['deletePolicy'] = 'Delete'
        else:
            db['deletePolicy'] = 'Snapshot'

        if not db.get('default'):
            db['default'] = False

        # used as resource names in cfm templates
        db['resourceName'] = cluster.get_db_resource_name(db)
        db['dbPassword'] = util.generate_random_password()

    return config


def get_cfm_file(file_name: str):
    """
    Gets the content of a default cfm file so it can be copied to a new directory.

    :param file_name: the name of the file in aws/templates/cfm

    :return: The contents of the file.read()
    """
    aws_dir = os.path.abspath(os.path.dirname(__file__))
    cfm_dir = os.path.join(aws_dir, 'templates/cfm')
    file_path = os.path.join(cfm_dir, file_name)

    assert os.path.exists(file_path), f'aws/templates/cfm/{file_name} not found'

    with open(file_path) as file:
        contents = file.read()

    return contents
