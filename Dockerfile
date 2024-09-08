FROM jodogne/orthanc-python:1.12.4

# This example is using a virtual env that is not mandatory when using Docker containers
# but recommended since python 3.11 and Debian bookworm based images where you get a warning
# when installing system-wide packages.
RUN apt-get update && apt install -y python3-venv
RUN python3 -m venv /.venv

# Installing the required packages
RUN /.venv/bin/pip install --no-cache-dir requests
RUN /.venv/bin/pip install --no-cache-dir torch
RUN /.venv/bin/pip install --no-cache-dir torchvision
RUN /.venv/bin/pip install --no-cache-dir torchxrayvision
RUN /.venv/bin/pip install --no-cache-dir pydicom
RUN /.venv/bin/pip install --no-cache-dir highdicom

ENV PYTHONPATH=/.venv/lib64/python3.11/site-packages/

WORKDIR /app
COPY . .