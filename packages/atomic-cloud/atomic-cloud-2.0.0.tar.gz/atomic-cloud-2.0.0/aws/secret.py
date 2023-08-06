from aws.region import get_secret
from botocore.exceptions import ClientError
import json
import time


def get_secret_value(name: str, key: str = None):
    """
    Gets a secret's value. By default, this gets the string value. If that string is a json object, you can supply a key to get the value from.

    :param name: The name of the secret you're looking for. If this is a secret in your account, the 'friendly' name is acceptable. If you want a secret from another account, you need to supply the entire ARN.
    :param key: If the secret is a StringSecret, you can supply a key. If you do, we return the value of that key in the StringSecret parsed as JSON.
    """
    try:
        response = get_secret().get_secret_value(SecretId=name)
    except:
        return None  # secret doesn't exist

    if response.get('SecretString'):
        j = response.get('SecretString')
        if key:
            return json.loads(j).get(key)
        return j
    else:
        return response.get('SecretBinary')


def check_secret_has_all_tags(tags: dict, secret: dict):
    """
    Check if a secret has all the tags defined in tags.

    :param tags: The tags that you want to search the secrets by.
    :param secret: An element of the list returned by list_secrets.

    :returns: True if secret has all tags. False otherwise.
    """
    tags_in_secret = secret.get('Tags')
    total_matches = len(tags)
    num_matches = 0
    for key, value in tags.items():
        dictionary = {"Key": key, "Value": value}
        if dictionary in tags_in_secret:
            num_matches = num_matches + 1

    return num_matches == total_matches


def get_secrets_by_tags(tags: dict, desired_key: str = None):
    """
    Gets the values from secrets that have tags that match those passed in. By default, this gets the string value.
    If that string is a json object, you can supply a key to get the value from.

    :param tags: The tags that you want to search the secrets by. Should be in form {'key1': 'value1', 'key2': 'value2}
    :param desired_key: If the secret is a StringSecret, you can supply a key.
    If you do, we return the value of that key in the StringSecret parsed as JSON.
    :return: list of secret values
    """

    filters = [
        {
            'Key': 'tag-key',
            'Values': list(tags.keys())
        },
        {
            'Key': 'tag-value',
            'Values': list(tags.values())
        }
    ]

    secrets_remain = True
    all_secrets = []
    token = None
    try:
        while secrets_remain:
            if token:
                secrets = get_secret().list_secrets(Filters=filters, NextToken=token)
            else:
                secrets = get_secret().list_secrets(Filters=filters)
            secrets_list = secrets.get('SecretList')
            for secret in secrets_list:
                if check_secret_has_all_tags(tags, secret):
                    all_secrets.append(secret.get('Name'))
            if 'NextToken' in secrets:
                token = secrets['NextToken']
            secrets_remain = 'NextToken' in secrets
    except ClientError:
        return []
    returned_secrets = []
    for secret_name in all_secrets:
        secret_value = get_secret_value(name=secret_name, key=desired_key)
        if secret_value:
            returned_secrets.append(secret_value)
    return returned_secrets


def create_secret(name: str, description: str = "", binary: bytes = None, string: str = None, kvp: dict = None,
                  tags: dict = {}):
    """
  Creates a secret with either a binary or string/json value. You cannot supply both a binary and string value,
  but you must supply one.

  :param name: The (friendly) name of the secret you're creating. Must be unique.
  :param description: The description of that secret (optional).
  :param binary: Binary data to store in the secret. 
  :param string: String value to store in the secret. If this is a valid json dict, you can access a key using our get_secret_value() function.
  :param tags: dict of key/value pairs to set as tags on the secret (optional).
  """
    if (binary is not None and (string or kvp)) or (string and kvp):
        raise Exception("You cannot provide multiple types of values for one secret.")

    formatted_tags_list = [{'Key': key, 'Value': value} for key, value in tags.items()]

    if kvp:
        string = json.dumps(kvp)

    if binary:
        r = get_secret().create_secret(Name=name, Description=description, SecretBinary=binary,
                                       Tags=formatted_tags_list)
    else:  # string
        r = get_secret().create_secret(Name=name, Description=description, SecretString=string,
                                       Tags=formatted_tags_list)

    # add to r
    r['Description'] = description
    if binary:
        r['SecretBinary'] = binary
    else:
        r['SecretString'] = string
    if tags:
        r['Tags'] = formatted_tags_list
    return r


def update_secret(name: str, binary=None, string: str = None, kvp: dict = None, overwrite_json: bool = False):
    """
  Updates a secret. If you supply a binary or string, that becomes the new value of the secret. If you supply a dict, that dict's values
  are added to the json-formatted string in the secret (or overwrites the string if it was not json).

  :param name: The name of the secret you're updating. If the secret is in your account, this can be the 'friendly' name or ARN. Otherwise, it must be the ARN.
  :param binary: Binary data to update the secret with. Overwrites the content of the secret.
  :param string: String to update the secret with. Overwrites the content of the secret.
  :param kvp: Dictionary of string/string pairs to update the secret with. These pairs get added to the existing json dictionary (if it exists).
  :param overwrite_json: If this is true, kvp will overwrite an existing dictionary rather than add its pairs to it (defaults to False).
  """

    if (binary is not None and (string or kvp)) or (string and kvp):
        raise Exception("You cannot provide multiple types of values for one secret.")

    existing = get_secret_value(name)
    try:
        existing_json = json.loads(existing)
        use_json = True
    except:
        use_json = False
    if use_json:
        if overwrite_json:
            secret_string = json.dumps(kvp)
            r = get_secret().update_secret(SecretId=name, SecretString=secret_string)
            r['SecretString'] = wait_for_secret(name, value=secret_string)
        else:
            for k in kvp:
                existing_json[k] = kvp[k]
            secret_string = json.dumps(existing_json)
            r = get_secret().update_secret(SecretId=name, SecretString=secret_string)
            r['SecretString'] = wait_for_secret(name, value=secret_string)
    elif type(existing) is str:
        r = get_secret().update_secret(SecretId=name, SecretString=string)
        r['SecretString'] = wait_for_secret(name, value=string)
    else:  # binary
        r = get_secret().update_secret(SecretId=name, SecretBinary=binary)
        r['SecretBinary'] = wait_for_secret(name, value=binary)
    return r


def delete_secret(name: str, recovery_window: int = None, perma_delete: bool = False):
    """
  Deletes a secret. We do not recommend using the permanent deletion feature for otherwise inaccessible secrets!

  :param name: The name of the secret you're deleting. If the secret is in your account, this can be the 'friendly' name or ARN. Otherwise, it must be the ARN.
  :param recovery_window: The amount of days to wait before permanently deleting the secret. Minimum is 7, maximum is 30. Defaults to 7. Cannot be present if perma_delete is True.
  :param perma_delete: If True, we delete the secret permanently (without a 7-30 day recovery window). Cannot be True if recovery_window is supplied. Defaults to False.
  """
    if recovery_window and perma_delete:
        raise Exception("You cannot both specify a recovery window and force deletion without a recovery window")
    if not recovery_window or recovery_window < 7:
        recovery_window = 7
    if recovery_window > 30: recovery_window = 30
    try:
        if perma_delete:
            get_secret().delete_secret(SecretId=name, ForceDeleteWithoutRecovery=True)
            wait_for_secret(name, value=None)
            return True
        else:
            get_secret().delete_secret(SecretId=name, RecoveryWindowInDays=recovery_window)
            wait_for_secret(name, value=None)
    except:
        return False  # the secret doesn't exist
    return recovery_window


def describe_secret(name: str):
    """
  Get all the metadata associated with this secret. Does not return secret values.

  :param name: The secret name
  :return: The secret if it exists, else None
  """
    client = get_secret()
    try:
        res = client.describe_secret(SecretId=name)
        return res
    except client.exceptions.ResourceNotFoundException:
        return None


def secret_exists(name: str):
    """
  Whether this secret exists.
  Note, secrets that have not been perma-deleted but are pending deletion with a recovery window, still exist.

  :param name: The secret name
  :return: True if the secret exists, else False
  """
    return True if describe_secret(name) else False


def secret_exists_by_tags(tags: dict):
    """
  Whether this secret exists. This is determined by searching for all the secrets that have the passed in tags.

  :param tags: The tags to search the secrets by
  :return: True if there is one secret that matches the tags, False if there are no secrets that match the tags, a string if there are multiple secrets that match the tags.
  """
    result = get_secrets_by_tags(tags=tags)
    if len(result) == 0:
        return False
    elif len(result) == 1:
        return True
    else:
        return 'Inconclusive. There is more than one secret with the tags you have specified.'


def wait_for_perma_delete(name: str):
    """
  Wait for secret to be permanently deleted. Usually takes 10-30 seconds. Times out after 90 seconds.

  :param name: The secret name
  """
    t = 0
    while secret_exists(name) and t < 90:
        time.sleep(1)
        t += 1


def restore_secret(name: str):
    """
  Restores a deleted secret if it is within the recovery window time period. Waits until the value is retrievable.

  :param name: The name of the secret to restore.
  """
    get_secret().restore_secret(SecretId=name)
    wait_for_secret(name, restore=True)


def wait_for_secret(name: str, value=None, timeout: int = 60, restore=False):
    """
    Wait for a secret to have the given value. (value == get_secret_value(name))
    This is useful for synchronization purposes, as updates to secrets are not always immediately reflected in subsequent requests.

    :param name: The name of the secret to wait on.
    :param value: The value to wait for. If None, will wait for secret to be deleted.
    :param timeout: The maximum time to wait, after which an Exception will be thrown. Default is 60 seconds.
    :param restore: Whether you are trying to restore the secret. Default is False.
    :return: The secret value, once it matches
    """

    def ensure_stability():
        """
        NOTE: This is a temporary workaround. Should probably find a more stable solution in the future.

        Make sure the value is stable.
        Even after successfully reading the new value, an issue on the AWS side can sometimes cause a subsequent read to return the old value.
        (Probably, due to a replication synchronization issue)
        In practice, have only seen this happen one time before stabilizing. To be safe, wait for 5 consecutive accurate reads.
        """
        consecutively_correct = 0
        while consecutively_correct < 5:
            val = get_secret_value(name)
            if val == value or (restore and val is not None):
                consecutively_correct += 1
            else:
                consecutively_correct = 0
        time.sleep(1)

    for _ in range(timeout):
        found = get_secret_value(name)
        if found == value or (restore and found is not None):
            ensure_stability()
            return found
        else:
            time.sleep(1)

    raise TimeoutError('Secret did not change to the expected value')
