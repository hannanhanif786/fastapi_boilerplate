import boto3
from botocore.exceptions import NoCredentialsError
from decouple import config

ACCESS_KEY = config("AWSAccessKeyId")
SECRET_KEY = config("AWSSecretKey")
    
def upload_to_aws(local_file, bucket, s3_file, ext):

    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL': 'public-read', 'ContentType': f'image/{ext}'})
        return f" https://{bucket}.s3.amazonaws.com/{s3_file}"
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


