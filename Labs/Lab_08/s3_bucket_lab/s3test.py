import boto3

# Create an S3 client
s3 = boto3.client('s3', region_name='us-east-1')

local_file_path = 'C:/Users/isaac/Downloads/googlelogo.png'
bucket = 'kmj5gflab8part3'
s3_key = 'googlelogo.png'  # S3 file name



s3.upload_file(
    Filename=local_file_path,
    Bucket=bucket,
    Key=s3_key,
    ExtraArgs={'ACL': 'public-read'}
)
