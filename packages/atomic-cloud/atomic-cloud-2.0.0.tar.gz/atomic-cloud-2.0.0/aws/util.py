import yaml

from aws import region


def format_filter(name, value):
    '''
    Convert a filter name and value into boto3 filter format
    
    :param name: filter name to search on
    :param value: filter value to search on
    :return: The formated filter dict

    Example::

        format_filter('vpc-id', 'vpc-0dbb013f82b6694e9')
        
        {
            'Name': 'vpc-id',
            'Values': [
                'vpc-0dbb013f82b6694e9'
            ]
        }
    '''
    return {'Name': name, 'Values': [value]}


def format_filters(filters: dict):
    '''
    Convert a dictionary of filters into boto3 filter format

    :param filters: A dictionary of filters
    :return: The formatted filter dict

    Example::
    
        format_filters({
            'vpc-id', 'vpc-0dbb013f82b6694e9',
            'default', 'true'
        })

        [
            {
                'Name': 'vpc-id',
                'Values': [
                    'vpc-0dbb013f82b6694e9'
                ]
            },
            {
                'Name': 'default',
                'Values': [
                    'true'
                ]
            }
        ]
    '''
    return [format_filter(key, value) for key, value in filters.items()]


def get_tag_value(resource: dict, tag_key: str, tag_prop: str = 'Tags'):
    """
    Get the tag value of the specified key on the specified resource 
    :param resource: resource to get the tag from
    :param tag_key: value of the tag key
    :param tag_prop: optional value of the tag property on the resource. Mostly AWS resource has 'Tags' as the resource property, but some resource is using 'TagList'
    :return: the value of the tag
    """
    if resource and resource[tag_prop]:
        tag_name = [t for t in resource[tag_prop] if t['Key'] == tag_key]
        return tag_name[0]['Value'] if tag_name else ''
    else:
        return ''


def read_yaml(fn: str):
    """
    Reads a YAML file and returns the resulting the object.

    Example
    -------

    >>> read_yaml('tomcat-deploy-dev.yml')

    """
    assert fn, 'read_yaml() called without filename.'

    file = None
    try:
        file = open(fn)
        return yaml.safe_load(file)

    finally:
        if file is not None:
            file.close()


def generate_random_password():
    """
    Returns a random password string with 18 alphanumeric characters.
    """
    s3_client = region.get_secret()
    try:
        response = s3_client.get_random_password(
            PasswordLength=18,
            ExcludeCharacters="",
            ExcludeNumbers=False,
            ExcludePunctuation=True,
            ExcludeUppercase=False,
            ExcludeLowercase=False,
            IncludeSpace=False,
            RequireEachIncludedType=True
        )
        return response['RandomPassword']
    except Exception as e:
        print('Failed to generate random password')
        raise e


def generate_random_string(length: int):
    """
    Returns a random password string with 18 alphanumeric characters.
    """
    s3_client = region.get_secret()
    try:
        response = s3_client.get_random_password(
            PasswordLength=length,
            ExcludeCharacters="",
            ExcludeNumbers=False,
            ExcludePunctuation=True,
            ExcludeUppercase=False,
            ExcludeLowercase=False,
            IncludeSpace=False,
            RequireEachIncludedType=True
        )
        return response['RandomPassword']
    except Exception as e:
        print('Failed to generate random string')
        raise e