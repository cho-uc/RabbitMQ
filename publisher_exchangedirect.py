'''
Working example of publisher with specific exchange name

'''

import pika

# If you want to listen to rabbitmq 
# you need to connect through port 5672 - not 15672. 

credentials = pika.PlainCredentials('hapu', 'hapu123')
parameters = pika.ConnectionParameters('localhost',
                                   5672,
                                   '/',
                                   credentials,
                                   heartbeat=600,
                                    blocked_connection_timeout=300)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.exchange_declare(exchange='myexchangename_direct',
                         exchange_type='direct')

for i in range(5):
    body = 'abcbody : ' + str(i)
    channel.basic_publish(exchange='myexchangename_direct',
                      routing_key='purple_route',
                      body=body)
    print(" [x] Sending through purple_route " + body)

for i in range(5):
    body = 'abcbody : ' + str(i)
    channel.basic_publish(exchange='myexchangename_direct',
                      routing_key='pink_route',
                      body=body)
    print(" [x] Sending through pink_route " + body)

connection.close()