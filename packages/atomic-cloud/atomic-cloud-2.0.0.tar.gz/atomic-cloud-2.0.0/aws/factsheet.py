from array import array
from os import path
from aws import ec2, rds, region, util
from aws.cluster import TEMPLATE_DIR
from jinja2 import Environment, FileSystemLoader
import boto3


def generate_cluster_factsheet(cluster_name: str, output_dir: str = '.'):
    '''
    Create factsheet for a cluster.

    :param cluster_name: The cluster name
    :param output_dir: The target directory for the factsheet file. Defaults to current working directory
    :return: None
    '''
    print(f'Generating cluster factsheet for {cluster_name}...')
    # validate input
    assert cluster_name, 'generate_cluster_factsheet() requires cluster_name'
    assert path.isdir(output_dir), 'generate_cluster_factsheet() requires a valid output_dir'

    # get template params
    params = {}
    try:
        eks_cluster = region.get_eks().describe_cluster(name=cluster_name).get('cluster', {})
        params = _get_template_params(eks_cluster)
    except region.get_eks().exceptions.ResourceNotFoundException:
        print(f'cluster {cluster_name} not found')
        return None

    # apply params to template
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), lstrip_blocks=True, trim_blocks=True, autoescape=True)
    template = env.get_template('factsheet/cluster-factsheet.md')
    filename = f'{cluster_name}-factsheet.md'
    template.stream(params).dump(path.join(output_dir, filename))
    return filename


def _get_template_params(eks_cluster: dict):
    params = {}

    # Basic Info
    cluster_name = eks_cluster['name']
    params['account'] = region.get_account_id()
    account_aliases = region.get_iam().list_account_aliases()['AccountAliases']
    params['accountAlias'] = account_aliases[0] if account_aliases else None
    params['region'] = region.get_session_region()
    params['clusterName'] = cluster_name
    params['clusterArn'] = eks_cluster['arn']
    params['kubenetesVersion'] = eks_cluster['version']

    # Networking
    vpc_id = eks_cluster['resourcesVpcConfig']['vpcId']
    vpc = ec2.get_vpc(False, None, vpc_id)
    ec2.set_current_vpcid(None, vpc_id)
    params['vpcId'] = vpc_id
    params['vpcName'] = util.get_tag_value(vpc, 'Name')
    params['vpcCidr'] = vpc['CidrBlock']
    subnet_ids = eks_cluster['resourcesVpcConfig']['subnetIds']
    subnets = ec2.get_subnets(subnet_ids)
    public_subnets = []
    private_subnets = []
    for subnet in subnets:
        s = {}
        s['id'] = subnet['SubnetId']
        s['name'] = util.get_tag_value(subnet, 'Name')
        s['az'] = subnet['AvailabilityZone']
        s['cidr'] = subnet['CidrBlock']
        if ec2.is_public_subnet(subnet['SubnetId']):
            public_subnets.append(s)
        else:
            private_subnets.append(s)

    params['publicSubnets'] = public_subnets
    params['privateSubnets'] = private_subnets

    security_groups = []
    security_groups.append( _get_security_group(eks_cluster['resourcesVpcConfig']['clusterSecurityGroupId']) )
    for sg_node_id in eks_cluster['resourcesVpcConfig']['securityGroupIds']:
        security_groups.append( _get_security_group(sg_node_id) )
    params['securityGroups'] = security_groups    

    # Node Groups
    nodegroups = _get_nodegroups(cluster_name)
    params['nodeGroups'] = nodegroups

    # Nodes
    params['nodes'] = _get_nodes(cluster_name)

    # IAM roles
    cluster_role_arn = eks_cluster['roleArn']
    params['clusterRoleName'] = _extract_role_name(cluster_role_arn)
    params['clusterRoleArn'] = cluster_role_arn
    if nodegroups:
        params['nodeRoleName'] = nodegroups[0]['nodeRoleName']
        params['nodeRoleArn'] = nodegroups[0]['nodeRoleArn']

    # RDS
    cluster_tag_name = cluster_name.replace('-cluster', '')
    rds_instances = rds.list_db_instances(None, None, cluster_tag_name)
    params['dbInstances'] = _parse_db_instances(rds_instances)
    
    return params


def _get_nodegroup(cluster_name:str, nodegroup_name:str):
    return region.get_eks().describe_nodegroup(
            clusterName=cluster_name,
            nodegroupName=nodegroup_name
        ).get('nodegroup', {})


def _get_nodegroups(cluster_name:str):
    nodegroup_names = region.get_eks().list_nodegroups(clusterName=cluster_name).get('nodegroups', [])
    list_nodegroups = []
    for group_name in nodegroup_names:
        node_group = _get_nodegroup(cluster_name, group_name)
        ng = {}
        ng['name'] = node_group['nodegroupName']
        ng['type'] = node_group.get('capacityType', '')
        ng['min'] = node_group['scalingConfig']['minSize']
        ng['max'] = node_group['scalingConfig']['maxSize']
        ng['desired'] = node_group['scalingConfig']['desiredSize']
        ng['nodeRoleArn'] = node_group['nodeRole']
        ng['nodeRoleName'] = _extract_role_name(node_group['nodeRole'])
        list_nodegroups.append(ng)

    return list_nodegroups


def _get_nodes(cluster_name:str):
    nodes = region.get_ec2().describe_instances(
        Filters=[{'Name' : 'tag:eks:cluster-name', 'Values': [cluster_name]}]
    ).get('Reservations', {})
    list_nodes = []
    for node in nodes:
        n = {}
        n['name'] = node['Instances'][0]['PrivateDnsName']
        n['nodeGroup'] = util.get_tag_value(node['Instances'][0], 'eks:nodegroup-name')
        n['instanceId'] = node['Instances'][0]['InstanceId']
        n['instanceType'] = node['Instances'][0]['InstanceType']
        list_nodes.append(n)

    return list_nodes


def _get_security_group(sgid:str):
    result = {}
    sg = ec2.get_sg(None, sgid)
    result['name'] = sg['GroupName']
    result['desc'] = sg['Description']
    result['id'] = sg['GroupId']
    result['inbounds'] = _parse_security_group_rules(sg['IpPermissions'], True)
    result['outbounds'] = _parse_security_group_rules(sg['IpPermissionsEgress'], False)

    return result


def _parse_security_group_rules(rules:array, inbound:bool):
    results = []

    target = 'source' if inbound else 'destination'

    for rule in rules:
        r = {}
        r['protocol'] = rule['IpProtocol'].upper() if rule['IpProtocol'] != '-1' else 'All'
        if 'FromPort' in rule:
            r['port'] = str(rule['FromPort']) + ' - ' + str(rule['ToPort'])
        else:
            r['port'] = 'All'

        for gp in rule['UserIdGroupPairs']:
            r['desc'] = gp.get('Description', '')
            sg_id = gp['GroupId']
            sg_name = ec2.get_sg(None, sg_id).get('GroupName')
            r[target] = sg_id + " / " + sg_name
            results.append(r)

        for ip in rule['IpRanges']:
            r['desc'] = ip.get('Description', '')
            r[target] = ip['CidrIp']
            results.append(r)

    return results


def _extract_role_name(arn:str):
    """
    Extract Role name from the specified role ARN
    Example:
    _extract_role_name('arn:aws:iam::123456789:role/np-refresh-nodes-role')
    return: 'np-refresh-nodes-role'
    """
    return arn.split('/',1)[1] 


def _parse_db_instances(db_instances:array):
    results = []
    for instance in db_instances:
        db = {}
        db['id'] = instance['DBInstanceIdentifier']
        db['size'] = instance['DBInstanceClass']
        db['engine'] = instance['Engine']
        db['engineVersion'] = instance['EngineVersion']
        db['endpoint'] = instance['Endpoint']['Address'] + ':' + str(instance['Endpoint']['Port'])
        db['az'] = instance['AvailabilityZone']
        db['multiAz'] = instance['MultiAZ']
        results.append(db)

    return results