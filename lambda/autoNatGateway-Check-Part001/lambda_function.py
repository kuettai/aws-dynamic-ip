import boto3, json
import time, os

## Initialize:
__isDebug = True

## Testing
ec2 = boto3.client("ec2")



def lambda_handler(event, context):
    __natId = event['natId']

    natState = ec2.describe_nat_gateways(
        NatGatewayIds = [__natId]
    )
    myState = natState['NatGateways'][0]['State']

    return {'natId': __natId, 'ngwStatus': myState}
