import unittest
from aws import secret, region, util
import warnings
import json

# NOTE: Don't run this test multiple times in quick succession.
#       Even though the test secrets are perma-deleted afterwards,
#       it usually takes a minute for them to disappear completely.

class TestSecret(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Hide boto3 warnings. This is a known issue with boto3 + unittest.
        warnings.simplefilter('ignore', category=ResourceWarning)

        cls.tag_w = {"WwWwWw":"VvVvVv"}
        cls.tag_x = {"XxXxXx":"OoOoOo"}
        cls.tag_wx = {"XxXxXx":"OoOoOo", "WwWwWw":"VvVvVv"}
        
        cls.STRING_SECRET = secret.create_secret(
            name='unit-test-string-secret',
            description='Test string secret for Atomic Cloud unit tests',
            string='string-secret')

        cls.JSON_SECRET = secret.create_secret(
            name='unit-test-json-secret',
            description='Test JSON secret for Atomic Cloud unit tests',
            kvp={'secret-key': 'secret-value'},
            tags=cls.tag_w)

        cls.JSON_SECRET_WITH_TAGS = secret.create_secret(
            name='unit-test-json-secret-with-tags',
            description='Test JSON secret with tags for Atomic Cloud unit tests',
            kvp={'secret-key-with-tags': 'secret-value-with-tags'},
            tags=cls.tag_wx)

        cls.BINARY_SECRET = secret.create_secret(
            name='unit-test-binary-secret',
            description='Test binarysecret for Atomic Cloud unit tests',
            binary=b'binary-secret')


    @classmethod
    def tearDownClass(cls):
        secret.delete_secret(cls.STRING_SECRET['Name'], perma_delete=True)
        secret.delete_secret(cls.JSON_SECRET['Name'], perma_delete=True)
        secret.delete_secret(cls.JSON_SECRET_WITH_TAGS['Name'], perma_delete=True)
        secret.delete_secret(cls.BINARY_SECRET['Name'], perma_delete=True)


    ###########################################################################
    # Get Secret Value
    ###########################################################################
    
    def test_get_secret_value_string(self):
        secret_name = self.STRING_SECRET['Name']
        created_secret = self.STRING_SECRET['SecretString']

        retrieved_secret = secret.get_secret_value(secret_name)
        self.assertEqual(retrieved_secret, created_secret)


    def test_get_secret_value_json(self):
        secret_name = self.JSON_SECRET['Name']
        created_secret = self.JSON_SECRET['SecretString']

        retrieved_secret = secret.get_secret_value(secret_name)
        self.assertEqual(created_secret, retrieved_secret)

        created_secret_dict = json.loads(created_secret)
        created_secret_key = next(k for k in created_secret_dict)
        created_secret_value = created_secret_dict[created_secret_key]

        retrieved_secret_value = secret.get_secret_value(secret_name, created_secret_key)
        self.assertEqual(retrieved_secret_value, created_secret_value)


    def test_get_secret_value_binary(self):
        secret_name = self.BINARY_SECRET['Name']
        created_secret = self.BINARY_SECRET['SecretBinary']

        retrieved_secret = secret.get_secret_value(secret_name)
        self.assertEqual(retrieved_secret, created_secret)


    def test_get_secret_value_bogus_name(self):
        result = secret.get_secret_value('bogus')
        self.assertIsNone(result)


    def test_get_secret_value_bogus_key(self):
        result = secret.get_secret_value(self.JSON_SECRET, 'bogus')
        self.assertIsNone(result)


    def test_update_secret_string(self):
        secret_name = self.STRING_SECRET['Name']
        original_value = self.STRING_SECRET['SecretString']

        new_value = 'new-string-secret'
        secret.update_secret(secret_name, string=new_value)

        self.assertEqual(secret.get_secret_value(secret_name), new_value)
        secret.update_secret(secret_name, string=original_value)


    ###########################################################################
    # Create Secret
    ###########################################################################

    def test_create_secret_with_tags(self):
        try:
            string_secret = secret.create_secret(
                name='unit-test-string-secret-with-tags',
                string='string-secret',
                tags={'type': 'string'})['Name']

            binary_secret = secret.create_secret(
                name='unit-test-binary-secret-with-tags',
                binary=b'binary-secret',
                tags={'type': 'binary'})['Name']

            tag_found = lambda tags, k, v: any(pair for pair in tags if pair['Key'] == k and pair['Value'] == v)

            string_secret_tags = region.get_secret().describe_secret(SecretId=string_secret)['Tags']
            self.assertTrue(tag_found(string_secret_tags, 'type', 'string'))

            binary_secret_tags = region.get_secret().describe_secret(SecretId=binary_secret)['Tags']
            self.assertTrue(tag_found(binary_secret_tags, 'type', 'binary'))
        finally:
            secret.delete_secret(string_secret, perma_delete=True)
            secret.delete_secret(binary_secret, perma_delete=True)


    def test_create_secret_multiple_types(self):
        with self.assertRaises(Exception):
            secret.create_secret('toomanytypes', string='string', binary=b'binary')


    ###########################################################################
    # Update Secret
    ###########################################################################

    def test_update_secret_json(self):
        secret_name = self.JSON_SECRET['Name']
        original_value = self.JSON_SECRET['SecretString']
        original_kvp = json.loads(original_value)
        
        new_kvp = {'new-key': 'new-value'}
        secret.update_secret(secret_name, kvp=new_kvp, overwrite_json=False)

        combined_kvp = original_kvp.copy()
        combined_kvp.update(new_kvp)
        retrieved_kvp = json.loads(secret.get_secret_value(secret_name))
        self.assertEqual(retrieved_kvp, combined_kvp)

        secret.update_secret(secret_name, kvp=original_kvp, overwrite_json=True)
        self.assertEqual(secret.get_secret_value(secret_name), original_value)


    def test_update_secret_binary(self):
        secret_name = self.BINARY_SECRET['Name']
        original_value = self.BINARY_SECRET['SecretBinary']

        new_value = b'new-binary-secret'
        secret.update_secret(secret_name, binary=new_value)

        self.assertEqual(secret.get_secret_value(secret_name), new_value)
        secret.update_secret(secret_name, binary=original_value)


    def test_update_secret_multiple_types(self):
        with self.assertRaises(Exception):
            secret.update_secret('toomanytypes', string='string', binary=b'binary')


    ###########################################################################
    # Delete Secret
    ###########################################################################

    def test_delete_secret_nonexistent(self):
        result = secret.delete_secret('bogus')
        self.assertFalse(result)


    def test_delete_secret_recovery_and_perma(self):
        with self.assertRaises(Exception):
            secret.delete_secret('bogus', recovery_window=7, perma_delete=True)


    # def test_delete_secret_with_recovery(self):
    #     try:
    #         string_secret = secret.create_secret(
    #             name='unit-test-string-secret-delete-with-recovery',
    #             string='string-secret')['Name']

    #         secret.delete_secret(string_secret)
    #         found = secret.get_secret_value(string_secret)
    #         self.assertIsNone(found)

    #         secret.restore_secret(string_secret)
    #         found = secret.get_secret_value(string_secret)
    #         self.assertIsNotNone(found)
    #     finally:
    #         secret.delete_secret(string_secret, perma_delete=True)

    
    def test_delete_secret_perma(self):
        secret_name = 'test_delete_perma_secret'
        secret.create_secret(secret_name, string='secret')
        resulting_secret = secret.get_secret_value(name=secret_name)
        secret.wait_for_secret(name=secret_name, value=resulting_secret)
        self.assertTrue(secret.secret_exists(secret_name))
        secret.delete_secret(secret_name, perma_delete=True)
        secret.wait_for_perma_delete(secret_name)
        self.assertFalse(secret.secret_exists(secret_name))
        self.assertIsNone(secret.get_secret_value(secret_name))


    ###########################################################################
    # Describe Secret
    ###########################################################################

    def test_describe_secret(self):
        s = secret.create_secret('test_describe_secret', string='secret')['Name']
        result = secret.describe_secret(s)
        self.assertEqual(s, result.get('Name'))
        
        secret.delete_secret(s, perma_delete=True)
        secret.wait_for_perma_delete(s)
        self.assertIsNone(secret.describe_secret(s))

    
    def test_describe_secret_nonexistent(self):
        s = secret.describe_secret('bogus')
        self.assertIsNone(s)

    
    ###########################################################################
    # Secret Exists
    ###########################################################################

    def test_secret_exists(self):
        s = secret.create_secret('test_secret_exists', string='secret')['Name']
        self.assertTrue(secret.secret_exists(s))
        secret.delete_secret(s, perma_delete=True)
        secret.wait_for_perma_delete(s)
        self.assertFalse(secret.secret_exists(s))

    
    def test_secret_exists_not_perma_deleted(self):
        s = secret.create_secret('test_secret_exists_not_perma_deleted', string='secret')['Name']
        secret.delete_secret(s)
        self.assertTrue(secret.secret_exists(s))
        secret.delete_secret(s, perma_delete=True)

    
    def test_secret_exists_nonexistent(self):
        self.assertFalse(secret.secret_exists('bogus'))

    ###########################################################################
    # Wait for Secret
    ###########################################################################

    def test_wait_for_secret_timeout(self):
        with self.assertRaises(TimeoutError):
            secret.wait_for_secret(self.STRING_SECRET['Name'], 'bogus', timeout=3)


    ###########################################################################
    # Get Secret by Tag
    ###########################################################################

    def test_get_secrets_by_tag_no_tags_found(self):
        tags = {
            "bogus": "b0gu5"
        }
        secrets = secret.get_secrets_by_tags(tags=tags)
        self.assertEqual(len(secrets), 0)
    
    def test_get_secrets_by_tag_no_desired_key(self):
        secret_tag = self.tag_x
        created_secret = self.JSON_SECRET_WITH_TAGS['SecretString']

        secrets = secret.get_secrets_by_tags(tags=secret_tag)
        self.assertEqual(len(secrets), 1)
        self.assertEqual(secrets[0], created_secret)
    
    def test_get_secrets_by_tag_desired_key_exists(self):
        secret_tag = self.tag_x
        created_secret = self.JSON_SECRET_WITH_TAGS['SecretString']

        secret_dict = json.loads(created_secret)
        secret_key = next(k for k in secret_dict)
        secret_value = secret_dict[secret_key]

        retrieved_secret_value = secret.get_secrets_by_tags(tags=secret_tag, desired_key=secret_key)
        self.assertEqual(len(retrieved_secret_value), 1)
        self.assertEqual(retrieved_secret_value[0], secret_value)
    
    def test_get_secrets_by_tag_desired_key_nonexistent(self):
        secret_tag = self.JSON_SECRET_WITH_TAGS['Tags'][0]
        secrets = secret.get_secrets_by_tags(tags=secret_tag, desired_key='b0gu53mpt1')
        self.assertEqual(len(secrets), 0)


    ###########################################################################
    # Secret Exists by Tag
    ###########################################################################

    def test_secret_exists_by_tags_no_tags_found(self):
        tags = {"bogus": "b0gu5"}
        self.assertFalse(secret.secret_exists_by_tags(tags=tags))
    
    def test_secret_exists_by_tags_exists(self):
        tags = self.tag_x
        self.assertTrue(secret.secret_exists_by_tags(tags=tags))
    
    def test_secret_exists_by_tags_inconclusive(self):
        tags = self.tag_w
        self.assertEqual(secret.secret_exists_by_tags(tags=tags), 'Inconclusive. There is more than one secret with the tags you have specified.')

    ###########################################################################
    # Test secrets utilities
    ###########################################################################

    def test_generate_random_password(self):
        password = util.generate_random_password()
        self.assertTrue(password.isalnum())
        self.assertGreater(len(password), 12)
        new_password = util.generate_random_password()
        self.assertNotEqual(password, new_password)


if __name__ == "__main__":
    unittest.main(verbosity=2)