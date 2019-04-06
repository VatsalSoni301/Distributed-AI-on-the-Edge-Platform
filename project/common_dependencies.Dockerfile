FROM ubuntu:latest

WORKDIR /common
COPY requirements.txt .

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get install -y openssh-server
RUN apt-get install ssh
RUN apt-get install sshpass