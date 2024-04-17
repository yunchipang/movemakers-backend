# pull the official docker image
FROM python:3.11.5-slim

# set working directory in the container
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy the project files into the working directory
COPY . /app

# install python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# expose the port the app runs on
EXPOSE 8000

# command to run the uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]