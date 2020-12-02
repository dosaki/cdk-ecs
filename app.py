#!/usr/bin/env python3

from aws_cdk import core

from stacks.elb_stack import ElbStack
from stacks.network_stack import NetworkStack


app = core.App()
network = NetworkStack(app, "network")
ElbStack(app, "elb", network.vpc)

app.synth()