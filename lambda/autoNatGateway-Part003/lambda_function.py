import boto3, json
import time, os

## Initialize:
__isDebug = True

## Need to get from Step Function

## Testing
ec2 = boto3.client("ec2")

def printDebug(msg):
    if not __isDebug:
        return

    print(msg)
    print("\n")


def lambda_handler(event, context):
    allocId = event['eipAllocId']
    if len(allocId) == 0:
        return {'status': 'Ok; No '}

    releaseResp = ec2.release_address(
        AllocationId = allocId
    )
    print(releaseResp)
    return {'status': 'Ok'}
