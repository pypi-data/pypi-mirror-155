# Fact Sheet: cluster {{clusterName}}


## Basic Info

{% if accountAlias %}
**AWS Account:** [{{account}} ({{accountAlias}})](https://{{accountAlias}}.signin.aws.amazon.com/console)
{% else %}
**AWS Account:** [{{account}}](https://{{account}}.signin.aws.amazon.com/console)
{% endif %}

**Region:** {{region}}

**Kubernetes Version:** {{kubenetesVersion}}

**Cluster ARN:** [{{clusterArn}}](https://console.aws.amazon.com/eks/home?region={{region}}#/clusters/{{clusterName}}) 

## Networking

**VPC ID:** {{vpcId}}

**VPC Name:** {{vpcName}}

**CIDR:** {{vpcCidr}}

**Subnets:** 
| Type | Availability Zone | CIDR Range | ID (Link) |
| ---- | ----------------- | ---------- | ---------- |
{% for ps in privateSubnets %}
| Private | {{ps.az}} | {{ps.cidr}} | [{{ps.id}}](https://console.aws.amazon.com/vpc/home?region={{region}}#subnets:SubnetId={{ps.id}};sort=VpcId) |
{% endfor %}
{% for ps in publicSubnets %}
| Public | {{ps.az}} | {{ps.cidr}} | [{{ps.id}}](https://console.aws.amazon.com/vpc/home?region={{region}}#subnets:SubnetId={{ps.id}};sort=VpcId) |
{% endfor %}

**Security Groups:**

{% for sg in securityGroups %}
 1. **Name**: {{sg.name}}

    **Description**: {{sg.desc}}

    **ID (Link)**: [{{sg.id}}](https://console.aws.amazon.com/ec2/v2/home?region={{region}}#SecurityGroups:group-id={{sg.id}}) 

    **Inbound Rules**: 
    {% if sg.inbounds|length > 0 %}
    | Protocol | Port Range | Source | Description|
    | -------- | ---------- |--------| -----------|
    {% for ib in sg.inbounds %}
    | {{ib.protocol}} | {{ib.port}} | {{ib.source}} | {{ib.desc}} |
    {% endfor %}
    {% else %}
     None
    {% endif %}

    **Outbound Rules**: 
    {% if sg.outbounds|length > 0 %}
    | Protocol | Port Range | Destination | Description|
    | -------- | ---------- |-------------| -----------|
    {% for ob in sg.outbounds %}
    | {{ob.protocol}} | {{ob.port}} | {{ob.destination}} | {{ob.desc}} |
    {% endfor %}
    {% else %}
     None
    {% endif %}
{% endfor %}


## Node Groups
| Group Name | Capacity Type | Minimum Size | Maximum Size | Desired Size |
| ---------- | ------------- | ------------ | ------------ | ------------ |
{% for ng in nodeGroups %}
| {{ng.name}}| {{ng.type}} | {{ng.min}} | {{ng.max}} | {{ng.desired}} |
{% endfor %}


## Nodes
| Node Name | Instance ID | Instance Type | Node Group | 
| --------- | ----------- | ------------- | ---------- |
{% for n in nodes %}
| {{n.name}}| [{{n.instanceId}}](https://console.aws.amazon.com/ec2/v2/home?region={{region}}#InstanceDetails:instanceId={{n.instanceId}}) | {{n.instanceType}} | {{n.nodeGroup}} |
{% endfor %}


## IAM Roles
| Name | Description | ARN (Link) |
| ---- | ----------- | ---------- |
| {{clusterRoleName}} | Control Plane Role | [{{clusterRoleArn}}](https://console.aws.amazon.com/iam/home?{{region}}#/roles/{{clusterRoleName}}) |
| {{nodeRoleName}} | Worker Nodes Role | [{{nodeRoleArn}}](https://console.aws.amazon.com/iam/home?{{region}}#/roles/{{nodeRoleName}}) |


### RDS Instances
 {% if dbInstances|length > 0 %}
| Identifier (Link) | Engine (Version) | Size | Endpoint | Region&AZ | Multi-AZ |
| ----------------- | ---------------- | ---- | -------- | --------- | -------- |
{% for i in dbInstances %}
| [{{i.id}}](https://console.aws.amazon.com/rds/home?region={{region}}#database:id={{i.id}};is-cluster=false) | {{i.engine}} ({{i.engineVersion}}) | {{i.size}} | {{i.endpoint}} | {{i.az}} | {% if i.multiAz %} Yes {% else %} No {% endif %} |
{% endfor %}
{% else %}
    None
{% endif %}
