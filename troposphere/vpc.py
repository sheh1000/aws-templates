# Converted from VPC_With_VPN_Connection.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

from troposphere import Output
from troposphere import Parameter, Ref, Tags, Template
from troposphere import ec2 as ec2


t = Template()

t.add_version("2010-09-09")

t.add_description("""\
AWS CloudFormation Sample Template:\
Includes:\
VPC, Public subnet, Private subnet, Gateway\
""")

""" METADATA """

""" PARAMETERS """
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


""" MAPPINGS """

""" CONDITIONS """

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

igw = t.add_resource(ec2.InternetGateway('InternetGateway',))
t.add_resource(ec2.VPCGatewayAttachment("GWAttachmnent",
                                        VpcId = Ref(stack_vpc),
                                        InternetGatewayId=Ref(igw)))

""" OUTPUTS """
VPCId = t.add_output(
    Output(
        "VPCId",
        Description="VPCId of the newly created VPC",
        Value=Ref(stack_vpc),
))


print(t.to_json())