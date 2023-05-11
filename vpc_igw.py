import argparse
import boto3
import re
from ipaddress import ip_network
from os import getenv
from dotenv import load_dotenv 

load_dotenv()

def init_client():
  client = boto3.client(
    "s3",
    aws_access_key_id=getenv("aws_access_key_id"),
    aws_secret_access_key=getenv("aws_secret_access_key"),
    aws_session_token=getenv("aws_session_token"),
    region_name=getenv("aws_region_name")
  )
  client.list_buckets()
  return client

def create_vpc(vpc_name, cidr_block):
    ec2 = boto3.resource('ec2')
    vpc = ec2.create_vpc(CidrBlock=cidr_block)
    vpc.create_tags(Tags=[{"Key": "Name", "Value": vpc_name}])
    vpc.wait_until_available()
    print(f'Created VPC {vpc.id} with name {vpc_name} and CIDR block {cidr_block}')
    return vpc

def create_igw(vpc_id, vpc_name):
    ec2 = boto3.resource('ec2')
    igw = ec2.create_internet_gateway()
    igw.create_tags(Tags=[{"Key": "Name", "Value": 'IGW_FOR_' + vpc_name}])
    igw.attach_to_vpc(VpcId=vpc_id)
    print(f'Created IGW {igw.id} and attached it to VPC {vpc_id}')
    return igw


def is_private_cidr(cidr_block):
    try:
        network = ip_network(cidr_block)
        private_blocks = [
            ip_network('10.0.0.0/8'),
            ip_network('172.16.0.0/12'),
            ip_network('192.168.0.0/16')
        ]
        for block in private_blocks:
            if network.subnet_of(block):
                return True
        return False
    except ValueError:
        return False



def main():
    parser = argparse.ArgumentParser(description='Create a VPC and an Internet Gateway')
    parser.add_argument('--name','-n', type=str, help='The name of the VPC')
    parser.add_argument('--cidr','-c', type=str, help='The CIDR block of the VPC (e.g. 10.0.0.0/16)')
    args = parser.parse_args()

    if args.name:
        vpc_name = args.name
    else:
        vpc_name = input('Enter a name for the VPC: ')

    if args.cidr:
        cidr_block = args.cidr
    else:
        cidr_block = input('Enter a CIDR block for the VPC (e.g. 10.0.0.0/16): ')

    if is_private_cidr(cidr_block):
        vpc = create_vpc(vpc_name, cidr_block)
        igw = create_igw(vpc.id, vpc_name)
    else:
        print("Invalid CIDR block provided. Please provide a private IP address range.")

if __name__ == '__main__':
    main()