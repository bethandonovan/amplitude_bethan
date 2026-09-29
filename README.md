#P1 Amplitude API
## Description
The file 'Amplitude_API_Script' uses an API to connect to amplitude, pulls the data in nested .zip format. It unzips the .zip and the .gz layers, to reveal .json files, which are then dumped into a file and saved. There is a skeleton at the end of the code to upload this data file to an amazon s3 bucket.

## Packages
You will need Python 3 installed, along with the following packages. You can install them via pip:\
`pip install requests boto3 pandas python-dotenv`

## Environment Variables
If you connect to this code, you will need to create your own .env file and input your own credentials to access the api. Ensure your .env file is added to your .gitignore so you do not accidentally expose your credentials on GitHub.\
Template:\

### Amplitude API Credentials
```
AMP_API_KEY=your_amplitude_api_key_here
AMP_SECRET_KEY=your_amplitude_secret_key_here
```

### AWS Credentials
```
DENG_AWS_ACCESS_KEY=your_aws_access_key_here\
DENG_AWS_SECRET_KEY=your_aws_secret_key_here\
DENG_BUCKET_NAME=your_s3_bucket_name_here\
```
## First Output
Once the script has been run, this generates 2 files, one in the 'amplitude_data' folder, with a timestamp for when this file was created.
The second file created is a log file to track the results of running the script.

# P2 Upload to S3 Bucket
The script 'Amplitude_load_script' uses the aws access keys defined earlier, to connect to an s3 bucket of your choice, and drop the .json files collected in the previous section into said s3 bucket. 

## Personalised instructions
Create your own .aws_env file, and use the instructions in course_docs/week_2_amplitude_Load.md to follow how to connect to the s3 bucket via terminal, and then set up a connection to snowflake where the files can be added to a schema to be analysed. 

