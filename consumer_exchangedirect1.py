'''
Working example of consumer with specific direct-exchange name
Run consumer_exchangedirect2.py at the same time with this script
'''

import pika

credentials = pika.PlainCredentials('hapu', 'hapu123')
params = pika.ConnectionParameters('localhost',
                                   5672,
                                   '/',
                                   credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange='myexchangename_direct', exchange_type='direct')
result = channel.queue_declare(queue='') # choose a random queue name
queue_name = result.method.queue
channel.queue_bind(exchange='myexchangename_direct', queue=queue_name, routing_key='purple_route')
print(queue_name)
for method_frame, properties, body in channel.consume(queue=queue_name):

    # Display the message parts
    print(method_frame)
    print("Properties: " + str(properties))
    print("Body: "+ str(body))

    # Acknowledge the message
    channel.basic_ack(method_frame.delivery_tag)

    # Escape out of the loop after 5 messages
    if method_frame.delivery_tag == 5:
        break

# Cancel the consumer and return any pending messages
requeued_messages = channel.cancel()
print('Requeued %i messages' % requeued_messages)

# Close the channel and the connection
channel.close()
connection.close()