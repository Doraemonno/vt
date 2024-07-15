#!/usr/bin/env python3

# import aws_cdk as cdk
from aws_cdk import App
from vt.vt_stack import VtStack


app = App()
VtStack(app, "VtStack")

app.synth()
