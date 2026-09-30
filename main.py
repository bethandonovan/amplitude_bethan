
from modules.log_initialise import set_up_logging
from modules.extract_function import extract_zip_unzip_to_json
from modules.load_function import load_to_s3
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

#Add dotenv thing
load_dotenv()

#timestamp that will label any files created with the current timestamp
time_stamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

#logger set up module used
logger = set_up_logging('log', time_stamp)

#API URL
url = "https://analytics.eu.amplitude.com/api/2/export"

#Define variables - 
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


#use extract module with variables defined above input as the parameters
extract_zip_unzip_to_json(url, start_date, end_date, 'data', time_stamp, amplitude_api_key, amplitude_secret_key)

#use load module 
load_to_s3('data', aws_access_key, aws_secret_key, aws_bucket_name)




