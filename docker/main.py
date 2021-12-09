#!/usr/bin/env/python
import os
from dotenv import load_dotenv
import boto3
from botocore.client import Config

### Load environmental variables from .env file
load_dotenv()
# local directory path info
data_dir = os.environ.get('DATA_DIR')
data_file = os.environ.get('DATA_FILE2')
# Env variables S3 settings
endpoint_url = os.environ.get('ENDPOINT_URL')
s3_config_signature = os.environ.get('AWS_CONFIG_SIGNATURE')
aws_region = os.environ.get('AWS_REGION')
# MODIFY THESE TO GET INFO FROM SEPARATE FILE
access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
# Env variables S3 bucket and filenames
s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
s3_input_filename = os.environ.get('FILE_NAME_INPUT')
s3_output_filename = os.environ.get('FILE_NAME_OUTPUT')

# download file from s3 to local
def download_s3_file(s3_client_conn, bucket_name, s3_filename,
                    target_dir, target_filename):
    """Download a file from s3 to target local directory
    
    Parameters:
    s3_client_conn - boto s3 client object
        A boto s3 client object with an established connection
    bucket_name - str
        s3 bucket name to download from
    s3_filename - str
        s3 filename
    target_dir - str
        target local directory name
    target_filename - str
        target local file name

    Returns:
    True if file download succeeds, else False
    """
    s3_client_conn.download_file(bucket_name,
                                s3_filename,
                                f"{target_dir}/{target_filename}")
    
    if os.path.isfile(f"{target_dir}/{target_filename}"):
        print(f"file: {s3_filename} has been downloaded from "
            f"{bucket_name} as {target_dir}/{target_filename}.")
        return True
    else:
        print('File not downloaded.')
        return False

# modify file
def modify_file(dir_name, file_name, added_string):
    """Modify downloaded s3 file"""
    with open(f"{dir_name}/{file_name}", "a") as f:
        f.write(added_string)
    return None

def establish_s3conn(endpoint, aws_key, aws_secret,
                    aws_config_sig, region, 
                    use_ssl = False, verify = False):
    """Establish s3 connection"""
    s3_conn = boto3.client('s3',
                            endpoint_url=endpoint,
                            aws_access_key_id=aws_key,
                            aws_secret_access_key=aws_secret,
                            config=Config(signature_version=aws_config_sig),
                            region_name=region,
                            use_ssl = use_ssl,
                            verify = verify)

    return s3_conn

def upload_s3_file(s3_client_conn, local_dir, local_file,
                    s3_bucket_name, s3_filename):
    """Upload a file from local directory to s3 bucket
    
    Parameters:
    s3_client_conn - boto s3 client object
        A boto s3 client object with an established connection
    local_dir - str
        target local directory name
    local_file - str
        target local file name
    s3_bucket_name - str
        s3 bucket name to download from
    s3_filename - str
        s3 filename

    Returns:
    True if file download succeeds, else False"""
    s3_client_conn.upload_file(f"{local_dir}/{local_file}",
                s3_bucket_name,
                s3_filename)
    return True
    

if __name__ == '__main__':
    s3 = establish_s3conn(endpoint_url, access_key_id,
                        secret_key, s3_config_signature,
                        aws_region)

    download_s3_file(s3, s3_bucket_name, s3_input_filename,
                data_dir, data_file)

    modify_file(data_dir, data_file, '\ntest string add')

    # upload file from local to s3
    upload_s3_file(s3, data_dir, data_file,
                    s3_bucket_name, s3_output_filename)
    # s3.upload_file(f"{data_dir}/{data_file}",
    #                 s3_bucket_name,
    #                 s3_output_filename)

    with open(f"{data_dir}/{data_file}", "r") as f:
            print(f"{data_file} contents: {f.readlines()}")

    # remove local copy of file
    os.remove(f"{data_dir}/{data_file}")