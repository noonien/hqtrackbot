#!/usr/bin/env python3

from aws_cdk import cdk

from cdk_fargate.cdk_fargate_stack import CdkFargateStack


app = cdk.App()
CdkFargateStack(app, "cdk-fargate-cdk-1")

app.run()
