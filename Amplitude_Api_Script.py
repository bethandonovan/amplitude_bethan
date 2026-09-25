#Import libraries/packages needed, boto3, os, json, datetime, pandas?, dotenv, logging, requests
import os
import json
from datetime import datetime, timedelta
import boto3
import pandas as pd
from dotenv import load_dotenv
import logging
import requests
import zipfile
import gzip
import logging

#Add dotenv thing
load_dotenv()

#Define variables - access keys from dotenv, url, url prefix, dates etc
#First define AWS access keys
aws_access_key = os.getenv('DENG_AWS_ACCESS_KEY')
aws_secret_key = os.getenv('DENG_AWS_SECRET_KEY')
aws_bucket_name = os.getenv('DENG_BUCKET_NAME')

#Now define amplitude access keys 
amplitude_api_key = os.getenv('AMP_API_KEY')
amplitude_secret_key = os.getenv('AMP_SECRET_KEY')

# Calculate yesterday's date to dynamically pull the previous day's data
yesterday = datetime.now() - timedelta(days=1)
# Format the date as YYYYMMDD and append the required start (T00) and end (T23) hours
start_date = yesterday.strftime('%Y%m%dT00')
end_date = yesterday.strftime('%Y%m%dT23')

#Now define any other variables needed
url = "https://analytics.eu.amplitude.com/api/2/export"
#define date parameters for the date range we want to export
export_start_date = start_date
export_end_date = end_date
#Concatenate into a url 
full_url = f'{url}?start={export_start_date}&end={export_end_date}'

#Create folder to store data
amplitude_dir = 'amplitude_data'
os.makedirs(amplitude_dir, exist_ok = True)

#Create a folder to store logs
log_dir = 'log'
os.makedirs(log_dir, exist_ok=True)


#Give the data file a name with timestamp - make zip file as thats the response format & a json file for later & a file name for s3 bucket & a file for logging
time_stamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
zip_file_name = f'{amplitude_dir}/{time_stamp}.zip'
parsed_json_file = f'{amplitude_dir}/{time_stamp}_parsed.json'
s3_file_name = f'{amplitude_dir}/{time_stamp}_Parsed.json'
log_filename = f'{log_dir}/{time_stamp}.log'
#Empty list to put parsed zip -> json
all_events = []

#
logging.basicConfig(
    filename = log_filename,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

logger = logging.getLogger()
logging.info('Logger Successfully Initialised')

#Set up Amplitude API Connection
#Getting data from the url 
response = requests.get(full_url ,auth=(amplitude_api_key, amplitude_secret_key))
#returning response to check that its pulling from the api correctly
status = response.status_code
print(f'This is the status code returned: {status}, investigate if necessary')
logging.info(f'This is the status code returned: {status}, investigate if necessary')


#If statement to seperate if there is an status code error
if status == 200: 
	#downloading the data into the file we created
	#open our empty file we created and allow writing in binary 
	with open(zip_file_name, 'wb') as f:
		#write the content from response into our open file 
		f.write(response.content)
	print(f'Successfully Downloaded {zip_file_name}')
	logging.info(f'Successfully Downloaded {zip_file_name}')

	#open zipfile and parse the JSON inside
	#opening the zip file and setting to 'read'
	with zipfile.ZipFile(zip_file_name, 'r') as archive:
		#looping through all the files in the zip file
		for internal_file in archive.namelist():
			#opens whichever json file we are on 
			with archive.open(internal_file) as internal_f:
				#checks if that row has a secondary zip layer
				if internal_file.endswith('.gz'):
					#opens gzip file to read text and decompress file, translating from bits to human language
					with gzip.open(internal_f, 'rt', encoding='utf-8') as gz_f:
						#loop to read files one at a time
						for line in gz_f:
							#parsing data
							data = json.loads(line)
							#appending to empty events lsit
							all_events.append(data)
				#for other instances with no second zip layer
				else: 
					for line in internal_f:
						#converts from bytes into readable text
						data = json.loads(line.decode('utf-8'))
						#append to the empty list we made earlier 
						all_events.append(data)
						

	print(f'Successfully parsed {len(all_events)} events.')
	logging.info(f'Successfully parsed {len(all_events)} events.')

else: 
	print(f'Failed to fetch data. Status code: {status}')
	logging.critical(f'Failed to fetch data. Status code: {status}')

#open the empty parsed_json_file and dump our new events list into the file
with open(parsed_json_file, 'w') as file:
	json.dump(all_events, file, indent=4)
print(f'File {parsed_json_file} was successfully saved')
logging.info(f'File {parsed_json_file} was successfully saved')

if os.path.exists(zip_file_name):
    os.remove(zip_file_name)
    print(f'Cleaned up temporary zip file: {zip_file_name}')
    logging.info(f'Cleaned up temporary zip file: {zip_file_name}')


#Set up AWS S3 bucket connection
#s3_client = boto3.client(
#	"s3",
#	aws_access_key_id = aws_access_key,
#	aws_secret_access_key = aws_secret_key
#)

# Drop data into s3 bucket
# s3_client.upload_file(
# 	Filename= parsed_json_file,
# 	Bucket = aws_bucket_name,
# 	Key = s3_file_name
# )





