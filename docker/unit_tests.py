import pytest
import datetime
import boto3
import botocore.session
from moto import mock_s3
import os

from boto3_test_script import download_s3_file
from boto3_test_script import upload_s3_file

from botocore.stub import Stubber
from botocore.client import Config

@mock_s3
def test_download_s3_file():
    # create mock s3 client, bucket, and file
    s3 = boto3.client('s3', region_name = 'us-east-1')
    s3.create_bucket(Bucket = 'test-bucket')
    s3.put_object(Bucket = 'test-bucket', Key = 'test_file.txt', Body = 'stuff')
    # test script
    download_s3_file(s3, 'test-bucket', 'test_file.txt',
                    '.', 'downloaded_file.txt')
    # check file exists
    assert os.path.isfile('downloaded_file.txt')

#test_download_s3_file()

@mock_s3
def test_upload_s3_file():
    # create mock s3 client and bucket
    s3 = boto3.client('s3', region_name = 'us-east-1')
    s3.create_bucket(Bucket = 'test-bucket')
    # test script
    upload_s3_file(s3, './data', 'test_upload_file.txt',
                    'test-bucket', 'test-upload.txt')
    # check 
    resp = s3.get_object(Bucket = 'test-bucket', Key = 'test-upload.txt')
    content_length = resp["ResponseMetadata"]["HTTPHeaders"]["content-length"]
    assert content_length == '20'

#test_upload_s3_file()



