from aws_cdk import core, aws_ec2 as ec2, aws_elasticloadbalancingv2 as elbv2


class ElbStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.elb_security_group = ec2.SecurityGroup(self, "ELBSG", vpc=vpc, allow_all_outbound=True,
                                                    description="Group for the ELB")
        self.elb_security_group.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(80),
                                                 description="Allow HTTP access")
        self.elb_security_group.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(443),
                                                 description="Allow HTTPS access")

        lb = elbv2.ApplicationLoadBalancer(self, "ELB", vpc=vpc, internet_facing=True,
                                           vpc_subnets=ec2.SubnetSelection(subnets=vpc.public_subnets))

        health_check = elbv2.HealthCheck(enabled=True, healthy_http_codes="200", healthy_threshold_count=3,
                                         interval=core.Duration.seconds(15), path="/pi",
                                         timeout=core.Duration.seconds(10), unhealthy_threshold_count=3)

        blue_target_group = elbv2.ApplicationTargetGroup(self, "BlueTargetGroup", port=8224,
                                                         protocol=elbv2.ApplicationProtocol.HTTP,
                                                         stickiness_cookie_duration=core.Duration.days(30),
                                                         health_check=health_check, target_type=elbv2.TargetType.IP,
                                                         vpc=vpc)
