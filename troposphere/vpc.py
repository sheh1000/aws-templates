# Converted from VPC_With_VPN_Connection.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

from troposphere import Parameter, Ref, Tags, Template, Output, Base64, GetAtt, FindInMap, Join
from troposphere import ec2 as ec2
import troposphere.policies

t = Template()

t.add_version("2010-09-09")

t.add_description("""\
AWS CloudFormation Sample Template:\
Includes:\
VPC, Public subnet, Private subnet, Gateway\
""")

# ##################
""" METADATA """
stack_tags = Tags(
    Application=Ref("AWS::StackName")
)

# ##################
""" PARAMETERS """
# newtworking parameters
cidr_vpc = t.add_parameter(Parameter(
    "VPCCIDR",
    ConstraintDescription=(
        "must be a valid IP CIDR range of the form x.x.x.x/x."),
    Description="IP Address range for the VPN connected VPC",
    Default="10.1.0.0/16",
    MinLength="9",
    AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
    MaxLength="18",
    Type="String",
))

cidr_public = t.add_parameter(Parameter(
    "PUBLICCIDR",
    ConstraintDescription=(
        "must be a valid IP CIDR range of the form x.x.x.x/x."),
    Description="IP Address range for the Public Subnet",
    Default="10.1.1.0/24",
    MinLength="9",
    AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
    MaxLength="18",
    Type="String",
))

cidr_private = t.add_parameter(Parameter(
    "PRIVATECIDR",
    ConstraintDescription=(
        "must be a valid IP CIDR range of the form x.x.x.x/x."),
    Description="IP Address range for the Private Subnet",
    Default="10.1.2.0/24",
    MinLength="9",
    AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
    MaxLength="18",
    Type="String",
))

sshlocation_param = t.add_parameter(Parameter(
    'SSHLocation',
    Description=' The IP address range that can be used to SSH to the EC2 \
instances',
    Type='String',
    MinLength='9',
    MaxLength='18',
    Default='0.0.0.0/0',
    AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
    ConstraintDescription=(
        "must be a valid IP CIDR range of the form x.x.x.x/x."),
))


# EC2 parameters
keyname_param = t.add_parameter(Parameter(
    'KeyName',
    ConstraintDescription='must be the name of an existing EC2 KeyPair.',
    Description='Name of an existing EC2 KeyPair to enable SSH access to the instance',
    Type='AWS::EC2::KeyPair::KeyName',
))

instanceType_param = t.add_parameter(Parameter(
    'InstanceType',
    Type='String',
    Description='WebServer EC2 instance type',
    Default='t2.micro',
    AllowedValues=[
        't1.micro', 't2.micro', 't2.small', 't2.medium',
        'm1.small', 'm1.medium', 'm1.large', 'm1.xlarge',
        'm2.xlarge', 'm2.2xlarge', 'm2.4xlarge', 'm3.medium', 'm3.large', 'm3.xlarge', 'm3.2xlarge',
        'c1.medium', 'c1.xlarge', 'c3.large', 'c3.xlarge', 'c3.2xlarge', 'c3.4xlarge', 'c3.8xlarge',
        'g2.2xlarge',
        'r3.large', 'r3.xlarge', 'r3.2xlarge', 'r3.4xlarge', 'r3.8xlarge',
        'i2.xlarge', 'i2.2xlarge', 'i2.4xlarge', 'i2.8xlarge',
        'hi1.4xlarge',
        'hs1.8xlarge',
        'cr1.8xlarge',
        'cc2.8xlarge',
        'cg1.4xlarge',
    ],
    ConstraintDescription='must be a valid EC2 instance type.',
))

# ##################
""" MAPPINGS """
t.add_mapping('AWSInstanceType2Arch', {
    't1.micro': {'Arch': 'PV64'},
    't2.micro': {'Arch': 'HVM64'},
    't2.small': {'Arch': 'HVM64'},
    't2.medium': {'Arch': 'HVM64'},
    'm1.small': {'Arch': 'PV64'},
    'm1.medium': {'Arch': 'PV64'},
    'm1.large': {'Arch': 'PV64'},
    'm1.xlarge': {'Arch': 'PV64'},
    'm2.xlarge': {'Arch': 'PV64'},
    'm2.2xlarge': {'Arch': 'PV64'},
    'm2.4xlarge': {'Arch': 'PV64'},
    'm3.medium': {'Arch': 'HVM64'},
    'm3.large': {'Arch': 'HVM64'},
    'm3.xlarge': {'Arch': 'HVM64'},
    'm3.2xlarge': {'Arch': 'HVM64'},
    'c1.medium': {'Arch': 'PV64'},
    'c1.xlarge': {'Arch': 'PV64'},
    'c3.large': {'Arch': 'HVM64'},
    'c3.xlarge': {'Arch': 'HVM64'},
    'c3.2xlarge': {'Arch': 'HVM64'},
    'c3.4xlarge': {'Arch': 'HVM64'},
    'c3.8xlarge': {'Arch': 'HVM64'},
    'g2.2xlarge': {'Arch': 'HVMG2'},
    'r3.large': {'Arch': 'HVM64'},
    'r3.xlarge': {'Arch': 'HVM64'},
    'r3.2xlarge': {'Arch': 'HVM64'},
    'r3.4xlarge': {'Arch': 'HVM64'},
    'r3.8xlarge': {'Arch': 'HVM64'},
    'i2.xlarge': {'Arch': 'HVM64'},
    'i2.2xlarge': {'Arch': 'HVM64'},
    'i2.4xlarge': {'Arch': 'HVM64'},
    'i2.8xlarge': {'Arch': 'HVM64'},
    'hi1.4xlarge': {'Arch': 'HVM64'},
    'hs1.8xlarge': {'Arch': 'HVM64'},
    'cr1.8xlarge': {'Arch': 'HVM64'},
    'cc2.8xlarge': {'Arch': 'HVM64'},
})

t.add_mapping('AWSRegionArch2AMI', {
    'us-east-1': {'PV64': 'ami-50842d38', 'HVM64': 'ami-08842d60',
                  'HVMG2': 'ami-3a329952'},
    'us-west-2': {'PV64': 'ami-af86c69f', 'HVM64': 'ami-8786c6b7',
                  'HVMG2': 'ami-47296a77'},
    'us-west-1': {'PV64': 'ami-c7a8a182', 'HVM64': 'ami-cfa8a18a',
                  'HVMG2': 'ami-331b1376'},
    'eu-west-1': {'PV64': 'ami-aa8f28dd', 'HVM64': 'ami-748e2903',
                  'HVMG2': 'ami-00913777'},
    'ap-southeast-1': {'PV64': 'ami-20e1c572', 'HVM64': 'ami-d6e1c584',
                       'HVMG2': 'ami-fabe9aa8'},
    'ap-northeast-1': {'PV64': 'ami-21072820', 'HVM64': 'ami-35072834',
                       'HVMG2': 'ami-5dd1ff5c'},
    'ap-southeast-2': {'PV64': 'ami-8b4724b1', 'HVM64': 'ami-fd4724c7',
                       'HVMG2': 'ami-e98ae9d3'},
    'sa-east-1': {'PV64': 'ami-9d6cc680', 'HVM64': 'ami-956cc688',
                  'HVMG2': 'NOT_SUPPORTED'},
    'cn-north-1': {'PV64': 'ami-a857c591', 'HVM64': 'ami-ac57c595',
                   'HVMG2': 'NOT_SUPPORTED'},
    'eu-central-1': {'PV64': 'ami-a03503bd', 'HVM64': 'ami-b43503a9',
                     'HVMG2': 'ami-b03503ad'},
})


# ##################
""" CONDITIONS """


# ##################
""" RESOURCES """
stack_vpc = t.add_resource(
    ec2.VPC(
        "VPC",
        EnableDnsSupport="true",
        CidrBlock=Ref(cidr_vpc),
        EnableDnsHostnames="true",
        Tags=Tags(
            Application=Ref("AWS::StackName"),
            Network="VPC + public + private",
        )
    )
)

subnet_public = t.add_resource(ec2.Subnet(
    'PublicSubnet',
    CidrBlock=Ref(cidr_public),
    MapPublicIpOnLaunch=False,
    VpcId=Ref(stack_vpc),
))

subnet_private = t.add_resource(ec2.Subnet(
    'PrivateSubnet',
    CidrBlock=Ref(cidr_private),
    MapPublicIpOnLaunch=False,
    VpcId=Ref(stack_vpc),
))


#  Internet gateway and NAT instances
igw = t.add_resource(ec2.InternetGateway('InternetGateway',))
t.add_resource(ec2.VPCGatewayAttachment("GWAttachmnent",
                                        VpcId=Ref(stack_vpc),
                                        InternetGatewayId=Ref(igw)))
nat_eip = t.add_resource(ec2.EIP(
    'NatEip',
    Domain="vpc",
))

nat = t.add_resource(ec2.NatGateway(
    'Nat',
    AllocationId=GetAtt(nat_eip, 'AllocationId'),
    SubnetId=Ref(subnet_public),
))


# route tables
rt_public = t.add_resource(ec2.RouteTable(
    "RouteTablePublic",
    VpcId=Ref(stack_vpc),
    Tags=stack_tags,
))

rt_private = t.add_resource(ec2.RouteTable(
    'RouteTablePrivate',
    VpcId=Ref(stack_vpc),
    Tags=stack_tags,
))

# route associacions
public_route_association = t.add_resource(ec2.SubnetRouteTableAssociation(
    'PublicRouteAssociation',
    SubnetId=Ref(subnet_public),
    RouteTableId=Ref(rt_public),
))

private_route_association = t.add_resource(ec2.SubnetRouteTableAssociation(
    'PrivateRouteAssociation',
    SubnetId=Ref(subnet_private),
    RouteTableId=Ref(rt_private),
))


# routes for public table
t.add_resource(ec2.Route(
    'PublicDefaultRoute',
    RouteTableId=Ref(rt_public),
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=Ref(igw),
))

# routes for private table
t.add_resource(ec2.Route(
    'NatRoute',
    RouteTableId=Ref(rt_private),
    DestinationCidrBlock='0.0.0.0/0',
    NatGatewayId=Ref(nat),
))

# network acls
public_subnet_acl = t.add_resource(ec2.NetworkAcl(
    'NetworkAcl',
    VpcId=Ref(stack_vpc),
    Tags=stack_tags,
))

subnetNetworkAclAssociation = t.add_resource(ec2.SubnetNetworkAclAssociation(
    'SubnetNetworkAclAssociation',
    SubnetId=Ref(subnet_public),
    NetworkAclId=Ref(public_subnet_acl),
))


# EC2 security groups
instanceSecurityGroup = t.add_resource(ec2.SecurityGroup(
    'InstanceSecurityGroup',
    GroupDescription='Enable SSH access via port 22',
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(
            IpProtocol='tcp',
            FromPort='22',
            ToPort='22',
            CidrIp=Ref(sshlocation_param))
    ],
    VpcId=Ref(stack_vpc),
))

# EC2 instances
bastion_instance = t.add_resource(ec2.Instance(
    'BastionServerInstance',
    # Metadata=instance_metadata,
    ImageId=FindInMap(
        'AWSRegionArch2AMI',
        Ref('AWS::Region'),
        FindInMap(
            'AWSInstanceType2Arch',
            Ref(instanceType_param),
            'Arch')),
    InstanceType=Ref(instanceType_param),
    KeyName=Ref(keyname_param),
    NetworkInterfaces=[
        ec2.NetworkInterfaceProperty(
            GroupSet=[
                Ref(instanceSecurityGroup)],
            AssociatePublicIpAddress='true',
            DeviceIndex='0',
            DeleteOnTermination='true',
            SubnetId=Ref(subnet_public))],
    CreationPolicy=troposphere.policies.CreationPolicy(
        ResourceSignal=troposphere.policies.ResourceSignal(
            Timeout='PT15M')),
    Tags=stack_tags,
))


# ##################
""" OUTPUTS """
VPCId = t.add_output(Output(
    "VPCId",
    Description="VPCId of the newly created VPC",
    Value=Ref(stack_vpc),
))

t.add_output(Output(
    'NatEip',
    Value=Ref(nat_eip),
    Description='Nat Elastic IP',
))

t.add_output(Output(
    'PublicIP',
    Description="Public IP address of the newly created EC2 instance",
    Value=GetAtt(bastion_instance, "PublicIp"),
))

print(t.to_json())
