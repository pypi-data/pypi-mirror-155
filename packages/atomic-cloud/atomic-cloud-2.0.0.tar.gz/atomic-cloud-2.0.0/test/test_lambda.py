import time
from unittest import TestCase, mock, main
import warnings
from aws import iam
from aws.lambda_fn import create_lambda_function, delete_lambda_function, get_lambda_function, list_lambda_functions, invoke_lambda_function


class TestLambda(TestCase):

    @classmethod
    def setUpClass(cls):
        # Hide boto3 warnings. This is a known issue with boto3 + unittest.
        warnings.simplefilter('ignore', category=ResourceWarning)

    def test_create_list_delete_function(self):
        
        try:
            create_lambda_function('unit-fn', 'arn:aws:iam::570208142024:role/atomic-cloud-role', 'lambda/lambda.handle', [], [], zip_fn = './test/templates/lambda.zip', desc = 'unit test lambda')

            lambdas = list_lambda_functions()
            found = False
            for l in lambdas:
                if l.get('FunctionName', '') == 'unit-fn':
                    found = True
                    continue
            self.assertTrue(found)
            self.assertIsNotNone(get_lambda_function('unit-fn'))
        finally:
            delete_lambda_function('unit-fn')

        post_lambdas = list_lambda_functions()
        found = False
        for l in post_lambdas:
            if l.get('FunctionName', '') == 'unit-fn':
                found = True
                continue
        self.assertFalse(found)
        self.assertIsNone(get_lambda_function('unit-fn'))

    def test_bad_get(self):
        self.assertIsNone(get_lambda_function('asdfasdfasdf'))
    
    def test_bad_delete(self):
        self.assertFalse(delete_lambda_function('asdfasdfasdf'))

    def test_nocode(self):
        try:
            create_lambda_function('asdf', 'asdf', 'asdf', [], [])
            self.fail()
        except Exception as e:
            self.assertNotEqual(e.args[0].find('Must provide code'), -1)

    def test_invoke(self):
        create_lambda_function('unit-fn', 'arn:aws:iam::570208142024:role/atomic-cloud-role', 'lambda/lambda.handle', [], [], zip_fn = './test/templates/lambda.zip', desc = 'unit test lambda')
        try:
            time.sleep(10)
            e = invoke_lambda_function('unit-fn', {'set': 'value1', 'also': 'value2'})
            self.assertEqual(e.get('statusCode'), 200)
            self.assertEqual(e.get('body', {}).get('set', None), 'value1')
            print(e)
        finally:
          delete_lambda_function('unit-fn')
        
    def test_invoke_bad(self):
        try:
            invoke_lambda_function('asdfasdf', {})
            self.fail()
        except Exception as e:
            self.assertNotEqual(e.args[0].find('Attempted to invoke lambda that does not exist'), -1)

if __name__ == "__main__":
    main()