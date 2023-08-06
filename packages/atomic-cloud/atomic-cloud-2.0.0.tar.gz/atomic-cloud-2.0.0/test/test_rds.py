import unittest
import warnings
import os
from os import path
import random
from aws import rds, cluster, cfm, util, secret
from test import test_cluster as test_cluster


CLUSTER_NAME = test_cluster.CONFIG_FILE['clusterName']

DB_CLUSTER_ID = None
DB_CLUSTER_ENGINE = None
DB_INSTANCE_ID = None
DB_INSTANCE_ENGINE = None
DB_SG = None


def _abs_path(file: str):
    basedir = path.abspath(path.dirname(__file__))
    return path.join(basedir, file)

def _delete_secrets_after_test(random_env: str, random_app_name: str):
    secret.delete_secret(name=f'{CLUSTER_NAME}-{random_env}-{random_app_name}-owner', perma_delete=True)
    secret.delete_secret(name=f'{CLUSTER_NAME}-{random_env}-{random_app_name}-readonly', perma_delete=True)
    secret.delete_secret(name=f'{CLUSTER_NAME}-{random_env}-{random_app_name}-master', perma_delete=True)

class TestRDS(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Hide boto3 warnings. This is a known issue with boto3 + unittest.
        warnings.simplefilter('ignore', category=ResourceWarning)
        
        rds_stack = cluster.get_rds(CLUSTER_NAME)
        if not rds_stack:
            raise RuntimeError('must call test_cluster.create_test_cluster() prior to this test')

        cfm.set_template_path(_abs_path("templates/"))
        db_cluster_stack = cfm.create_stack(
            'rds-db-cluster',
            params={'clusterName': CLUSTER_NAME},
            tags={'createdByTest': 'TestRDS-setUpClass'})

        global DB_CLUSTER_ID, DB_CLUSTER_ENGINE, DB_INSTANCE_ID, DB_INSTANCE_ENGINE, DB_SG
        DB_CLUSTER_ID = cfm.get_output(db_cluster_stack, 'DBCluster')
        DB_CLUSTER_ENGINE = rds.get_db_cluster(DB_CLUSTER_ID)['Engine']
        DB_INSTANCE_ID = test_cluster.CONFIG_FILE['databases'][0]['dBClusterId']
        DB_INSTANCE_ENGINE = rds.get_db_instance(DB_INSTANCE_ID)['Engine']
        DB_SG = cfm.get_output(rds_stack, 'DBSecurityGroup')


    @classmethod
    def tearDownClass(cls):
        cfm.delete_stack(f'{CLUSTER_NAME}-rds-db-cluster')


    ###########################################################################
    # Database Clusters
    ###########################################################################
    
    def test_list_db_clusters(self):
        all_clusters = rds.list_db_clusters()
        self.assertNotEqual(all_clusters, [])

        filtered_clusters = rds.list_db_clusters(engine=DB_CLUSTER_ENGINE)
        self.assertNotEqual(filtered_clusters, [])


    def test_list_db_clusters_nonexistent_engine(self):
        with self.assertRaises(Exception):
            rds.list_db_clusters(engine='bogus')


    def test_get_db_cluster(self):
        result = rds.get_db_cluster(DB_CLUSTER_ID)
        self.assertIsNotNone(result)


    def test_get_db_cluster_nonexistent(self):
        result = rds.get_db_cluster('bogus')
        self.assertIsNone(result)


    def test_set_cluster_delete_protection(self):
        rds.set_db_cluster_delete_protection(DB_CLUSTER_ID, protect=True)
        db_cluster = rds.get_db_cluster(DB_CLUSTER_ID)
        self.assertTrue(db_cluster['DeletionProtection'])

        rds.set_db_cluster_delete_protection(DB_CLUSTER_ID, protect=False)
        db_cluster = rds.get_db_cluster(DB_CLUSTER_ID)
        self.assertFalse(db_cluster['DeletionProtection'])

    
    ###########################################################################
    # Database Instances
    ###########################################################################

    def test_list_db_instances(self):
        all_instances = rds.list_db_instances()
        self.assertNotEqual(all_instances, [])

        filtered_by_engine = rds.list_db_instances(engine=DB_INSTANCE_ENGINE)
        self.assertNotEqual(filtered_by_engine, [])

        filtered_by_cluster = rds.list_db_instances(db_cluster_id=DB_CLUSTER_ID)
        self.assertEqual(filtered_by_cluster, [])


    def test_get_db_instance(self):
        result = rds.get_db_instance(DB_INSTANCE_ID)
        self.assertIsNotNone(result)


    def test_get_db_instance_nonexistent(self):
        result = rds.get_db_instance('bogus')
        self.assertIsNone(result)


    def test_set_db_instance_delete_protection(self):
        rds.set_db_instance_delete_protection(DB_INSTANCE_ID, protect=True)
        db_instance = rds.get_db_instance(DB_INSTANCE_ID)
        self.assertTrue(db_instance['DeletionProtection'])

        rds.set_db_instance_delete_protection(DB_INSTANCE_ID, protect=False)
        db_instance = rds.get_db_instance(DB_INSTANCE_ID)
        self.assertFalse(db_instance['DeletionProtection'])


    ###########################################################################
    # Database Subnet Groups
    ###########################################################################

    def test_list_subnet_groups(self):
        groups = rds.list_subnet_groups()
        self.assertNotEqual(groups, [])


    def test_get_subnet_group(self):
        subnet_group_name = rds.get_db_instance(DB_INSTANCE_ID)['DBSubnetGroup']['DBSubnetGroupName']
        subnet_group = rds.get_subnet_group(subnet_group_name)
        self.assertIsNotNone(subnet_group)

    
    def test_get_subnet_group_nonexistent(self):
        subnet_group = rds.get_subnet_group('bogus')
        self.assertIsNone(subnet_group)


    ###########################################################################
    # Database Security Groups
    ###########################################################################

    def test_list_db_sgs(self):
        sgs = rds.list_db_sgs()
        self.assertNotEqual(sgs, [])


    def test_get_db_sg(self):
        sg_name = rds.list_db_sgs()[0]['DBSecurityGroupName']
        found_sg = rds.get_db_sg(sg_name)
        self.assertEqual(found_sg['DBSecurityGroupName'], sg_name)


    def test_get_db_sg_nonexistent(self):
        found = rds.get_db_sg('bogus')
        self.assertIsNone(found)


    ###########################################################################
    # Tags
    ###########################################################################

    def test_get_rds_tags(self):
        arn = rds.get_db_instance(DB_INSTANCE_ID)['DBInstanceArn']
        tags = rds.get_rds_tags(arn)
        self.assertNotEqual(tags, {})

    
    ###########################################################################
    # Lambda
    ###########################################################################

    def test_find_default_rds_instance_not_found(self):
        with self.assertRaisesRegex(ValueError, 
            'There was no RDS instance that was found with a default tag. '
            'You can specify which instance to use by using the rdsInstance variable in your app-config.yml.'):
            rds.find_default_rds_instance(cluster_name='bogous')
    

    def test_find_default_rds_instance_success(self):
        result = rds.find_default_rds_instance(cluster_name=CLUSTER_NAME)
        self.assertNotEqual(result, None)
    

    def test_db_info_pre_check_failure(self):
        db_info_list = [
            {
                "function": "create",
                "database": "dvl_myapp",
                "env": "dvl",
                "appName": "myapp",
            },
            {
                "function": "create",
                "env": "sat",
                "appName": "myapp",
            }
        ]
        with self.assertRaisesRegex(ValueError, 
            'ERROR: The database key is required for every entry in the database_infos. '
            'No action was performed for any application database.'):
            rds.db_info_pre_check(database_info_list=db_info_list)
    

    def test_db_info_pre_check_success(self):
        db_info_list = [
            {
                "function": "create",
                "database": "dvl_myapp",
                "env": "dvl",
                "appName": "myapp",
            },
            {
                "function": "create",
                "database": "sat_myapp",
                "env": "sat",
                "appName": "myapp",
            }
        ]
        try:
            rds.db_info_pre_check(database_info_list=db_info_list)
        except Exception as e:
            print(e)
            self.fail('Unexpected failure occurred')
    

    def test_check_database_info_missing_required(self):
        db_info = {
            "database": "dvl_myapp",
            "env": "dvl",
            "appName": "myapp",
        }
        self.assertFalse(rds.check_database_info(database_info=db_info))
    

    def test_check_database_info_incorrect_function(self):
        db_info = {
            "function": "destroy",
            "database": "dvl_myapp",
            "env": "dvl",
            "appName": "myapp",
        }
        self.assertFalse(rds.check_database_info(database_info=db_info))
    

    def test_check_database_info_success(self):
        db_info = {
            "function": "create",
            "database": "dvl_myapp",
            "env": "dvl",
            "appName": "myapp",
        }
        self.assertTrue(rds.check_database_info(database_info=db_info))
    

    def test_check_rds_password_exists_nonexistent(self):
        with self.assertRaises(ValueError):
            rds.check_rds_password_exists(cluster_name='moreb0gus', rds_instance_id='ev3nm0r38Ogu5')


    def test_create_lambda_empty_information(self):
        with self.assertRaises(AssertionError):
            rds.create_lambda(cluster_name='', database_infos=[])
    

    def test_create_lambda_cluster_not_found(self):
        with self.assertRaises(AssertionError):
            rds.create_lambda(cluster_name='bogus', database_infos=[{'bogus': 'data'}])
    

    def test_create_lambda_specified_rdsInstance_nonexistent(self):
        database_infos = [{
            'function': 'create',
            'database': 'dvl_myapp',
            'env': 'dvl',
            'appName': 'myapp',
            'rdsInstance': 'b0gu5'
        }]
        with self.assertRaisesRegex(ValueError, f"An RDS instance with name b0gu5 does not exist in the cluster with name {CLUSTER_NAME}."):
            rds.create_lambda(cluster_name=CLUSTER_NAME, database_infos=database_infos)
    

    def test_create_lambda_no_action(self):
        default_rds = rds.find_default_rds_instance(cluster_name=CLUSTER_NAME).get('DBInstanceIdentifier')
        database_infos = [
            {
                'function': 'noaction',
                'database': 'dvl_myapp',
                'env': 'dvl',
                'appName': 'myapp',
                'rdsInstance': default_rds,
            }
        ]
        try:
            no_action, performed, errored, wait_for_delete = rds.create_lambda(cluster_name=CLUSTER_NAME, database_infos=database_infos)
            print('create_lambda() returned. Wait for delete now.')
            wait_for_delete()
            if len(no_action) != 1 or len(performed) > 0 or len(errored) > 0:
                self.fail(f'No databases should have been created.')
        except Exception:
            self.fail(f'An unexpected exception was encountered.')
    

    def test_create_lambda_success(self):
        env_choices = ['dvl', 'sat', 'prd', 'prf', 'edu', 'cicd']
        random_env = random.choice(env_choices)
        random_app_name = util.generate_random_string(5)
        database_infos = [
            {
                "function": "create",
                "database": f"{random_env}_{random_app_name}",
                "env": random_env,
                "appName": random_app_name,
                "schema": ["dvl-myapp-standard"]
            }
        ]
        try:
            no_action, performed, errored, wait_for_delete = rds.create_lambda(cluster_name=CLUSTER_NAME, database_infos=database_infos)
            print('create_lambda() returned. Wait for delete now.')
            wait_for_delete()
            if len(no_action) > 0 or len(performed) != 1 or len(errored) > 0:
                _delete_secrets_after_test(random_env=random_env, random_app_name=random_app_name)
                self.fail(f'Application database was not created properly.')
        except Exception as e:
            print(e)
            _delete_secrets_after_test(random_env=random_env, random_app_name=random_app_name)
            self.fail(f'An unexpected exception was encountered during creation of the application database.')
        self.assertTrue(secret.secret_exists(f'{CLUSTER_NAME}-{random_env}-{random_app_name}-owner'))
        self.assertTrue(secret.secret_exists(f'{CLUSTER_NAME}-{random_env}-{random_app_name}-readonly'))
        self.assertTrue(secret.secret_exists(f'{CLUSTER_NAME}-{random_env}-{random_app_name}-master'))
        _delete_secrets_after_test(random_env=random_env, random_app_name=random_app_name)


if __name__ == "__main__":
    unittest.main()