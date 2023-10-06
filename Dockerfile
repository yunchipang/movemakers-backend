# pull the official docker image
FROM python:3.11.5-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# add app
COPY . .

# expose the port the application will run on
EXPOSE 8000

# run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
