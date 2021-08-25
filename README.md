# aws-dynamic-ip
This document shows the way to have all EC2 outbound using the same ip address. Leverage on AWS CloudWatch Canary detects any outbound failure with AWS CloudWatch Alarm to trigger StepFunction to launch new NAT Gateway, update RouteTable once ready. Then release EIP and delete NAT GW for cost saving.

Setup CloudWatch Alarm with Canary
https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Create.html

Simple Canary Script: /canary/sample.js
Step Function Script: /stepfunc/sample.json
Lambda Functions:
- /lambda/autoNatGateway-Part001, to create EIP and NatGW
- /lambda/autoNatGateway-Check-Part001, check for NatGW creation status for cost saving
- /lambda/autoNatGateway-Part002, update RouteTable to use new NatGW, disassociate EIP from NATGw
- /lambda/autoNatGateway-Part003, delte NATGw and release EIP for cost saving
