FROM ubuntu:jammy

WORKDIR /ingest

# Get latest apt updates and upgrades
RUN apt update
RUN apt upgrade -y

# Install python3
RUN apt install -y python3-full

# Create new virtual environment to install dependencies into
RUN python3 -m venv /env

# Install pip packages and deps
RUN /env/bin/pip install --upgrade pip
RUN /env/bin/pip install celery[librabbitmq,redis,auth,msgpack]
RUN /env/bin/pip install Flask
RUN /env/bin/pip install requests
RUN /env/bin/pip install GitPython

ENTRYPOINT /env/bin/python server.py 
