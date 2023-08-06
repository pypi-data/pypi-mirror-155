from aws.region import get_lambda

import json
import time


# Here we'll have functions dealing with lambdas. Upload, trigger, delete, list/get, potentially update code?

def create_lambda_function(name: str, role: str,
                    handler: str,
                    subnets: list,
                    security_groups: list,
                    s3: dict = None,
                    zip_fn: str = None,
                    desc: str = None,
                    runtime: str = 'python3.8',
                    env: dict = {},
                    layers: list = [], 
                    timeout: int = 5
                    ):
    """
    Creates a lambda function from either a zip file or an S3 bucket

    :param name: the name of the function.
    :param handler: what function to invoke when the lambda is called (needs event and context params).
    :param subnets: list of subnet ids to host the lambda in.
    :param security_groups: list of security groups for access control.
    :param s3: s3 bucket + key to get the code from. format: {'S3Bucket': bucketname, 'S3Key': filename.zip}. Leave None if zip is local.
    :param zip_fn: filename of the zipfile the code + libs is in. Leave none if zip is in s3.
    :param desc: a short description of the lambda function.
    :param runtime: the runtime to use for the function. Python 3.8 is almost certainly what you want.
    :param env: key/value pairs of environment variables to set on the function's container.
    :param layers: list of layers to include with the function.
    :param timeout: number of seconds to let the function run before timing out.
    """

    vpc_config = {
        'SubnetIds': subnets,
        'SecurityGroupIds': security_groups
    }

    if s3:
        code = s3
    elif zip_fn:
        with open(zip_fn, 'rb') as z:
            c = z.read()
        code = {'ZipFile': c} 
    else:
        raise Exception('Must provide code for the function as either a zip file or s3 bucket arn')

    return get_lambda().create_function(FunctionName = name,
                                        Role = role,
                                        Handler = handler,
                                        Code = code,
                                        VpcConfig = vpc_config,
                                        Layers = layers,
                                        Timeout = timeout,
                                        Runtime = runtime,
                                        Environment = {'Variables': env})

    
def invoke_lambda_function(name: str, body: dict):
    """
    Runs a lambda function with the supplied body.

    :param name: the name of the lambda you're invoking.
    :param body: the json you would like to supply to the function as an event.
    :return: the response to the invocation, including `statusCode` and `body`.
    """
    if not get_lambda_function(name):
        raise Exception('Attempted to invoke lambda that does not exist')

    event = json.dumps(body)
    response = get_lambda().invoke(FunctionName = name, InvocationType = 'RequestResponse', LogType = 'Tail', Payload = bytes(event, 'utf-8'))
    return json.loads(response['Payload'].read().decode())


def delete_lambda_function(name: str):
    """
    Deletes a lambda function

    :param name: the name of the lambda you're deleting.
    :return: True if deleted, False if not found.
    """
    lams = list_lambda_functions()
    for l in lams:
        if l.get('FunctionName', '') == name:
          get_lambda().delete_function(FunctionName = name)
          return True
    return False


def get_lambda_function(name: str):
    """
    Retrieves a lambda function's details

    :param name: the name of the lambda you're searching for.
    :return: a dict containing details on that lambda if it exists. Otherwise, returns None.
    """
    lams = list_lambda_functions()
    for l in lams:
        if l.get('FunctionName', '') == name:
          return l
    return None


def list_lambda_functions():
    """
    Lists lambda functions

    :return: a list of the lambda functions in your aws account
    """
    lam = []
    more = True
    marker = None
    while more:
        if marker:
            fns = get_lambda().list_functions(Marker = marker)
        else:
            fns = get_lambda().list_functions()
        lam.extend(fns.get('Functions', []))
        marker = fns.get('NextMarker', False)
        more = marker
    return lam


def update_function_code(function: str, filepath: str):
    """
    Update lambda function code from a zip file.

    :param function: The lambda function name
    :param filepath: The file path to the zip file containing the code
    """
    with open(filepath, 'rb') as file:
        filebytes = file.read()

    get_lambda().update_function_code(
        FunctionName=function,
        ZipFile=filebytes,
        Publish=True
    )


def wait_for_lambda(name: str):
    """
    Wait for lambda to finish updating

    :param function: The lambda function name
    :return: True if lambda readies within 2 minutes
    """
    for _ in range(120):
        function = get_lambda().get_function(FunctionName = name)
        if function['Configuration']['LastUpdateStatus'] == 'Successful':
            return True
        else:
            time.sleep(1)

    raise TimeoutError('Lambda did not finish updating within 2 minutes.')