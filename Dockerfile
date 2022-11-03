FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app/aplication

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt


COPY . /app


#EXPOSE 8080

CMD ["python", "serwer.py"]