#Import libraries/packages needed, boto3, os, json, datetime, pandas?, dotenv, logging, requests
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging
import requests
import zipfile
import gzip
import logging

logger = logging.getLogger(__name__)

def extract_zip_unzip_to_json(url:str, start_date:str, end_date:str, data_dir:str, timestamp:str, Amplitude_api_key:str, Amplitude_secret_key:str):
    """_summary_

    Args:
        url (str): Appropriate URL to the amplitude API
        start_date (str): Start date of data collection (format: YYYYMMDDTHH, eg 20260925T00)
        end_date (str): End date of data collection (format: YYYYMMDDTHH, eg 20260925T23)
        data_dir (str): Name of folder to store the data files
        timestamp (str): Timestamp to tag to the file name, typically time of running
        Amplitude_api_key (str): Your Amplitde API key
        Amplitude_secret_key (str): Your Amplitude secret key
    """

    #Concatenate into a url 
    full_url = f'{url}?start={start_date}&end={end_date}'

    #Create folder to store data
    os.makedirs(data_dir, exist_ok = True)

    #Give the data file a name with timestamp - make zip file as thats the response format & a json file for later & a file name for s3 bucket & a file for logging
    zip_file_name = f'{data_dir}/{timestamp}.zip'
    parsed_json_file = f'{data_dir}/{timestamp}_parsed.json'
    #Empty list to put parsed zip -> json
    all_events = []


    #Set up Amplitude API Connection
    #Getting data from the url 
    response = requests.get(full_url ,auth=(Amplitude_api_key, Amplitude_secret_key))
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

    #deleted zip files after use
    if os.path.exists(zip_file_name):
        os.remove(zip_file_name)
        print(f'Cleaned up temporary zip file: {zip_file_name}')
        logging.info(f'Cleaned up temporary zip file: {zip_file_name}')






