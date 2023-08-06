import unittest
import os
import warnings
from aws import cfm, ec2
import json
import requests

VPC_NAME = 'cfm-unit-test'
CLUSTER_NAME = 'prf'


def _abs_path(file: str):
    basedir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(basedir, file)


def stack_matches(found, expected):
    return found['StackName'] == expected['StackName']


def stack_found(stack, stacks):
    return any(s for s in stacks if stack_matches(s, stack))


def send_slack(name: str, status: str, reason: str, ecr = False):
    slack_message = "WARNING: Deletion of ECR stack for application with name {} has been skipped because other clusters may still depend on it.".format(name) if ecr else "Deletion of stack with name {} has failed with status {}. {}".format(name, status, reason)
    slack_data = {'text': slack_message}
    webhook_url = os.environ["WEBHOOK"]
    response = requests.post(
        webhook_url, data = json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )


def verify_stacks_deleted(cluster_name: str):
    stack_types = ['s3-hosting', 's3-storage', 'rds', 'eks-workers', 'cp', 'vpc']
    everything_deleted = True
    # s3 and ecr are not created currently
    """
    # check s3 deleted
    for stack_type in stack_types[:2]:
        result = cfm.find_stack(StackType=stack_type, clusterName=cluster_name)
        if result:
            everything_deleted = False
            reason = result['StackStatusReason']
            status = result['StackStatus']
            name = result['StackName']
            send_slack(name, status, reason)

    dependant_stacks = cfm.find_stacks(clusterName=cluster_name)
    if len(dependant_stacks) > 1: # (Account for the ECR stack itself)
        send_slack(cluster_name, '', '', ecr=True)
    else:
        result = cfm.find_stack(StackType='ecr', clusterName=cluster_name)
        if result:
            everything_deleted = False
            reason = result['StackStatusReason']
            status = result['StackStatus']
            name = result['StackName']
            send_slack(name, status, reason)
    """
    # check rds, eks, and vpc deleted
    for stack_type in stack_types[2:]:
        result = cfm.find_stack(StackType=stack_type, clusterName=cluster_name)
        if result:
            everything_deleted = False
            if 'StackStatusReason' in result:
                reason = result['StackStatusReason']
            else:
                reason = 'No status reason'
            status = result['StackStatus']
            name = result['StackName']
            send_slack(name, status, reason)
            print(f"{stack_type} not deleted! Sent slack notification.")

    return everything_deleted


class TestCloudFormation(unittest.TestCase):
    params = {
        'VpcName': VPC_NAME,
        'CidrPrefix': '10.10',
        'clusterName': CLUSTER_NAME
    }

    @classmethod
    def setUpClass(cls):
        # Hide boto3 warnings. This is a known issue with boto3 + unittest.
        warnings.simplefilter('ignore', category=ResourceWarning)

        cls.STACK_NAME = f'{CLUSTER_NAME}-basic-stack'
        cfm.set_template_path(_abs_path("templates/"))
        cls.STACK = cfm.create_stack(
            'basic-stack',
            params=cls.params,
            capabilities=[cfm.CAPABILITY_NAMED_IAM],
            tags={'createdByTest': 'test-cfm-setUpClass'},
            debug=True)

        print("cls.STACK = ", cls.STACK)

    @classmethod
    def tearDownClass(cls):
        cfm.delete_stack(cls.STACK_NAME)

    ###########################################################################
    # Set Template Path
    ###########################################################################
    def test_correct_path(self):
        template_dir = _abs_path("templates/")
        cfm.set_template_path(template_dir)
        self.assertEqual(template_dir, cfm._template_path)

    def test_invalid_path(self):
        cfm.set_template_path("invalid")
        stack = cfm.create_stack('invalid-stack', params=self.params,
                                 tags={'createdByTest': 'test-cfm-invalid-path'})
        self.assertIsNone(stack)

    def test_env_changed(self):
        cfm.set_template_path(_abs_path("templates/"))
        env1 = cfm._jinja_env
        cfm.set_template_path(_abs_path("cfm/"))
        env2 = cfm._jinja_env

        self.assertNotEqual(env1, env2)

    ###########################################################################
    # List Stacks
    ###########################################################################

    def test_list_stacks(self):
        all_stacks = cfm.list_stacks()
        self.assertTrue(stack_found(self.STACK, all_stacks))

        completed_stacks = cfm.list_stacks(stack_status_filter=cfm.CREATE_COMPLETE)
        self.assertTrue(stack_found(self.STACK, completed_stacks))

    def test_list_stacks_bogus_filter(self):
        stacks = cfm.list_stacks(stack_status_filter='bogus')
        self.assertEqual(stacks, [])

    ###########################################################################
    # Describe Stacks
    ###########################################################################

    def test_describe_stacks(self):
        all_stacks = cfm.describe_stacks()
        self.assertTrue(stack_found(self.STACK, all_stacks))

        filtered_stacks = cfm.describe_stacks(stack_name=self.STACK_NAME)
        self.assertTrue(stack_found(self.STACK, filtered_stacks))

    def test_describe_stacks_bogus_filter(self):
        stacks = cfm.describe_stacks(stack_name='bogus')
        self.assertEqual(stacks, [])

    ###########################################################################
    # Find Stacks
    ###########################################################################

    def test_find_stacks_exact_match(self):
        stacks = cfm.find_stacks(clusterName=CLUSTER_NAME)
        self.assertTrue(stack_found(self.STACK, stacks))

        stacks = cfm.find_stacks(BogusTag='garbage')
        self.assertEqual(stacks, [])

        stacks = cfm.find_stacks(clusterName=CLUSTER_NAME, BogusTag='garbage')
        self.assertEqual(stacks, [])

    def test_find_stacks_loose_match(self):
        stacks = cfm.find_stacks(match_all=False, clusterName=CLUSTER_NAME)
        self.assertTrue(stack_found(self.STACK, stacks))

        stacks = cfm.find_stacks(match_all=False, BogusTag='garbage')
        self.assertEqual(stacks, [])

        stacks = cfm.find_stacks(match_all=False, clusterName=CLUSTER_NAME, BogusTag='garbage')
        self.assertTrue(stack_found(self.STACK, stacks))

    ###########################################################################
    # Find Stack
    ###########################################################################

    def test_find_stack_exact_match(self):
        stack = cfm.find_stack(clusterName=CLUSTER_NAME)
        self.assertTrue(stack_matches(stack, self.STACK))

        stack = cfm.find_stack(BogusTag='garbage')
        self.assertIsNone(stack)

        stack = cfm.find_stack(clusterName=CLUSTER_NAME, BogusTag='garbage')
        self.assertIsNone(stack)

    def test_find_stack_loose_match(self):
        stack = cfm.find_stack(match_all=False, clusterName=CLUSTER_NAME)
        self.assertTrue(stack_matches(stack, self.STACK))

        stack = cfm.find_stack(match_all=False, BogusTag='garbage')
        self.assertIsNone(stack)

        stack = cfm.find_stack(match_all=False, clusterName=CLUSTER_NAME, BogusTag='garbage')
        self.assertTrue(stack_matches(stack, self.STACK))

    ###########################################################################
    # Stack Status
    ###########################################################################

    def test_get_stack_status(self):
        status = cfm.get_stack_status(self.STACK_NAME)
        self.assertEqual(status, cfm.CREATE_COMPLETE)

    def test_get_stack_status_bogus_stack(self):
        status = cfm.get_stack_status('bogus')
        self.assertIsNone(status)

    ###########################################################################
    # Get Stack
    ###########################################################################

    def test_get_stack(self):
        stack = cfm.get_stack(self.STACK_NAME)
        self.assertTrue(stack_matches(stack, self.STACK))

    def test_get_stack_bogus_name(self):
        stack = cfm.get_stack('bogus')
        self.assertIsNone(stack)

    ###########################################################################
    # Stack Exists
    ###########################################################################

    def test_stack_exists(self):
        exists = cfm.stack_exists(self.STACK_NAME)
        self.assertTrue(exists)

    def test_stack_exists_bogus_name(self):
        exists = cfm.stack_exists('bogus')
        self.assertFalse(exists)

    ###########################################################################
    # Wait For Stack
    ###########################################################################

    def test_wait_for_stack(self):
        status = cfm.wait_for_stack(self.STACK_NAME, cfm.CREATE_IN_PROGRESS)
        self.assertEqual(status, cfm.CREATE_COMPLETE)

    ###########################################################################
    # Create Stack
    ###########################################################################

    # NOTE: Happy path tested via tes setup and other functions

    def test_create_stack_default_name(self):
        # The autogenerated name should match the existing stack name
        # Creation should be skipped and the existing stack returned:
        cfm.set_template_path(_abs_path("templates/"))
        stack = cfm.create_stack('basic-stack', params=self.params,
                                 tags={'createdByTest': 'test-cfm-default-name'})
        self.assertEqual(stack, self.STACK)

    def test_create_stack_already_exists(self):
        cfm.set_template_path(_abs_path("templates/"))
        existing = cfm.create_stack('basic-stack', params=self.params,
                                    tags={'createdByTest': 'test-cfm-already-exists'})
        self.assertEqual(existing, self.STACK)

    def test_create_stack_bogus_filename(self):
        cfm.set_template_path(_abs_path("templates/"))
        result = cfm.create_stack('bogus', params=self.params,
                                  tags={'createdByTest': 'test-cfm-bogus-filename'})
        self.assertIsNone(result)

    ###########################################################################
    # Get Export Value
    ###########################################################################

    def test_get_export_value(self):
        export_name = f'{VPC_NAME}-vpc'
        export_value = cfm.get_export_value(self.STACK_NAME, export_name)
        self.assertIsNotNone(export_value)

    def test_get_export_value_bogus_export(self):
        export_value = cfm.get_export_value(self.STACK_NAME, 'bogus')
        self.assertIsNone(export_value)

    def test_get_export_value_bogus_stack(self):
        export_name = f'{VPC_NAME}-vpc'
        export_value = cfm.get_export_value('bogus', export_name)
        self.assertIsNone(export_value)

    ###########################################################################
    # Delete Stack
    ###########################################################################

    # NOTE: Happy path tested via tear down function

    def test_delete_stack_bogus_stack(self):
        status = cfm.delete_stack('bogus')
        self.assertIsNone(status)

    ###########################################################################
    # Get Output
    ###########################################################################

    def test_get_output(self):
        output = cfm.get_output(self.STACK, 'VPC')
        self.assertIsNotNone(output)

        output = cfm.get_output(self.STACK_NAME, 'VPC')
        self.assertIsNotNone(output)

    def test_get_output_bogus_stack(self):
        with self.assertRaises(Exception):
            cfm.get_output(['wrong-type'], 'VPC')
        with self.assertRaises(Exception):
            cfm.get_output({}, 'VPC')

    def test_get_output_bogus_output(self):
        output = cfm.get_output(self.STACK, 'bogus')
        self.assertIsNone(output)

    ###########################################################################
    # Get Resources
    ###########################################################################

    def test_get_resources(self):
        resources = cfm.get_resources(self.STACK_NAME)
        self.assertNotEqual(resources, [])

    def test_get_resources_bogus_stack(self):
        with self.assertRaises(ValueError):
            cfm.get_resources('bogus')

    def test_get_resource(self):
        resource = cfm.get_resource(self.STACK_NAME, 'VPC')
        self.assertIsNotNone(resource)

    def test_get_resource_bogus_stack(self):
        with self.assertRaises(ValueError):
            cfm.get_resource('bogus', 'VPC')

    def test_get_resource_bogus_resource(self):
        resource = cfm.get_resource(self.STACK_NAME, 'bogus')
        self.assertIsNone(resource)

    def test_get_resource_id(self):
        resource_id = cfm.get_resource_id(self.STACK_NAME, 'VPC')
        vpc = ec2.get_vpc(vpcid=resource_id)
        self.assertIsNotNone(vpc)

    def test_get_resource_id_bogus_stack(self):
        with self.assertRaises(ValueError):
            cfm.get_resource_id('bogus', 'VPC')

    def test_get_resource_id_bogus_resource(self):
        resource_id = cfm.get_resource_id(self.STACK_NAME, 'bogus')
        self.assertIsNone(resource_id)


if __name__ == "__main__":
    unittest.main(verbosity=2)
