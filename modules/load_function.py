#import packages
from dotenv import load_dotenv
import os
import boto3
import logging
from datetime import datetime 
from botocore.exceptions import ClientError

def load_to_s3(data_dir:str, AWS_ACCESS_KEY:str, AWS_SECRET_ACCESS_KEY:str, AWS_BUCKET_NAME:str):

    #connect to s3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id = AWS_ACCESS_KEY,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )

    #define variables to upload data file, using names created in Amplitude_API_Script.py
    files_to_upload = os.listdir(data_dir)

    #loops through all the files in the data folder
    for file in files_to_upload:
        file_to_upload = f'{data_dir}/{file}'
        print(file_to_upload)
        try:
        #upload the file to s3 bucket 
            s3_client.upload_file(
                file_to_upload,
                AWS_BUCKET_NAME,
                file
            )
            print(f'{file} has been uploaded successfully')
            logging.info(f'{file} has been uploaded successfully')
            #deleted files once uploaded to s3
            os.remove(file_to_upload)
        #collect more detailed error if having trouble uploading to s3 bucket 
        except ClientError as e:
            print(f'Unexpected error {e}')
            logging.warning('An error has occured')