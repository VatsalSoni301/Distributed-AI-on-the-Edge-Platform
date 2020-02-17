FROM python

Expose 5000

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "server.py"]
