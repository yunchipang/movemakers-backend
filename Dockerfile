# pull the official docker image
FROM python:3.11.5-slim

# set work directory
WORKDIR /src
ADD ./ /src

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# add app
COPY . .
