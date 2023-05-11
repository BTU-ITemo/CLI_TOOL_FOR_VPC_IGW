# CLI_TOOL_FOR_VPC_IGW
VPC and Internet Gateway CLI Tool

This CLI tool can be used to create a new Virtual Private Cloud (VPC) and Internet Gateway (IGW) in AWS. The tool is written in Python and uses the Boto3 library to interact with AWS services.
Requirements
- Python 3.x
- Boto3 library
- AWS account with sufficient permissions to create VPC and IGW resources

Installation:

Clone the repository or download the vpc_igw.py and .env file.
Install the Boto3 library and dotenv using pip:

```pip install boto3 python-dotenv```

Set up your AWS credentials and region. You can modify the file .env

Usage

To create a new VPC and IGW, run the vpc_igw.py script with the --name and --cidr arguments:

```python vpc_igw.py --name my-vpc --cidr 10.0.0.0/16```

You can also run the script without these arguments, and you will be prompted to enter the VPC name and CIDR block:

```python vpc_igw.py```



