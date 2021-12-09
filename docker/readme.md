# Running Docker and Python Code

This folder allows a user to build a docker image and run a container using that image to execute arbitrary Python code.

1. Dockerfile - Use this file to build an image. The environmental variables to point to the data directory and data files can be modified here. The relevant lines are:

- ENV DATA_DIR=/app/data
- ENV DATA_FILE=data.txt

2. main.py - This file can be edited to add any arbitrary Python code. It currently pulls in the DATA_DIR and DATA_FILE environmental variables that are loaded during the docker build.

3. requirements.txt - Python library requirements file.

4. /data/data.txt - Sample data file in the data folder.

To build the image, run this code:

```docker build . -t {image_name}```

After building, to run a container using the image, run this code:

```docker run --rm -v $(pwd):/app --name {container_name} {image_name}```

The ```--rm``` tag will delete the container after the process runs.

$(pwd) sets the current directory to be mounted. Use absolute path if there are mounting issues.

5. Python .env file contents below:

`# Set data directory and file`  
DATA_DIR=/app/data  
DATA_FILE=data.txt  
DATA_FILE2=file_download.txt

`# AWS S3 connection variables`  
ENDPOINT_URL=http://172.17.0.2:9000  
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE  
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_CONFIG_SIGNATURE=s3v4  
AWS_REGION=us-east-1  

`# AWS File settings (input = filename IN S3) (output = saved filename TO s3)`  
S3_BUCKET_NAME=test-bucket  
FILE_NAME_INPUT=aws-test-file-in.txt  
FILE_NAME_OUTPUT=aws-test-file-out.txt  
