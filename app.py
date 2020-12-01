#!/usr/bin/env python3

from aws_cdk import core

from ecs_dashboard.ecs_dashboard_stack import EcsDashboardStack


app = core.App()
EcsDashboardStack(app, "ecs-dashboard")

app.synth()
