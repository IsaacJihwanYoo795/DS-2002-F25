import boto3
import urllib.request

url="https://media.tenor.com/x8v1oNUOmg4AAAAM/rickroll-roll.gif"
bucket="kmj5gflab8part3"
key = "rickroll.gif"
expires_in = 604800

urllib.request.urlretrieve(url, key)

s3 = boto3.client('s3', region_name='us-east-1')
s3.upload_file(Filename=key, Bucket=bucket, Key=key)

response = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket, 'Key': key},
    ExpiresIn=expires_in
)

print(response)
