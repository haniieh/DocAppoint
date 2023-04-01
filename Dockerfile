# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.10

##Iinstalling dependent packages
RUN apt-get update && apt-get install -y apt-utils && apt-get -y install sudo
RUN apt-get install -y python3-dev  \
    && apt-get install -y gcc  \
    && apt-get install -y virtualenv


### Creating workding directory
WORKDIR /app

# Copy in your requirements file
ADD requirements.txt /tmp/requirements.txt


RUN pip install --upgrade pip

COPY ./requirements.txt /tmp/

##Installing the pip requirements
RUN pip install -r /tmp/requirements.txt

### Copying all the files
COPY . .

##Exposing the application 
EXPOSE 8000
###Running the application
CMD ["python","manage.py","runserver","0.0.0.0:8000"]


