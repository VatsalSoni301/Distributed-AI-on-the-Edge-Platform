from kombu import Connection, Exchange, Queue, Consumer
import socket
import sys
import requests
import numpy as np
def get_prediction(API_ENDPOINT, data1):
    # print type(data1)
    # print data1
    response=requests.post(API_ENDPOINT,data=data1)
    # print 'Response:', response
    
    result = response.json()
    
    print 'Result',result
    return str(result)

def process_message(body, message):
#    print("The body is {}".format(body))
    message.ack()
    print pred_url
    output = get_prediction(pred_url, body) + '\n'
    with open(file_url, 'a+') as f:
        f.write(output)



def establish_connection():
    revived_connection = conn.clone()
    revived_connection.ensure_connection(max_retries=3)
    channel = revived_connection.channel()
    
    consumer.revive(channel)
    consumer.consume()
    return revived_connection
def consume():
    new_conn = establish_connection()
    while True:
        try:
            new_conn.drain_events()
        except socket.timeout:
            new_conn.heartbeat_check()

def run():
    while True:
        try:
            consume()
        except conn.connection_errors:
            print("connection revived")
pred_url = ''

queue_list = { "mnist": "mnist-queue", "iris":"iris-queue"}
exchange_list = { "mnist": "exchange-mnist", "iris":"exchange-iris"}

argument_list = sys.argv
print argument_list

type_of_model = argument_list[1]

url = argument_list[2]
rabbit_url = "amqp://admin:admin@" + url + ":5672/"

queue_name = queue_list[type_of_model]
exchange_name = exchange_list[type_of_model]


pred_url = argument_list[3]
file_url = argument_list[4]

conn = Connection(rabbit_url, heartbeat=10)
exchange = Exchange(exchange_name, type="direct")
queue = Queue(name=queue_name, exchange=exchange, routing_key="BOB")
consumer = Consumer(conn, queues=queue, callbacks=[process_message], accept=["text/plain"])
consumer.consume()
run()