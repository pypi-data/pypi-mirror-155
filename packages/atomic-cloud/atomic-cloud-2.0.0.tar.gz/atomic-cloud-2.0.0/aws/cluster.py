from aws import cfm, cert, ec2, region, lambda_fn
from aws.region import get_ec2
import os
from os import path
import boto3
from botocore.exceptions import ClientError
import re
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass


###########################################################################
# Constants
###########################################################################

@dataclass
class _StackTypes:
    certificate = 'certificate'
    vpc = 'vpc'
    cp = 'cp'
    eks_workers = 'eks-workers'
    rds = 'rds'
    ecr = 'ecr'
    s3_storage = 's3-storage'
    s3_hosting = 's3-hosting'
    lambda_function = 'lambda'



STACK_TYPES = _StackTypes()

MODULE_DIR = path.abspath(path.dirname(__file__))
TEMPLATE_DIR = path.join(MODULE_DIR, 'templates')
CFM_DIR = path.join(TEMPLATE_DIR, 'cfm')
LAMBDAS_DIR = path.join(MODULE_DIR, 'lambdas')


###########################################################################
# Helper Functions
###########################################################################

def _abs_path(file_name: str):
    '''
    Helper function to get the absolute path for a template file in the cfm_templates directory.
    '''
    return path.join(TEMPLATE_DIR, 'templates/cfm', file_name)


def _safe_domain(domain_name: str):
    '''
    Helper function to convert a domain to a safe resource name.
    All `.` will be replaced with `-`, and all non-alphanumeric characters (except `-`) will be stripped.
    '''
    return re.sub(r'[^a-zA-Z\d-]', '', domain_name.replace('.', '-'))


def _get_output(stack: dict, output_key: str):
    '''
    Helper function to get an OutputValue from the given stack
    '''
    return next((o['OutputValue'] for o in stack['Outputs'] if o.get('OutputKey') == output_key), None)


###########################################################################
# Wrapper Functions
###########################################################################

def create_cluster(config):
    '''
    Create all cluster resource stacks. This is the preferred way of creating a cluster.

    Note, if this function is interrupted or raises an exception, the resources that were successfully created will remain in AWS.
    Call :meth:`~aws.cluster.delete_cluster` to cleanup these resources.

    :param config: config object defined in a config.yaml file. Contains all information necessary to create a cluster.
    :return: A list of the created stacks
    '''
    # unpack config
    cluster_name = config['clusterName']
    base_domain = config['baseDomain']
    validation_domain = config['validationDomain']
    cidr_prefix = config['cidrPrefix']
    eks_version = config.get('eksVersion', '1.21')

    stacks = []

    cert = create_certificate(cluster_name, base_domain, validation_domain=validation_domain)
    stacks.append(cert)

    try:
        if region.get_default_region() != 'us-east-1':
            with region.use_region('us-east-1'):
                east1_cert = create_certificate(cluster_name, base_domain, validation_domain=validation_domain)
                stacks.append(east1_cert)
    except ClientError as e:
        # error thrown if using gov-cloud credentials
        if 'UnrecognizedClientException' in str(e):
            print(f'Skipping creation *.{base_domain} in region us-east-1.')
        else:
            raise e

    vpc = create_vpc(cluster_name, cidr_prefix=cidr_prefix)
    stacks.append(vpc)

    cp = create_cp(cluster_name, eks_version)
    stacks.append(cp)

    eks_workers = create_eks_workers(cluster_name, config['workerGroups'], is_cicd=config['isCicd'])
    stacks.append(eks_workers)

    rds = create_rds(cluster_name, config['databases'])
    stacks.append(rds)
    
    return stacks


def delete_cluster(cluster_name: str, keep_certs=False):
    '''
    Delete all cluster resources.

    If you want to delete and recreate a cluster without re-approving certificates, the parameter `keep_certs` can be used.

    :param cluster_name: The cluster name
    :param keep_certs: If set, certificates will not be deleted
    :return: None
    '''
    vpc_stack = get_vpc(cluster_name)
    vpc_id = _get_output(vpc_stack, 'VPC')
    delete_rds(cluster_name)
    delete_eks_workers(cluster_name)
    delete_cp(cluster_name)
    delete_all_eni_sg(vpc_id)
    delete_vpc(cluster_name)
    if not keep_certs:
        delete_certificates(cluster_name)
        try:
            if region.get_default_region() != 'us-east-1':
                with region.use_region('us-east-1'):
                    delete_certificates(cluster_name)
        except ClientError as e:
            # error thrown if using gov-cloud credentials
            if 'UnrecognizedClientException' in str(e):
                print('Skipping delete of cluster certificate in us-east-1.')
            else:
                raise e


def delete_all_eni_sg(vpc_id: str):
    ec2.set_current_vpcid(vpcid=vpc_id)
    network_interface_list = get_ec2().describe_network_interfaces(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]).get('NetworkInterfaces')
    for ni in network_interface_list:
        ni_description = ni.get('Description')
        print(ni_description)
        if ("Interface for NAT Gateway" in ni_description):
            continue
        ni_id = ni.get('NetworkInterfaceId')
        get_ec2().delete_network_interface(NetworkInterfaceId=ni_id)
    sg_list = ec2.list_sgs()
    for sg in sg_list:
        print(sg)
        if (sg.get("GroupName") == "default"):
            continue
        sg_id = ec2.get_sgid(sg)
        get_ec2().delete_security_group(GroupId=sg_id)

###########################################################################
# Certificate
###########################################################################

def create_certificate(cluster_name: str, base_domain: str, validation_domain: str = None, stack_name: str = None):
    '''
    Create certificate stack.

    :param cluster_name: The VPC class (`np`, `prd`, or `cicd`). If `np` the `cluster_name` will be prepended to the domain (`cluster_name.yourdomain.com`).
                      If `cicd`, `"cicd"` will be prepended to the domain (`cicd.yourdomain.com`). If `prd` the original domain will be used (`yourdomain.com`)
    :param base_domain: The domain name for which to request a certificate.
    :param validation_domain: The suffix of the address to which validation emails will be sent. Must be the same as, or a superdomain of, `domain_name`. Defaults to `domain_name`
    :param stack_name: optional stack name if it's not cluster specific. By default, stack_name is clusterName + templateName
    :return: The created stack
    '''
    domain_safe = _safe_domain(base_domain)

    params = {
        'clusterName': cluster_name,
        'baseDomain': base_domain,
        'DomainSafe': domain_safe,
        'ValidationDomain': validation_domain or base_domain,
    }

    tags = {
        'StackType': STACK_TYPES.certificate,
        'baseDomain': base_domain,
        'clusterName': cluster_name,
    }

    if stack_name is not None:
        params = {**params, 'stackName': stack_name}

    message = f'Certificate requested for *.{base_domain}.'

    existing_certs = cert.get_certificate(base_domain)
    if not existing_certs:
        print(message)
    elif existing_certs[0]['Status'] != 'FAILED':
        print('Certificate already created, skipping request')
        existing_stack_name = stack_name if stack_name is not None else cluster_name
        existing_stack_name = existing_stack_name + '-' + '00-cert'
        return cfm.get_stack(existing_stack_name)
    else:
        print('Certificate already created but failed. Will delete and recreate')
        cert.delete_cert(base_domain)

    return cfm.create_stack('00-cert', params=params, tags=tags)


def get_certificate(cluster_name: str, base_domain: str):
    '''
    Get certificate stack.

    :param cluster_name: The cluster name
    :param base_domain: The domain name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.certificate, clusterName=cluster_name, baseDomain=base_domain)


def get_cert_by_stack_name(stack_name: str):
    return cfm.find_stack(stackName=stack_name)


def delete_certificate(cluster_name: str, base_domain: str):
    '''
    Delete certificate stack.

    :param cluster_name: The cluster name
    :param base_domain: The domain name
    :return: None
    '''
    cert = get_certificate(cluster_name, base_domain)
    if cert:
        cfm.delete_stack(cert.get('StackName'))


def delete_certificates(cluster_name: str):
    '''
    Delete all certificate stack for a cluster (vpc).

    :param cluster_name: The cluster name
    :return: None
    '''
    certs = cfm.find_stacks(StackType=STACK_TYPES.certificate, clusterName=cluster_name)
    for cert in certs:
        cfm.delete_stack(cert['StackName'])


###########################################################################
# VPC
###########################################################################

def create_vpc(cluster_name: str, cidr_prefix: str):
    '''
    Create VPC stack.

    :param cluster_name: The cluster name
    :param cidr_prefix: The CIDR prefix.
    :return: The created stack
    '''
    params = {
        'CidrPrefix': cidr_prefix,
        'azs': ec2.list_azs(),
        'clusterName': cluster_name
    }

    tags = {
        'StackType': STACK_TYPES.vpc,
        'clusterName': cluster_name
    }

    vpc_stack = cfm.create_stack('01-vpc', params=params, tags=tags)

    # Provide name tag for the default route table and network ACL
    vpcid = cfm.get_output(vpc_stack, 'VPC')
    ec2.set_current_vpcid(vpcid=vpcid)

    default_rt_id = ec2.get_main_route_table()['RouteTableId']
    ec2.set_tag('Name', f'{cluster_name}-default-rt', resource_id=default_rt_id)

    network_acl_id = ec2.get_default_network_acl()['NetworkAclId']
    ec2.set_tag('Name', f'{cluster_name}-network-acl', resource_id=network_acl_id)

    return vpc_stack


def get_vpc(cluster_name: str):
    '''
    Get VPC stack

    :param cluster_name: The cluster name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.vpc, clusterName=cluster_name)


def delete_vpc(cluster_name: str):
    '''
    Delete VPC stack.

    :param cluster_name: The cluster name
    :return: None
    '''
    vpc = cfm.find_stack(StackType=STACK_TYPES.vpc, clusterName=cluster_name)
    if vpc:
        cfm.delete_stack(vpc.get('StackName'))


###########################################################################
# Control Plane
###########################################################################

def create_cp(cluster_name: str, eks_version: str):
    '''
    Create control plane stack. Must only be called after creating the VPC (:meth:`~aws.cluster.create_vpc`)

    :param cluster_name: The cluster name
    :param eks_version: The version of kubernetes used for the EKS cluster (optional)
    :return: The created stack
    '''
    params = {
        'azs': ec2.list_azs(),
        'clusterName': cluster_name,
        'eksVersion': eks_version
    }

    tags = {
        'StackType': STACK_TYPES.cp,
        'clusterName': cluster_name
    }

    return cfm.create_stack('02-eks-cp', params=params,
                            capabilities=['CAPABILITY_NAMED_IAM'], tags=tags)


def get_cp(cluster_name: str):
    '''
    Get control plane stack

    :param cluster_name: The cluster name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.cp, clusterName=cluster_name)


def delete_cp(cluster_name: str):
    '''
    Delete control plane stack.

    :param cluster_name: The cluster name
    :return: None
    '''
    cp = cfm.find_stack(StackType=STACK_TYPES.cp, clusterName=cluster_name)
    if cp:
        cfm.delete_stack(cp.get('StackName'))


###########################################################################
# EKS Workers
###########################################################################

def create_eks_workers(cluster_name: str, worker_groups, is_cicd: bool = False):
    '''
    Create EKS worker nodegroup stack. Must only be called after creating the control plane (:meth:`~aws.cluster.create_cp`)

    :param cluster_name: The cluster name
    :param worker_groups: The workerGroups list of dicts from the config file.
    :param is_cicd: Whether the workers are part of the cicd cluster. Used to give ECR and CloudFormation access roles.
    Optional, default is False.

    :return: The created stack
    '''
    instance_launch_args = '--enable-docker-bridge'

    params = {
        'InstanceLaunchArgs': instance_launch_args,
        'clusterName': cluster_name,
        'workerGroups': worker_groups,
        'isCicd': is_cicd
    }

    tags = {
        'StackType': STACK_TYPES.eks_workers,
        'clusterName': cluster_name
    }

    return cfm.create_stack('03-eks-workers', params=params,
                            capabilities=['CAPABILITY_NAMED_IAM'], tags=tags)


def get_eks_workers(cluster_name: str):
    '''
    Get EKS worker stack

    :param cluster_name: The cluster name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.eks_workers, clusterName=cluster_name)


def delete_eks_workers(cluster_name: str):
    '''
    Delete EKS worker stack.

    :param cluster_name: The VPC name
    :return: None
    '''
    eks_workers = cfm.find_stack(StackType=STACK_TYPES.eks_workers, clusterName=cluster_name)
    if eks_workers:
        cfm.delete_stack(eks_workers.get('StackName'))


###########################################################################
# RDS
###########################################################################

def get_db_resource_name(database):
    """
    Resource Names must be alphanumeric. Turns dBClusterId to CamelCase
    'test-rds-db' -> TestRdsDb
    return: The Resource Name
    """
    words = database['dBClusterId'].split('-')
    return ''.join(word.title() for word in words)


def create_rds(cluster_name: str, databases):
    '''
    Create RDS stack. Must only be called after creating the VPC (:meth:`~aws.cluster.create_vpc`)

    :param cluster_name: The cluster name
    :param databases: The list of database objects provided in the config file.
    :return: The created stack
    '''

    params = {
        'clusterName': cluster_name,
        'databases': databases
    }

    tags = {
        'StackType': STACK_TYPES.rds,
        'clusterName': cluster_name
    }

    stack = cfm.create_stack('04-rds', params=params,
                             capabilities=[cfm.CAPABILITY_NAMED_IAM], tags=tags)

    return stack


def get_rds(cluster_name: str):
    '''
    Get RDS stack

    :param cluster_name: The cluster name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.rds, clusterName=cluster_name)


def delete_rds(cluster_name: str):
    '''
    Delete RDS stack

    :param cluster_name: The cluster name
    :return: None
    '''
    rds = cfm.find_stack(StackType=STACK_TYPES.rds, clusterName=cluster_name)
    if rds:
        cfm.delete_stack(rds.get('StackName'))


###########################################################################
# ECR
###########################################################################

def create_ecr(app_name: str, cicd_cross_account_number: str = None, template_dir: str = CFM_DIR):
    '''
    Create ECR repository for an application. Must only be called after creating the VPC (:meth:`~aws.cluster.create_vpc`)

    :param app_name: The application name
    :param cicd_cross_account_number: The account number of the CICD environment if different from the current. Default is none.
    :param template_dir: Optional. Template directory that contains ecr.yml if using a custom ecr CloudFormation file.

    :return: The created stack
    '''
    params = {
        # ecr name must be lowercase
        'AppName': app_name.lower(),
        'CicdCrossAccountNumber': cicd_cross_account_number,
        'stackName': app_name
    }

    tags = {
        'StackType': STACK_TYPES.ecr,
        'AppName': app_name,
    }

    cfm.set_template_path(template_dir)
    return cfm.create_stack('ecr', params=params, tags=tags)


def get_ecr(app_name: str):
    '''
    Get the ECR repository for an application

    :param app_name: The application name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.ecr, AppName=app_name)


def delete_ecr(app_name: str):
    '''
    Delete ECR stack

    :param app_name: The application name
    :return: None
    '''
    ecr = cfm.find_stack(StackType=STACK_TYPES.ecr, AppName=app_name)
    if ecr:
        cfm.delete_stack(ecr.get('StackName'))


###########################################################################
# S3 Hosting
###########################################################################


def create_s3_hosting(cluster_name: str, app_name: str, domain_name: str, env_name: str, validation_domain: str = None):
    '''
    Create hosting resources for an application (S3 bucket and CloudFront distribution).
    Certificate will be requested if not exist.
    
    :param cluster_name: The cluster name
    :param app_name: The application name
    :param domain_name: The domain name
    :param env_name: environment name of the application
    :param validation_domain: root domain for validating the certificate

    :return: The created stack
    '''
    # remove *. if the input domain_name included it
    domain_name = domain_name.replace('*.', '')

    # construct stack_name to not use cluster_name by default
    stack_name = f'{app_name}-{env_name}'

    with region.use_region('us-east-1'):
        cert_list = cert.get_certificate(domain_name)
        if not cert_list:
            app_cert = create_certificate(cluster_name, domain_name, validation_domain, stack_name)
            app_cert_arn = _get_output(app_cert, 'OutputCertificate')
        else:
            print(f'Certificate {domain_name} already exists')
            app_cert_arn = cert_list[0]['CertificateArn']

    params = {
        'appName': app_name,
        'envName': env_name,
        'domainName': domain_name,
        'bucketName': domain_name,
        'DomainSafe': _safe_domain(domain_name),
        'certArn': app_cert_arn,
        'clusterName': cluster_name,
        'stackName': stack_name
    }

    tags = {
        'StackType': STACK_TYPES.s3_hosting,
        'clusterName': cluster_name,
        'appName': app_name,
        'domainName': domain_name,
        'envName': env_name
    }
    attempts = 0
    exception = None
    # stack will fail to create if a bucket with the same name already exists (even in another AWS account)
    # try creating new buckets with unique names, but the same domain name
    while attempts < 5:
        try:
            stack = cfm.create_stack('s3-hosting', params=params, tags=tags)
            return stack
        except Exception as e:
            # resolve bucket name conflicts
            params['bucketName'] = str(attempts) + '-' + domain_name
            print(f'Retrying with bucketName: {params["bucketName"]}')
            attempts += 1
            exception = e
    raise exception


def get_s3_hosting(cluster_name: str, app_name: str, env_name: str):
    '''
    Get the hosting resources for an application (S3 bucket and CloudFront distribution)

    :param cluster_name: The cluster name
    :param app_name: The application name
    :param env_name: The environment name
    :return: The created stack
    '''
    return cfm.find_stack(StackType=STACK_TYPES.s3_hosting, clusterName=cluster_name, appName=app_name, envName=env_name)


def delete_s3_hosting(cluster_name: str, app_name: str, env_name: str):
    '''
    Delete hosting stack

    :param cluster_name: The cluster name
    :param app_name: The application name
    :param env_name: The environment name
    :return: None
    '''
    hosting = cfm.find_stack(StackType=STACK_TYPES.s3_hosting, clusterName=cluster_name, appName=app_name, envName=env_name)
    if hosting:
        cfm.delete_stack(hosting.get('StackName'))
        bucket = _get_output(hosting, 'Bucket')
        if bucket:
            region.get_s3().delete_bucket(Bucket=bucket)
