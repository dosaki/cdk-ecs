from aws_cdk import core, aws_ec2 as ec2


class NetworkStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, "VPC", cidr="190.0.0.0/16", max_azs=3, nat_gateways=0)
        self.vpc.add_gateway_endpoint("S3Endpoint", service=ec2.GatewayVpcEndpointAwsService.S3,
                                      subnets=self.vpc.isolated_subnets)

        ecr_endpoint_sg = ec2.SecurityGroup(self, "ECREndpointSG", vpc=self.vpc, allow_all_outbound=True,
                                            description="Group for the ECR VPC Endpoints")
        ecr_endpoint_sg.add_ingress_rule(ec2.Peer.ipv4(self.vpc.vpc_cidr_block),
                                         ec2.Port.all_tcp(), description="Allow access from the VPC")

        self.vpc.add_interface_endpoint("ECREndpoint", service=ec2.InterfaceVpcEndpointAwsService.ECR,
                                        subnets=ec2.SubnetSelection(subnets=self.vpc.isolated_subnets),
                                        security_groups=[ecr_endpoint_sg])
        self.vpc.add_interface_endpoint("ECRDockerEndpoint", service=ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER,
                                        subnets=ec2.SubnetSelection(subnets=self.vpc.isolated_subnets),
                                        security_groups=[ecr_endpoint_sg])
