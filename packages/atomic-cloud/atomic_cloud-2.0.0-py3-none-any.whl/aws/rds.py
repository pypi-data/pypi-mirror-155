from aws import util, secret, cfm, lambda_fn
from aws.cluster import LAMBDAS_DIR, STACK_TYPES
from os import path
from aws.region import get_rds
from itertools import groupby

###########################################################################
# Database Clusters & Instances
###########################################################################

MODULE_DIR = path.abspath(path.dirname(__file__))
TEMPLATE_DIR = path.join(MODULE_DIR, 'templates')
CFM_DIR = path.join(TEMPLATE_DIR, 'cfm')


def list_db_clusters(engine: dict = None):
    """
    List of all database clusters in the environment

    :param engine: Optional engine type of the database cluster :return: `Database Cluster Details
    <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client
    .describe_db_clusters>`_

    Example Output::

        [
            {
                AllocatedStorage: 1
                AvailabilityZones: [
                    "us-east-1c"
                    "us-east-1b"
                    "us-east-1a"
                ]
                BackupRetentionPeriod: 1
                DatabaseName: ""
                DBClusterIdentifier: "database-1"
                DBClusterParameterGroup: "default.aurora5.6"
                DBSubnetGroup: "default-vpc-098ec64bb7f6e4799"
                Status: "available"
                EarliestRestorableTime: 2019-11-13 10:37:42.998000+00:00
                Endpoint: "database-1.cluster-cliglprpku2i.us-east-1.rds.amazonaws.com"
                ReaderEndpoint: "database-1.cluster-ro-cliglprpku2i.us-east-1.rds.amazonaws.com"
                MultiAZ: False
                Engine: "aurora"
                EngineVersion: "5.6.10a"
                LatestRestorableTime: 2019-11-14 20:39:01.484000+00:00
                Port: 3306
                MasterUsername: "admin"
                PreferredBackupWindow: "10:25-10:55"
                PreferredMaintenanceWindow: "mon:06:39-mon:07:09"
                ReadReplicaIdentifiers: []
                DBClusterMembers: [
                    {
                        DBInstanceIdentifier: "database-1-instance-1"
                        IsClusterWriter: True
                        DBClusterParameterGroupStatus: "pending-reboot"
                        PromotionTier: 1
                    }
                ]
                VpcSecurityGroups: [
                    {
                        VpcSecurityGroupId: "sg-0864e77f268788dd5"
                        Status: "active"
                    }
                ]
                HostedZoneId: "Z2R2ITUGPM61AM"
                StorageEncrypted: True
                KmsKeyId: "arn:aws:kms:us-east-1:683863474030:key/c7c7bfb8-3225-4da1-8724-9e06ddf0cff6"
                DbClusterResourceId: "cluster-OQ3NVZTFVRMSNVJWY6K6FNHXWE"
                DBClusterArn: "arn:aws:rds:us-east-1:683863474030:cluster:database-1"
                AssociatedRoles: []
                IAMDatabaseAuthenticationEnabled: False
                ClusterCreateTime: 2019-11-08 19:38:29.519000+00:00
                EngineMode: "provisioned"
                DeletionProtection: False
                HttpEndpointEnabled: False
                ActivityStreamStatus: "stopped"
                CopyTagsToSnapshot: True
                CrossAccountClone: False
            }
        ]

    """

    if engine is not None:
        clusters = get_rds().describe_db_clusters(Filters=[{'Name': 'engine', 'Values': [engine]}]).get('DBClusters')
    else:
        clusters = get_rds().describe_db_clusters().get('DBClusters')

    return clusters


def get_db_cluster(id: str):
    """
    Get details of a specific database cluster

    :param id: The name of the database cluster :return: `Database Cluster Details
    <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client
    .describe_db_clusters>`_

    """

    clusters = get_rds().describe_db_clusters(Filters=[{'Name': 'db-cluster-id', 'Values': [id]}]).get('DBClusters')
    return clusters[0] if clusters else None


def set_db_cluster_delete_protection(id: str, protect: bool):
    """
    Set the delete protection configuration of the specified database cluster

    :param id: The name of the database cluster
    :param protect: If true, delete protection is enabled for the database cluster.
    :return: N/A

    """

    get_rds().modify_db_cluster(DBClusterIdentifier=id, DeletionProtection=protect)


def list_db_instances(db_cluster_id: str = None, engine: str = None, eks_cluster_name: str = None):
    """
    List all the database instances in the environment

    :param db_cluster_id: Optional name of the database cluster
    :param engine: Optional engine of the database instance
    :param eks_cluster_name: Optional name of EKS cluster. This will search DB that has Tag:clusterName
    defined as the specified EKS cluster name :return: `Database Instance Details
    <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client
    .describe_db_instances>`_

    Example Output::

        [
            {
                DBInstanceIdentifier: "database-1-instance-1"
                DBInstanceClass: "db.r5.large"
                Engine: "aurora"
                DBInstanceStatus: "available"
                MasterUsername: "admin"
                Endpoint: {
                    Address: "database-1-instance-1.cliglprpku2i.us-east-1.rds.amazonaws.com"
                    Port: 3306
                    HostedZoneId: "Z2R2ITUGPM61AM"
                }
                AllocatedStorage: 1
                InstanceCreateTime: 2019-11-08 19:42:38.941000+00:00
                PreferredBackupWindow: "10:25-10:55"
                BackupRetentionPeriod: 1
                DBSecurityGroups: []
                VpcSecurityGroups: [
                    {
                        VpcSecurityGroupId: "sg-0864e77f268788dd5"
                        Status: "active"
                    }
                ]
                DBParameterGroups: [
                    {
                        DBParameterGroupName: "default.aurora5.6"
                        ParameterApplyStatus: "in-sync"
                    }
                ]
                AvailabilityZone: "us-east-1b"
                DBSubnetGroup: {
                    DBSubnetGroupName: "default-vpc-098ec64bb7f6e4799"
                    DBSubnetGroupDescription: "Created from the RDS Management Console"
                    VpcId: "vpc-098ec64bb7f6e4799"
                    SubnetGroupStatus: "Complete"
                    Subnets: [
                        {
                            SubnetIdentifier: "subnet-01777641646dce71d"
                            SubnetAvailabilityZone: {
                                Name: "us-east-1b"
                            }
                            SubnetStatus: "Active"
                        }
                        {
                            SubnetIdentifier: "subnet-022e237798060f8de"
                            SubnetAvailabilityZone: {
                                Name: "us-east-1b"
                            }
                            SubnetStatus: "Active"
                        }
                        {
                            SubnetIdentifier: "subnet-096fe6360d7096d4f"
                            SubnetAvailabilityZone: {
                                Name: "us-east-1c"
                            }
                            SubnetStatus: "Active"
                        }
                        {
                            SubnetIdentifier: "subnet-0a0ededb6d5cec867"
                            SubnetAvailabilityZone: {
                                Name: "us-east-1c"
                            }
                            SubnetStatus: "Active"
                        }
                        {
                            SubnetIdentifier: "subnet-0ed958b196df664ac"
                            SubnetAvailabilityZone: {
                                Name: "us-east-1a"
                            }
                            SubnetStatus: "Active"
                        }
                        {
                            SubnetIdentifier: "subnet-01482395eb32b7e33"
                            SubnetAvailabilityZone: {
                                Name: "us-east-1a"
                            }
                            SubnetStatus: "Active"
                        }
                    ]
                }
                PreferredMaintenanceWindow: "sat:04:17-sat:04:47"
                PendingModifiedValues: {}
                MultiAZ: False
                EngineVersion: "5.6.10a"
                AutoMinorVersionUpgrade: True
                ReadReplicaDBInstanceIdentifiers: []
                LicenseModel: "general-public-license"
                OptionGroupMemberships: [
                    {
                        OptionGroupName: "default:aurora-5-6"
                        Status: "in-sync"
                    }
                ]
                PubliclyAccessible: False
                StorageType: "aurora"
                DbInstancePort: 0
                DBClusterIdentifier: "database-1"
                StorageEncrypted: True
                KmsKeyId: "arn:aws:kms:us-east-1:683863474030:key/c7c7bfb8-3225-4da1-8724-9e06ddf0cff6"
                DbiResourceId: "db-FDGE6FEF2D45HYI4N4TT4KBFRU"
                CACertificateIdentifier: "rds-ca-2015"
                DomainMemberships: []
                CopyTagsToSnapshot: False
                MonitoringInterval: 60
                EnhancedMonitoringResourceArn: "arn:aws:logs:us-east-1:683863474030:log-group:RDSOSMetrics:log-stream:db-FDGE6FEF2D45HYI4N4TT4KBFRU"
                MonitoringRoleArn: "arn:aws:iam::683863474030:role/rds-monitoring-role"
                PromotionTier: 1
                DBInstanceArn: "arn:aws:rds:us-east-1:683863474030:db:database-1-instance-1"
                IAMDatabaseAuthenticationEnabled: False
                PerformanceInsightsEnabled: True
                PerformanceInsightsKMSKeyId: "arn:aws:kms:us-east-1:683863474030:key/c7c7bfb8-3225-4da1-8724-9e06ddf0cff6"
                PerformanceInsightsRetentionPeriod: 7
                DeletionProtection: False
                AssociatedRoles: []
            }
        ]

    """

    if db_cluster_id is not None:
        instances = get_rds().describe_db_instances(Filters=[{'Name': 'db-cluster-id', 'Values': [db_cluster_id]}]).get(
            'DBInstances')
    elif engine is not None:
        instances = get_rds().describe_db_instances(Filters=[{'Name': 'engine', 'Values': [engine]}]).get('DBInstances')
    else:
        instances = get_rds().describe_db_instances().get('DBInstances')

    if eks_cluster_name is None:
        return instances

    # Find ones with TagList:clusterName = eks_cluster_name
    filtered_instances = []
    for instance in instances:
        if util.get_tag_value(instance, 'clusterName', 'TagList') == eks_cluster_name:
            filtered_instances.append(instance)

    return filtered_instances


def get_db_instance(id: str):
    """
    Get details of a specific database instance

    :param id: The name of the database instance
    :return: `Database Instance Details
    <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_instances>`_

    """
    instances = get_rds().describe_db_instances(Filters=[{'Name': 'db-instance-id', 'Values': [id]}]).get('DBInstances')
    return instances[0] if instances else None


def set_db_instance_delete_protection(id: str, protect: bool):
    """
    Set the delete protection configuration of the specified database instance

    :param id: The name of the database instance
    :param protect: If true, delete protection is enabled for the database instance.
    :return: N/A

    """
    get_rds().modify_db_instance(DBInstanceIdentifier=id, DeletionProtection=protect)


###########################################################################
# Database Subnet Groups
###########################################################################

def list_subnet_groups():
    """
    List all database subnet groups

    :return: `Database Subnet Groups Details
    <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_subnet_groups>`_

    Example Output::

        [
            {
                DBSubnetGroupName: "default"
                DBSubnetGroupDescription: "default"
                VpcId: "vpc-c74fccbd"
                SubnetGroupStatus: "Complete"
                Subnets: [
                    {
                        SubnetIdentifier: "subnet-683f4246"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1c"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-fe9ab3f1"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1f"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-42c8b81e"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1a"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-5045431a"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1d"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-86d16bb8"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1e"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-1dec9b7a"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1b"
                        }
                        SubnetStatus: "Active"
                    }
                ]
                DBSubnetGroupArn: "arn:aws:rds:us-east-1:683863474030:subgrp:default"
            }
            {
                DBSubnetGroupName: "default-vpc-098ec64bb7f6e4799"
                DBSubnetGroupDescription: "Created from the RDS Management Console"
                VpcId: "vpc-098ec64bb7f6e4799"
                SubnetGroupStatus: "Complete"
                Subnets: [
                    {
                        SubnetIdentifier: "subnet-01777641646dce71d"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1b"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-022e237798060f8de"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1b"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-096fe6360d7096d4f"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1c"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-0a0ededb6d5cec867"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1c"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-0ed958b196df664ac"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1a"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-01482395eb32b7e33"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1a"
                        }
                        SubnetStatus: "Active"
                    }
                ]
                DBSubnetGroupArn: "arn:aws:rds:us-east-1:683863474030:subgrp:default-vpc-098ec64bb7f6e4799"
            }
            {
                DBSubnetGroupName: "test"
                DBSubnetGroupDescription: "test subnet group"
                VpcId: "vpc-098ec64bb7f6e4799"
                SubnetGroupStatus: "Complete"
                Subnets: [
                    {
                        SubnetIdentifier: "subnet-01777641646dce71d"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1b"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-0ed958b196df664ac"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1a"
                        }
                        SubnetStatus: "Active"
                    }
                ]
                DBSubnetGroupArn: "arn:aws:rds:us-east-1:683863474030:subgrp:test"
            }
        ]

    """
    db_subnet_groups = get_rds().describe_db_subnet_groups().get('DBSubnetGroups')
    return db_subnet_groups


def get_subnet_group(id: str):
    """
    Get details of a specific subnet group

    :param id: The name of the subnet group
    :return: `Database Subnet Groups Details
    <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_subnet_groups>`_

    """
    for group in list_subnet_groups():
        if group['DBSubnetGroupName'] == id:
            return group
    return None


###########################################################################
# Database Security Groups
###########################################################################
def list_db_sgs():
    """
    List all database security groups

    :return: `Database Security Groups Details
    <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_security_groups>`_

    Example Output::

        [
            {
                OwnerId: "683863474030"
                DBSecurityGroupName: "default"
                DBSecurityGroupDescription: "default"
                EC2SecurityGroups: []
                IPRanges: []
                DBSecurityGroupArn: "arn:aws:rds:us-east-1:683863474030:secgrp:default"
            }
        ]

    """

    db_security_groups = get_rds().describe_db_security_groups().get('DBSecurityGroups')
    return db_security_groups


def get_db_sg(id: str):
    """
    List the details of a specific database security group

    :param id: The name of the database security group
    :return: `Database Security Groups Details
    <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_security_groups>`_

    """
    for group in list_db_sgs():
        if group['DBSecurityGroupName'] == id:
            return group
    return None


###########################################################################
# Tags
###########################################################################
def get_rds_tags(arn: str):
    """
    List the tags associated with the RDS object

    :param arn: The ARN of the object or the object in dictionary form to query for Tag element
    :return: The tags associated with the RDS object

    ExampleOutput::

        {
            Env: "test"
            Name: "database-1-instance-1"
        }

    """
    tags = get_rds().list_tags_for_resource(ResourceName=arn).get("TagList")
    res = {}
    for x in tags:
        key = x.get('Key')
        val = x.get('Value')
        res[key] = val
    return res


def find_default_rds_instance(cluster_name: str):
    """
    Find the default rds instance for a given cluster name.

    :param cluster_name: The cluster name to find the default rds instance for.

    :returns: The default rds instance.
    """
    db_instances = list_db_instances(eks_cluster_name=cluster_name)
    db_instance = None
    for instance in db_instances:
        if util.get_tag_value(instance, 'default', 'TagList').lower() == 'true':
            db_instance = instance
            break
    if not db_instance:
        raise ValueError(
            'There was no RDS instance that was found with a default tag. '
            'You can specify which instance to use by using the rdsInstance variable in your app-config.yml.')

    return db_instance


###########################################################################
# Lambda
###########################################################################
def create_lambda(cluster_name: str, database_infos: list):
    """
    Creates a temporary lambda for the RDS associated with the cluster, runs it using the information in database_infos, and finally deletes it.

    :param cluster_name: The name of the cluster
    :param database_infos: The list of information for the lambda in dictionary form.
    Each of the dictionaries should correspond to a database. See the example below for the format

    :return: A tuple containing 3 lists of database names, corresponding to those that haven't had actions performed,
    those that have been created/deleted successfully, and those that encountered errors, the 4th returned value is a
    function to wait for the deletion of the lambda

    Example database_infos::

        database_infos = [
            {
                "function": "create",
                "database": "dvl_myapp",
                "env": "dvl",
                "appName": "myapp",
                'schemas': ["dvl-myapp-customer1"],
                'rdsInstance': "rds-instance-2"
            },
            {
                "function": "create",
                "database": "sat_myapp",
                "env": "sat",
                "appName": "myapp"
            }
        ]
    """

    assert cluster_name and database_infos, 'Cluster name and list of database informations are required.'
    db_instances = list_db_instances(eks_cluster_name=cluster_name)
    assert len(db_instances) >= 1, f'The cluster with name {cluster_name} does not have any associated RDS instances.'
    db_instance = find_default_rds_instance(cluster_name)

    no_action, succeeded, errored = [], [], []

    # default value if perform_lambda_action does not return a waiting function
    def wait_for_delete():
        print('No wait function returned.')

    database_infos_with_no_rds_instance = list(filter(lambda info: (info.get('rdsInstance', '') == ''), database_infos))
    database_infos_that_have_rds_instance = list(
        filter(lambda database_info: (database_info.get('rdsInstance', '') != ''), database_infos))

    if len(database_infos_with_no_rds_instance) > 0:
        na, performed, erred, wait_for_delete = perform_lambda_action(cluster_name=cluster_name,
                                                     database_infos=database_infos_with_no_rds_instance,
                                                     db_instance=db_instance)
        no_action.extend(na)
        succeeded.extend(performed)
        errored.extend(erred)

    if len(database_infos_that_have_rds_instance) > 0:
        database_infos_that_have_rds_instance = sorted(database_infos_that_have_rds_instance,
                                                       key=key_func)  # sort list for use in next line
        for key, value in groupby(database_infos_that_have_rds_instance, key_func):
            # key corresponds to rdsInstance, value corresponds to list of database_info that use that rdsInstance
            rds_instance = list(filter(lambda inst, k=key: inst.get('DBInstanceIdentifier') == k,
                                       db_instances))  # check to see if rds list contains the rdsInstance
            if len(rds_instance) == 0:
                raise ValueError(
                    f'An RDS instance with name {key} does not exist in the cluster with name {cluster_name}.')
            else:
                db_instance = rds_instance[0]
            database_infos_for_rds_instance = list(value)
            na, performed, erred, wait_for_delete = perform_lambda_action(cluster_name=cluster_name,
                                                         database_infos=database_infos_for_rds_instance,
                                                         db_instance=db_instance)
            no_action.extend(na)
            succeeded.extend(performed)
            errored.extend(erred)

    return no_action, succeeded, errored, wait_for_delete


def key_func(k):
    return k['rdsInstance']


def db_info_pre_check(database_info_list):
    """
    Check that database is present in all dicts before doing any work.

    :param database_info_list: list of database_info objects
    """
    for db_info in database_info_list:
        if 'database' not in db_info:
            raise ValueError(
                'ERROR: The database key is required for every entry in the database_infos. '
                'No action was performed for any application database.')


def check_database_info(database_info: dict):
    """
    Checks that a database information object is properly formatted.

    :param database_info: Information about a database for the lambda function.

    :returns: True if valid, False otherwise.

    Example:

    ::

        {
            "function": "create",
            "database": "dvl_myapp",
            "env": "dvl",
            "appName": "myapp",
            'schemas': ["schema1"],
            'rdsInstance': "rds-instance-2"
        }
    """
    database_name = database_info.get('database', '')

    required_keys = ['database', 'function', 'env', 'appName']

    for key in required_keys:
        if key not in database_info:
            print(
                f'WARNING: No action will be performed for application database {database_name} '
                f'because the required "{key}" key is not defined.')
            return False

    if database_info.get('function') not in ["create", "delete"]:
        print(
            f'WARNING: No action will be performed for the application database {database_name} '
            f'because the action specified by the "function" parameter is neither create nor delete.')
        return False

    return True


def create_db_users(database_info: dict, cluster_name: str):
    """
    Create owner, read-only, and master users for a database as defined in database_info.

    :param database_info: Information about a database for the lambda function.
    :param cluster_name: Name of the cluster the db belongs to.
    """

    schemas = database_info['schemas']
    database_name = database_info.get('database')
    env = database_info.get('env')
    app_name = database_info.get('appName')

    for schema in schemas:
        # owner user
        owner_user = schema + "-owner"
        owner_secret_name = f'{cluster_name}-{owner_user}'
        owner_tags = {
            'clusterName': cluster_name,
            'databaseName': database_name,
            'env': env,
            'appName': app_name,
            'schema': schema,
            'userType': 'Owner',
            'secretType': 'Application database schema owner user credentials'
        }
        if not secret.secret_exists_by_tags(tags=owner_tags):
            owner_user_secret_password = util.generate_random_password()
            owner_tags['Name'] = owner_user
            owner_kvp = {'username': owner_user, 'password': owner_user_secret_password}
            secret.create_secret(name=owner_secret_name,
                                 description=f"Credentials for the {owner_user} user for the "
                                             f"{database_name} application database in the {cluster_name} cluster.",
                                 kvp=owner_kvp, tags=owner_tags)
            resulting_secret = secret.get_secret_value(name=owner_user)
            secret.wait_for_secret(name=owner_user, value=resulting_secret)

        # read only user
        readonly_user = schema + "-readonly"
        readonly_secret_name = f'{cluster_name}-{readonly_user}'
        readonly_tags = {
            'clusterName': cluster_name,
            'databaseName': database_name,
            'env': env,
            'appName': app_name,
            'schema': schema,
            'userType': 'ReadOnly',
            'secretType': 'Application database schema readonly user credentials'
        }
        if not secret.secret_exists_by_tags(tags=readonly_tags):
            readonly_user_secret_password = util.generate_random_password()
            readonly_tags['Name'] = readonly_user
            readonly_kvp = {'username': readonly_user, 'password': readonly_user_secret_password}
            secret.create_secret(name=readonly_secret_name,
                                 description=f"Credentials for the {readonly_user} user for the "
                                             f"{database_name} application database in the {cluster_name} cluster.",
                                 kvp=readonly_kvp, tags=readonly_tags)
            resulting_secret = secret.get_secret_value(name=readonly_user)
            secret.wait_for_secret(name=readonly_user, value=resulting_secret)

    # master user
    master_user = env + "-" + app_name + "-master"
    master_secret_name = f'{cluster_name}-{master_user}'
    master_tags = {
        'clusterName': cluster_name,
        'databaseName': database_name,
        'env': env,
        'appName': app_name,
        'userType': 'Master',
        'secretType': 'Application database user credentials'
    }
    if not secret.secret_exists_by_tags(tags=master_tags):
        master_user_secret_password = util.generate_random_password()
        master_tags['Name'] = master_user
        master_kvp = {'username': master_user, 'password': master_user_secret_password}
        secret.create_secret(name=master_secret_name,
                             description=f"Credentials for the {master_user} user for the "
                                         f"{database_name} application database in the {cluster_name} cluster.",
                             kvp=master_kvp, tags=master_tags)
        resulting_secret = secret.get_secret_value(name=master_user)
        secret.wait_for_secret(name=master_user, value=resulting_secret)


def check_rds_password_exists(cluster_name: str, rds_instance_id: str):
    """
    Check that the password for an RDS instance exists as a secret.

    :returns: None on success. Throws a ValueError if it does not exist.
    """
    tags = {
        "clusterName": cluster_name,
        "rdsInstance": rds_instance_id,
        "secretType": "RDS login credentials"
    }
    if not secret.secret_exists_by_tags(tags=tags):
        raise ValueError(
            f'Password secret for RDS instance {rds_instance_id} associated with cluster {cluster_name} does not exist.'
        )


def perform_lambda_action(cluster_name: str, database_infos: list, db_instance, template_dir: str = CFM_DIR):
    rds_instance_id = db_instance.get('DBInstanceIdentifier')
    check_rds_password_exists(cluster_name, rds_instance_id)

    words = rds_instance_id.split('-')
    resource_name = ''.join(word.title() for word in words)
    initial_stack_name = f'{cluster_name}-{resource_name}'
    stack_name, attempt = check_stack_name(initial_stack_name)

    data = {
        'resourceName': resource_name,
        'dbInstanceId': rds_instance_id,
    }

    params = {
        'clusterName': cluster_name,
        'databaseInfo': data,
        'stackName': stack_name,
        'attempt': attempt
    }

    tags = {
        'StackType': STACK_TYPES.lambda_function,
        'clusterName': cluster_name,
        'rdsInstance': rds_instance_id,
        'stackName': stack_name,
        'attempt': attempt
    }

    try:
        cfm.set_template_path(template_dir)
        stack = cfm.create_stack(template_name=STACK_TYPES.lambda_function, params=params,
                                 capabilities=[cfm.CAPABILITY_NAMED_IAM], tags=tags)
        function = cfm.get_output(stack, 'TemporaryLambda' + f'{resource_name}{attempt}')
        zipfile = path.join(LAMBDAS_DIR, 'rds', 'package.zip')
        lambda_fn.update_function_code(function, zipfile)
        lambda_fn.wait_for_lambda(f'rds-temporary-lambda-{resource_name}-{attempt}')

        rds_lambda = cfm.get_output(stack, 'TemporaryLambda' + f'{resource_name}{attempt}')
    except Exception as e:
        print('ERROR: An error occurred when attempting to create the lambda function. '
              'No action was performed for any application database.')
        print(e)
        print('Deleting lambda.')
        delete_lambda_stack(cluster_name, rds_instance_id, attempt, wait=True)
        raise e

    no_action = []
    errored = []
    performed = []

    try:
        db_info_pre_check(database_infos)

        for database_info in database_infos:
            database_name = database_info.get('database')
            database_info['clusterName'] = cluster_name

            if not check_database_info(database_info):
                no_action.append(database_name)
                continue

            function = database_info.get('function', '')
            env = database_info.get('env')
            app_name = database_info.get('appName')

            schemas = database_info.get('schemas', []) + [f'{env}-{app_name}']
            schemas = list(dict.fromkeys(schemas))  # remove duplicates
            database_info['schemas'] = schemas

            if function == "create":
                create_db_users(database_info, cluster_name)

            if database_info.get('rdsInstance', '') == '':
                database_info['rdsInstance'] = rds_instance_id

            master_tags = {
                'clusterName': cluster_name,
                'databaseName': database_name,
                'env': env,
                'appName': app_name,
                'userType': 'Master',
                'secretType': 'Application database user credentials'
            }
            if not secret.secret_exists_by_tags(tags=master_tags) and function == "delete":
                print(
                    f'WARNING: Deletion of application database with name {database_name} was skipped because '
                    f'the master user does not exist.')
                no_action.append(database_name)
                continue

            print(f'Attempting to {function} application database {database_name}')
            result = lambda_fn.invoke_lambda_function(rds_lambda, database_info)
            error = result.get('errorMessage', None)
            if error:
                error_type = result.get('errorType', None)
                print(f'ERROR: An error occurred when trying to {function} the application database {database_name}.')
                print(f'ERROR: {error} ERROR TYPE: {error_type}.')
                errored.append(database_name)
            else:
                print(f'Application database {database_name} was {function}d successfully.')
                performed.append(database_name)
    except Exception as e:
        print('An error occurred. Not all databases have been created/deleted.')
        print(e)
        delete_lambda_stack(cluster_name, rds_instance_id, attempt, wait=True)
        raise e
    finally:
        print('Deleting lambda.')
        delete_lambda_stack(cluster_name, rds_instance_id, attempt)

    return no_action, performed, errored, lambda: delete_lambda_stack(cluster_name, rds_instance_id, attempt, wait=True)


def delete_lambda_stack(cluster_name: str, rds_instance: str, attempt: str, wait: bool = False):
    """
    Deletes the lambda stack on a given cluster.

    :param cluster_name: The cluster name
    :param rds_instance: RDS instance the lambda stack was created for
    :param attempt: The attempt number this stack was created with
    :param wait: Whether to wait for the lambda stack to delete before returning.
    """
    lambda_stack = cfm.find_stack(StackType=STACK_TYPES.lambda_function, clusterName=cluster_name,
                                  rdsInstance=rds_instance, attempt=attempt)
    if lambda_stack:
        cfm.delete_stack(lambda_stack.get('StackName'), wait=wait)


def check_stack_name(stack_name: str):
    """
    Check to see if stack name will collide with other stacks

    :param stack_name: The stack name to be checked
    """
    stack_type = STACK_TYPES.lambda_function
    attempt = 1
    stack_name_check = f'{stack_name}-1-{stack_type}'
    while cfm.stack_exists(stack_name_check):
        attempt += 1
        stack_name_check = stack_name + f'-{attempt}-{stack_type}'
    final_stack_name = stack_name + f'-{attempt}'
    return final_stack_name, str(attempt)