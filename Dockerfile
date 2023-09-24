# pull the official docker image
FROM python:3.11.5-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project to container
COPY . .

# expose port 8000 (FastAPI app) and 5432 (PostgreSQL)
EXPOSE 8000
EXPOSE 5432

# Start FastAPI and PostgreSQL services
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]