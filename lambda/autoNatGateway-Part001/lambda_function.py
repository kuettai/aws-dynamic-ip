import boto3, json
import time, os

## Initialize:
__isDebug = True

## Need to get from Step Function
__natId = ""
__routeTableId = os.environ['routeTableId']

## Testing
ec2 = boto3.client("ec2")

def printDebug(msg):
    if not __isDebug:
        return

    print(msg)
    print("\n")

def createRoute():
    resp = ec2.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        NatGatewayId=__natId,
        RouteTableId=__routeTableId
    )

def setRouteTableWithNewNatGW():
    allocId = ''
    resp = ec2.describe_route_tables(
        RouteTableIds=[__routeTableId]
    )

    routes = resp['RouteTables'][0]['Routes']
    for i, route in enumerate(routes):
        if route['DestinationCidrBlock'] == '0.0.0.0/0':
            printDebug("Detected DestinationCidrBlock=0.0.0.0/0, deleting...")
            resp = ec2.describe_nat_gateways(
                NatGatewayIds=[route['NatGatewayId']]
            )

            printDebug("Nat Gateway: " + route['NatGatewayId'])
            deleteNatResp = ec2.delete_nat_gateway(
                NatGatewayId=route['NatGatewayId']
            )
            print(deleteNatResp)

            oldEip = resp['NatGateways'][0]['NatGatewayAddresses'][0]
            ipAddr = oldEip['PublicIp']
            allocId = oldEip['AllocationId']

            printDebug("Elastic Ip " + allocId + " (" + ipAddr + ")")
            # print("Sleep for 60 seconds...")
            # time.sleep(60)

            ## Cant release address until NAT Gateway is completely deleted; should pass allocId to stepfunction and delete later
            #releaseResp = ec2.release_address(
            #    AllocationId = allocId
            #)
            #print(releaseResp)


            ec2.delete_route(
                DestinationCidrBlock = route['DestinationCidrBlock'],
                RouteTableId = __routeTableId
            )
            printDebug("=== Completed ===")
            break

    createRoute()
    return allocId


def lambda_handler(event, context):
    global __natId
    __natId = event['natId']
    print(__natId)
    allocId = setRouteTableWithNewNatGW()
    return {'eipAllocId': allocId}
    
