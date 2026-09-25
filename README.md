# amplitude_bethan

This piece of code uses an API to connect to amplitude, and pulls the data.

You will need Python 3 installed, along with the following packages. You can install them via pip: 
pip install requests boto3 pandas python-dotenv


If you connect to this code, you will need to create your own .env file and input your own credentials to access the api. Ensure your .env file is added to your .gitignore so you do not accidentally expose your credentials on GitHub.
Template: 

Amplitude API Credentials
AMP_API_KEY=your_amplitude_api_key_here
AMP_SECRET_KEY=your_amplitude_secret_key_here

AWS Credentials
DENG_AWS_ACCESS_KEY=your_aws_access_key_here
DENG_AWS_SECRET_KEY=your_aws_secret_key_here
DENG_BUCKET_NAME=your_s3_bucket_name_here

Once the script has been run, this generates 2 files, one in the 'amplitude_data' folder, with a timestamp for when this file was created.
The second file created is a log file to track the results of running the script.

In dev (commented out) is a method to then load the data file created into an Amazon S3 Bucket.
