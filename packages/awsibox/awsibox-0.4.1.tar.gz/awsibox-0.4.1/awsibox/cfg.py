import os
import sys
from functools import reduce

cwd = os.getcwd()
sys.path.append(os.path.join(cwd, "lib"))

no_override = False

Parameters = {}
Conditions = {}
Mappings = {}
Resources = {}
Outputs = {}

OBJS = {}

PATH_INT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cfg")
PATH_INT = os.path.normpath(PATH_INT)

PATH_EXT = os.path.join(cwd, "cfg")
PATH_EXT = os.path.normpath(PATH_EXT)

STACK_TYPES = [
    "agw",
    "alb",
    "cch",
    "clf",
    "ec2",
    "ecr",
    "ecs",
    "rds",
    "res",
    "tsk",
]

MAX_SECURITY_GROUPS = 4
# SECURITY_GROUPS_DEFAULT equals list of empty values
# (Ex. for "MAX_SECURITY_GROUPS = 3" we have "SECURITY_GROUPS_DEFAULT = ',,'")
SECURITY_GROUPS_DEFAULT = reduce(
    lambda a, i: f",{a}", list(range(MAX_SECURITY_GROUPS - 1)), ""
)

ENV_BASE = ["dev", "stg", "prd"]

DEFAULT_REGIONS = [
    "eu-west-1",
    "us-east-1",
    "eu-central-1",
]

AZones = {
    "MAX": 6,
    "default": 3,
    "us-east-1": 6,
    "us-west-1": 2,
    "us-west-2": 4,
    "ca-central-1": 2,
    "sa-east-1": 2,
    "cn-north-1": 2,
    "ap-northeast-3": 1,
}

AZoneNames = ["A", "B", "C", "D", "E", "F"]

VPC_DEFAULT_CIDR_BLOCK = "10.80.0.0/16"
VPC_DEFAULT_CIDR_BLOCK_PREFIX = ".".join(VPC_DEFAULT_CIDR_BLOCK.split(".")[0:2])
VPC_DEFAULT_SUBNETS_CIDR_BLOCK_PRIVATE = [
    f"{VPC_DEFAULT_CIDR_BLOCK_PREFIX}.{i * 16}.0/20" for i in range(AZones["MAX"])
]
VPC_DEFAULT_SUBNETS_CIDR_BLOCK_PUBLIC = [
    f"{VPC_DEFAULT_CIDR_BLOCK_PREFIX}.{i + 200}.0/24" for i in range(AZones["MAX"])
]

PARAMETERS_SKIP_OVERRIDE_CONDITION = (
    "Env",
    "UpdateMode",
    "RecordSetExternal",
    "DoNotSignal",
    "EfsMounts",
    "LaunchTemplateDataImageIdLatest",
    "VPCCidrBlock",
    "VPCName",
)

EVAL_FUNCTIONS_IN_CFG = (
    "cfg.",
    "get_expvalue(",
    "Sub(",
    "Ref(",
    "get_subvalue(",
    "get_endvalue(",
    "get_resvalue(",
    "get_condition(",
    "GetAtt(",
    "Split(",
    "Select(",
    "Export(",
    "ImportValue(",
    "Join(",
    "Base64(",
    "If(",
    "Equals(",
    "Not(",
    "GetAZs(",
    "dict(",
    "eval(",
    "Tags(",
    "str(",
    "list(",
    "SG_SecurityGroups",
)

CLF_PATH_PATTERN_REPLACEMENT = {
    "/": "SLASH",
    "*": "STAR",
    "-": "HYPH",
    "?": "QUEST",
    ".": "DOT",
    "_": "USCORE",
}

INSTANCE_SIZES = [
    "nano",
    "micro",
    "small",
    "medium",
    "large",
    "xlarge",
    "2xlarge",
    "4xlarge",
    "8xlarge",
    "12xlarge",
    "16xlarge",
    "24xlarge",
    "32xlarge",
    "48xlarge",
]

INSTANCE_FAMILY = [
    {
        "Name": "t2",
        "Min": "nano",
        "Max": "2xlarge",
    },
    {
        "Name": "m4",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "c4",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "r4",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "t3",
        "Min": "nano",
        "Max": "2xlarge",
    },
    {
        "Name": "m5",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "c5",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "r5",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "t3a",
        "Min": "nano",
        "Max": "2xlarge",
    },
    {
        "Name": "m5a",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "c5a",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "r5a",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "m6i",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "c6i",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "r6i",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "m6a",
        "Min": "large",
        "Max": "4xlarge",
    },
    {
        "Name": "c6a",
        "Min": "large",
        "Max": "4xlarge",
    },
]

# override previous cfg with an External one
try:
    with open(os.path.join(cwd, "lib", "cfgExt.py")) as f:
        exec(f.read())
except FileNotFoundError:
    pass

# build instances list
def build_instance_list():
    family_instances_list = []
    for family in INSTANCE_FAMILY:
        name = family["Name"]
        min_size = INSTANCE_SIZES.index(family["Min"])
        max_size = INSTANCE_SIZES.index(family["Max"])

        for s in INSTANCE_SIZES[min_size : max_size + 1]:
            family_instances_list.append(f"{name}.{s}")

    return family_instances_list


INSTANCE_LIST = ["default"] + build_instance_list()

# Order is VERY important do not CHANGE it!
CFG_TO_FUNC = {
    "MappingClass": {"module": "mappings", "func": "Mappings"},
    "Parameter": {"module": "cloudformation", "func": "CFM_Parameters"},
    "Condition": {"module": "cloudformation", "func": "CFM_Conditions"},
    "Mapping": {"module": "cloudformation", "func": "CFM_Mappings"},
    "Alarm": {
        "module": "joker",
        "func": ("cloudwatch", "Alarm"),
        "dep": ["LoadBalancer"],
    },
    "ApiGatewayAccount": {"module": "joker", "func": ("apigateway", "Account")},
    "ApiGatewayApiKey": {"module": "apigateway", "func": "AGW_ApiKeys"},
    "ApiGatewayBasePathMapping": {
        "module": "joker",
        "func": ("apigateway", "BasePathMapping"),
    },
    "ApiGatewayDomainName": {"module": "apigateway", "func": "AGW_DomainName"},
    "ApiGatewayRestApi": {"module": "apigateway", "func": "AGW_RestApi"},
    "ApiGatewayStage": {"module": "apigateway", "func": "AGW_Stages"},
    "ApiGatewayUsagePlan": {"module": "apigateway", "func": "AGW_UsagePlans"},
    "ApplicationAutoScalingScalingPolicy": {
        "module": "autoscaling",
        "func": "AS_ScalingPolicies",
    },
    "Apps": {"module": "joker", "func": ("codedeploy", "DeploymentGroup")},
    "ASGLifecycleHook": {"module": "joker", "func": ("autoscaling", "LifecycleHook")},
    "AutoScalingGroup": {
        "module": "autoscaling",
        "func": "AS_Autoscaling",
        "dep": ["SecurityGroups"],
    },
    "AutoScalingScalingPolicy": {"module": "autoscaling", "func": "AS_ScalingPolicies"},
    "Bucket": {"module": "s3", "func": "S3_Buckets"},
    "Certificate": {"module": "joker", "func": ("certificatemanager", "Certificate")},
    "CacheSubnetGroup": {"module": "joker", "func": ("elasticache", "SubnetGroup")},
    "CloudFrontCachePolicy": {"module": "joker", "func": ("cloudfront", "CachePolicy")},
    "CloudFrontDistribution": {
        "module": "cloudfront",
        "func": "CF_CloudFront",
        "dep": ["LoadBalancer", "LambdaFunctionAssociation"],
    },
    "CloudFrontOriginAccessIdentity": {
        "module": "joker",
        "func": ("cloudfront", "CloudFrontOriginAccessIdentity"),
    },
    "CloudFrontOriginRequestPolicy": {
        "module": "joker",
        "func": ("cloudfront", "OriginRequestPolicy"),
    },
    "CodeDeployApp": {"module": "joker", "func": ("codedeploy", "Application")},
    "DBInstance": {"module": "rds", "func": "RDS_DB"},
    "DBSubnetGroup": {"module": "joker", "func": ("rds", "DBSubnetGroup")},
    "DynamoDBTable": {"module": "joker", "func": ("dynamodb", "Table")},
    "EC2EIP": {"module": "joker", "func": ("ec2", "EIP")},
    "EC2InternetGateway": {"module": "joker", "func": ("ec2", "InternetGateway")},
    "EC2NatGateway": {"module": "joker", "func": ("ec2", "NatGateway")},
    "EC2Route": {"module": "joker", "func": ("ec2", "Route")},
    "EC2RouteTable": {"module": "joker", "func": ("ec2", "RouteTable")},
    "EC2Subnet": {"module": "ec2", "func": "EC2_Subnet"},
    "EC2VPC": {"module": "joker", "func": ("ec2", "VPC")},
    "EC2VPCEndpoint": {"module": "joker", "func": ("ec2", "VPCEndpoint")},
    "EC2VPCGatewayAttachment": {
        "module": "joker",
        "func": ("ec2", "VPCGatewayAttachment"),
    },
    "EC2VPCPeeringConnection": {
        "module": "joker",
        "func": ("ec2", "VPCPeeringConnection"),
    },
    "ECSCapacityProvider": {"module": "joker", "func": ("ecs", "CapacityProvider")},
    "ECSCluster": {"module": "joker", "func": ("ecs", "Cluster")},
    "ECSClusterCapacityProviderAssociations": {
        "module": "joker",
        "func": ("ecs", "ClusterCapacityProviderAssociations"),
    },
    "EFSAccessPoint": {"module": "joker", "func": ("efs", "AccessPoint")},
    "EFSFileSystem": {"module": "efs", "func": "EFS_FileStorage"},
    "ElastiCacheCacheCluster": {
        "module": "joker",
        "func": ("elasticache", "CacheCluster"),
    },
    "ElastiCacheReplicationGroup": {
        "module": "joker",
        "func": ("elasticache", "ReplicationGroup"),
    },
    "EventsRule": {
        "module": "events",
        "func": "EVE_EventRules",
        "dep": ["SecurityGroups"],
    },
    "HostedZone": {"module": "route53", "func": "R53_HostedZones"},
    "IAMGroup": {"module": "iam", "func": "IAM_Groups"},
    "IAMPolicy": {"module": "iam", "func": "IAM_Policies"},
    "IAMUser": {"module": "iam", "func": "IAM_Users"},
    "IAMUserToGroupAddition": {"module": "iam", "func": "IAM_UserToGroupAdditions"},
    "KMSAlias": {"module": "joker", "func": ("kms", "Alias")},
    "KMSKey": {"module": "joker", "func": ("kms", "Key")},
    "Lambda": {"module": "lambdas", "func": "LBD_Lambdas"},
    "LambdaEventInvokeConfig": {
        "module": "joker",
        "func": ("awslambda", "EventInvokeConfig"),
    },
    "LambdaEventSourceMapping": {
        "module": "joker",
        "func": ("awslambda", "EventSourceMapping"),
    },
    "LambdaFunctionAssociation": {
        "module": "joker",
        "func": ("cloudfront", "LambdaFunctionAssociation"),
    },
    "LambdaLayerVersion": {"module": "lambdas", "func": "LBD_LayerVersions"},
    "LambdaPermission": {"module": "joker", "func": ("awslambda", "Permission")},
    "LoadBalancer": {
        "module": "elasticloadbalancing",
        "func": "LB_ElasticLoadBalancing",
    },
    "LogsLogGroup": {"module": "joker", "func": ("logs", "LogGroup")},
    "ScheduledAction": {"module": "joker", "func": ("autoscaling", "ScheduledAction")},
    "ScalableTarget": {
        "module": "joker",
        "func": ("applicationautoscaling", "ScalableTarget"),
    },
    "R53RecordSet": {"module": "joker", "func": ("route53", "RecordSetType")},
    "Repository": {"module": "ecr", "func": "ECR_Repositories"},
    "Role": {"module": "iam", "func": "IAM_Roles"},
    "SecurityGroup": {"module": "securitygroup", "func": "SG_SecurityGroup"},
    "SecurityGroupIngress": {
        "module": "securitygroup",
        "func": "SG_SecurityGroupIngresses",
    },
    "SecurityGroups": {"module": "securitygroup", "func": "SG_SecurityGroups"},
    "Service": {
        "module": "ecs",
        "func": "ECS_Service",
        "dep": ["SecurityGroups"],
    },
    "ServiceDiscoveryPublicDnsNamespace": {
        "module": "joker",
        "func": ("servicediscovery", "PublicDnsNamespace"),
    },
    "ServiceDiscoveryService": {
        "module": "joker",
        "func": ("servicediscovery", "Service"),
    },
    "SQSQueue": {"module": "joker", "func": ("sqs", "Queue")},
    "SNSSubscription": {"module": "sns", "func": "SNS_Subscriptions"},
    "SNSTopic": {"module": "joker", "func": ("sns", "Topic")},
    "TaskDefinition": {"module": "ecs", "func": "ECS_TaskDefinition"},
    "WafByteMatchSet": {
        "module": "waf",
        "func": ["WAF_GlobalByteMatchSets", "WAF_RegionalByteMatchSets"],
    },
    "WafIPSet": {"module": "waf", "func": ["WAF_GlobalIPSets", "WAF_RegionalIPSets"]},
    "WafRule": {"module": "waf", "func": ["WAF_GlobalRules", "WAF_RegionalRules"]},
    "WafWebAcl": {
        "module": "waf",
        "func": ["WAF_GlobalWebAcls", "WAF_RegionalWebAcls"],
    },
    "WAFv2IPSet": {
        "module": "joker",
        "func": ("wafv2", "IPSet"),
    },
    "WAFv2WebACL": {
        "module": "joker",
        "func": ("wafv2", "WebACL"),
    },
    # CloudformationCustomResource begin here
    "CCRFargateSpot": {
        "module": "cloudformation",
        "func": "CFM_CustomResourceFargateSpot",
    },
    "CCRLightHouse": {
        "module": "cloudformation",
        "func": "CFM_CustomResourceLightHouse",
    },
    # ReplicateRegions need to be the last one
    "CCRReplicateRegions": {
        "module": "cloudformation",
        "func": "CFM_CustomResourceReplicator",
    },
    # Output need to be last line
    "Output": {"module": "cloudformation", "func": "CFM_Outputs"},
}
