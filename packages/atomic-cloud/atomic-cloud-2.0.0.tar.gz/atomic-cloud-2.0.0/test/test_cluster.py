import time
from unittest import TestCase, main
from aws import cfm, ec2, cert, cluster, config
import boto3
import warnings
import os


basedir = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(basedir, 'templates/configs/cluster-config.yml')
if os.getenv('automated') == '1':
    config_path = os.path.join(basedir, 'templates/configs/jenkins-cluster-config.yml')
CONFIG_FILE = config.create_config(config_path)


def create_test_cluster():
    '''
    This can be used externally to create the test cluster before running tests.
    Useful for reusing the resources created here in other test files.
    '''

    try:

        cluster.create_cluster(config=CONFIG_FILE)
        # app specific
        # cluster.create_app(CONFIG_FILE['clusterName'], self.app_name, CONFIG.domain_name, CONFIG.app_db_password)
    except Exception as e:
        print('Exception raised during cluster creation. Cleaning up created resources...')
        delete_test_cluster()
        raise e


def delete_test_cluster():
    # cluster.delete_app(CONFIG.vpc_name, self.app_name)
    cluster.delete_ecr('UnitTestApp')
    cluster.delete_cluster(CONFIG_FILE['clusterName'], keep_certs=True)
    return CONFIG_FILE['clusterName']


def get_output(stack: dict, output_key: str):
    '''Helper function to get an OutputValue from the given stack'''
    return next((o['OutputValue'] for o in stack['Outputs'] if o.get('OutputKey') == output_key), None)


class TestCluster(TestCase):

    ###########################################################################
    # Test Setup/Cleanup
    ###########################################################################

    @classmethod
    def setUpClass(cls):
        # Hide boto3 warnings. This is a known issue with boto3 + unittest.
        warnings.simplefilter('ignore', category=ResourceWarning)

        cls.app_name = 'UnitTestApp'

        # NOTE: If running this test standalone, uncomment this line
        # create_test_cluster()

    @classmethod
    def tearDownClass(cls):
        # NOTE: If running this test standalone, uncomment this line
        # delete_test_cluster()
        pass

    ###########################################################################
    # Certificate
    ###########################################################################

    def test_create_certificate_invalid_domain_name(self):
        with self.assertRaises(Exception):
            # do not use the same clusterName in this call as in the config file or it will delete the real one
            cert = cluster.create_certificate('prd', 'garbage',
                                              validation_domain=CONFIG_FILE['validationDomain'])
            cfm.delete_stack(cert['StackName'])

    def test_create_certificate(self):
        cert = cluster.create_certificate(CONFIG_FILE['clusterName'], CONFIG_FILE['baseDomain'],
                                          validation_domain=CONFIG_FILE['validationDomain'])

        cert_arn = get_output(cert, 'OutputCertificate')
        self.assertIsNotNone(cert_arn, msg='Certificate ARN not found in output')

        try:
            boto3.client('acm').get_certificate(CertificateArn=cert_arn)
        except Exception:
            self.fail(f'Could not find certificate with ARN: {cert_arn}. It may have not been created properly.')

    def test_create_certificate_existent(self):
        test_domain_name = 'unittest1235.simoncomputing.com'
        try:
            # create a cert
            c = cert.generate_self_signed_cert(test_domain_name, 'US', 'Virginia', 'Alexandria', 'SimonComputing', 2)
            cert.import_cert(test_domain_name, c['public'], c['private'])
            time.sleep(30)

            stack = cluster.get_certificate(CONFIG_FILE['clusterName'], CONFIG_FILE['baseDomain'])

            # try to create a cert that already exist
            result = cluster.create_certificate(CONFIG_FILE['clusterName'], test_domain_name,
                                                validation_domain=CONFIG_FILE['validationDomain'])
            self.assertEqual(stack['Outputs'], result['Outputs'])
        finally:
            cert.delete_cert(test_domain_name)

    def test_get_certificate_nonexistent(self):
        cert = cluster.get_certificate('bogus', 'garbage')
        self.assertIsNone(cert)

    def test_get_certificate(self):
        cert = cluster.get_certificate(CONFIG_FILE['clusterName'], CONFIG_FILE['baseDomain'])
        self.assertIsNotNone(cert)

    ###########################################################################
    # VPC
    ###########################################################################

    def test_create_vpc_invalid_cidr(self):
        with self.assertRaises(Exception):
            stack = cluster.create_vpc('bogus', cidr_prefix='garbage')
            cfm.delete_stack(stack['StackName'])

    def test_create_vpc(self):
        vpc = cluster.create_vpc(CONFIG_FILE['clusterName'], cidr_prefix=CONFIG_FILE['cidrPrefix'])

        vpcid = get_output(vpc, 'VPC')
        self.assertIsNotNone(ec2.get_vpc(vpcid=vpcid))

    def test_get_vpc_nonexistent(self):
        vpc = cluster.get_vpc('garbage')
        self.assertIsNone(vpc)

    def test_get_vpc(self):
        vpc = cluster.get_vpc(CONFIG_FILE['clusterName'])
        self.assertIsNotNone(vpc)

    ###########################################################################
    # CP
    ###########################################################################

    def test_create_cp_unknown_vpc(self):
        with self.assertRaises(Exception):
            cp = cluster.create_cp('garbage')
            cfm.delete_stack(cp['StackName'])

    def test_create_cp(self):
        cp = cluster.create_cp(CONFIG_FILE['clusterName'], CONFIG_FILE.get('eksVersion', '1.21'))

        cluster_name = get_output(cp, 'Cluster')

        try:
            boto3.client('eks').describe_cluster(name=cluster_name)
        except Exception:
            self.fail(f'Could not find cluster: {cluster_name}. It may not have been created properly.')

    def test_get_cp_nonexistent(self):
        cp = cluster.get_cp('garbage')
        self.assertIsNone(cp)

    def test_get_cp(self):
        cp = cluster.get_cp(CONFIG_FILE['clusterName'])
        self.assertIsNotNone(cp)

    ###########################################################################
    # EKS Workers
    ###########################################################################

    def test_create_eks_workers_unknown_cp(self):
        with self.assertRaises(Exception):
            eks_workers = cluster.create_eks_workers('garbage', CONFIG_FILE['workerGroups'])
            cfm.delete_stack(eks_workers['StackName'])

    def test_create_eks_workers(self):
        eks_workers = cluster.create_eks_workers(CONFIG_FILE['clusterName'], CONFIG_FILE['workerGroups'])

        cluster_name = get_output(eks_workers, 'ClusterName')
        # the output key is 'NodegroupName'+workerGroupName for each workerGroup
        name_key = 'NodegroupName'+CONFIG_FILE['workerGroups'][0]['workerGroupName']
        nodegroup_name = get_output(eks_workers, name_key)

        try:
            boto3.client('eks').describe_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup_name)
        except Exception:
            self.fail(f'Could not find nodegroup: {nodegroup_name}. It may not have been created properly.')

    def test_get_eks_workers_nonexistent(self):
        workers = cluster.get_eks_workers('garbage')
        self.assertIsNone(workers)

    def test_get_eks_workers(self):
        eks_workers = cluster.get_eks_workers(CONFIG_FILE['clusterName'])
        self.assertIsNotNone(eks_workers)

    ###########################################################################
    # RDS
    ###########################################################################
    
    def test_create_rds_unknown_vpc(self):
        with self.assertRaises(Exception):
            rds = cluster.create_rds('garbage', CONFIG_FILE['databases'])
            cfm.delete_stack(rds['StackName'])

    def test_create_rds(self):
        # avoid lambda error from calling update_function_code twice too quickly
        stack_name = CONFIG_FILE['clusterName'] + '-04-rds'
        if not cfm.stack_exists(stack_name):
            rds = cluster.create_rds(CONFIG_FILE['clusterName'], CONFIG_FILE['databases'])
        else:
            rds = cfm.get_stack(stack_name)

        db = CONFIG_FILE['databases'][0]
        # DB instance output are named 'DBInstance' + resource name
        instance_id = get_output(rds, 'DBInstance'+cluster.get_db_resource_name(db))

        try:
            boto3.client('rds').describe_db_instances(DBInstanceIdentifier=instance_id)
        except Exception:
            self.fail(f'Could not find RDS instance: {instance_id}. It may not have been created properly.')

    def test_get_rds_nonexistent(self):
        rds = cluster.get_rds('garbage')
        self.assertIsNone(rds)

    def test_get_rds(self):
        rds = cluster.get_rds(CONFIG_FILE['clusterName'])
        self.assertIsNotNone(rds)

    ###########################################################################
    # ECR
    ###########################################################################

    def test_create_ecr(self):
        ecr = cluster.create_ecr(self.app_name)

        repo_name = get_output(ecr, 'Repository')

        try:
            boto3.client('ecr').describe_repositories(repositoryNames=[repo_name])
        except Exception:
            self.fail(f'Could not find ECR repository: {repo_name}. It may not have been created properly')

    def test_get_ecr_nonexistent(self):
        ecr = cluster.get_ecr('garbage')
        self.assertIsNone(ecr)

    def test_get_ecr(self):
        ecr = cluster.get_ecr(self.app_name)
        self.assertIsNotNone(ecr)

    """
    ###########################################################################
    # S3 Storage
    ###########################################################################

    def test_create_s3_storage_unknown_vpc(self):
        with self.assertRaises(ValueError):
            s3_storage = cluster.create_s3_storage('garbage', self.app_name)
            cfm.delete_stack(s3_storage['StackName'])

    def test_create_s3_storage(self):
        s3_storage = cluster.create_s3_storage(CONFIG_FILE['clusterName'], self.app_name)

        bucket = get_output(s3_storage, 'Bucket')

        try:
            boto3.client('s3').list_objects(Bucket=bucket)
        except Exception:
            self.fail(f'Could not find bucket {bucket}. It may not have been created properly.')

    def test_get_s3_storage_nonexistent(self):
        s3_storage = cluster.get_s3_storage('bogus', 'garbage')
        self.assertIsNone(s3_storage)

    def test_get_s3_storage(self):
        s3_storage = cluster.get_s3_storage(CONFIG_FILE['clusterName'], self.app_name)
        self.assertIsNotNone(s3_storage)
    """
    ###########################################################################
    # S3 Hosting
    ###########################################################################
    def test_create_s3_hosting(self):
        test_app_domain_name = 'unittest.dvl.atomictests.com'
        try:
            s3_hosting = cluster.create_s3_hosting(CONFIG_FILE['clusterName'], 'unittest', test_app_domain_name, 'dvl', CONFIG_FILE['validationDomain'])
            for o in s3_hosting['Outputs']:
                print(o['OutputValue'] + " " + o.get('OutputKey') )

            bucket = get_output(s3_hosting, 'Bucket')
            self.assertIsNotNone(bucket, msg='Bucket not found in output')

            try:
                boto3.client('s3').list_objects(Bucket=bucket)
            except Exception:
                self.fail(f'Could not find bucket {bucket}. It may not have been created properly.')

            distribution = get_output(s3_hosting, 'Distribution')
            self.assertIsNotNone(distribution, msg='Distribution not found in output')
            try:
                boto3.client('cloudfront').get_distribution(Id=distribution)
            except Exception:
                self.fail(f'Could not find cloudfront distribution {distribution}. It may not have been created properly.')

            get_s3_hosting = cluster.get_s3_hosting(CONFIG_FILE['clusterName'], 'unittest', 'dvl')
            self.assertIsNotNone(get_s3_hosting)
        finally:
            cluster.delete_s3_hosting(CONFIG_FILE['clusterName'], 'unittest', 'dvl')

    def test_get_s3_hosting_nonexistent(self):
        s3_hosting = cluster.get_s3_hosting('bogus', 'garbage', 'dvl')
        self.assertIsNone(s3_hosting)


    ###########################################################################
    # Application Database
    ###########################################################################
    """
    def test_create_app_database(self):
        cluster.delete_app_database(CONFIG_FILE['clusterName'], self.app_name)
        cluster.create_app_database(CONFIG_FILE['clusterName'], self.app_name, 'password')
        cluster.delete_app_database(CONFIG_FILE['clusterName'], self.app_name)

    def test_create_app_database_already_exists(self):
        cluster.delete_app_database(CONFIG_FILE['clusterName'], self.app_name)
        cluster.create_app_database(CONFIG_FILE['clusterName'], self.app_name, 'password')
        with self.assertRaises(ValueError):
            cluster.create_app_database(CONFIG_FILE['clusterName'], self.app_name, 'password')
            cluster.delete_app_database(CONFIG_FILE['clusterName'], self.app_name)

    def test_create_app_database_no_rds(self):
        with self.assertRaises(ValueError):
            cluster.create_app_database('bogus', 'garbage', 'password')

    def test_delete_app_database_nonexistent(self):
        cluster.delete_app_database(CONFIG_FILE['clusterName'], 'garbage')

    def test_delete_app_database_no_rds(self):
        with self.assertRaises(ValueError):
            cluster.delete_app_database('bogus', 'garbage')

    
    ###########################################################################
    # App Factsheet
    ###########################################################################

    def test_generate_app_factsheet_nonexistent_app(self):
        with self.assertRaises(Exception):
            cluster.generate_app_factsheet(['bogus'], 'garbage')

    def test_generate_app_factsheet(self):
        filename = cluster.generate_app_factsheet([CONFIG_FILE['clusterName']], self.app_name)
        self.assertTrue(os.path.isfile(filename))

    """


if __name__ == "__main__":
    main()
