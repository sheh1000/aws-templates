# Converted from RDS_with_DBParameterGroup.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

from troposphere import Parameter, Ref, Template
from troposphere.rds import DBInstance, DBParameterGroup
# Converted from RDS_with_DBParameterGroup.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

from troposphere import Parameter, Ref, Template
from troposphere.rds import DBInstance, DBParameterGroup


t = Template()

t.add_description(
    "AWS CloudFormation Sample Template RDS_with_DBParameterGroup: Sample "
    "template showing how to create an Amazon RDS Database Instance with "
    "a DBParameterGroup.**WARNING** This template creates an Amazon "
    "Relational Database Service database instance. You will be billed for "
    "the AWS resources used if you create a stack from this template.")


# ##################
""" METADATA """

# ##################
""" PARAMETERS """
vpcid = t.add_parameter(Parameter(
    "VPCid",
    Description="VpcId of your existing Virtual Private Cloud (VPC)",
    Type="String"
))

dbuser = t.add_parameter(Parameter(
    "DBUser",
    NoEcho=True,
    Description="The database admin account username",
    Type="String",
    MinLength="1",
    MaxLength="16",
    AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",
    ConstraintDescription=("must begin with a letter and contain only"
                           " alphanumeric characters.")
))

dbpassword = t.add_parameter(Parameter(
    "DBPassword",
    NoEcho=True,
    Description="The database admin account password",
    Type="String",
    MinLength="1",
    MaxLength="41",
    AllowedPattern="[a-zA-Z0-9]*",
    ConstraintDescription="must contain only alphanumeric characters."
))

dbidentifier = t.add_parameter(Parameter(
    "DBIdentifier",
    NoEcho=True,
    Description="Specify a name that is unique for all DB instances owned "
                            "by your AWS account in the current region.",
    Type="String",
    MinLength="1",
    MaxLength="41",
    AllowedPattern="[a-zA-Z0-9]*",
    ConstraintDescription="must contain only alphanumeric characters."
))

# ##################
""" MAPPINGS """

# ##################
""" CONDITIONS """

# ##################
""" RESOURCES """
t.add_resource(DBSecurityGroup(
    "DBSecurityGroup",
    EC2VpcId=Ref(vpcid),
    VPCSecurityGroups='DbSecurityGroup'
))

mydb = t.add_resource(DBInstance(
    "MyDB",
    AllocatedStorage="5",
    DBInstanceClass="db.t2.micro",
    StorageType="gp2",
    Engine="postgres",
    MasterUsername=Ref(dbuser),
    MasterUserPassword=Ref(dbpassword),
    PubliclyAccessible=False,
    DBInstanceIdentifier=Ref(dbidentifier)
))
# ##################
""" OUTPUTS """

response = cfclient.validate_template(TemplateBody=t.to_json())
print(response)

file = open('rds.template', 'w')
file.write(t.to_json())
file.close()