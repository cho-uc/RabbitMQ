'''
Working example of consumer with specific fanout-exchange name

'''

import pika

credentials = pika.PlainCredentials('hapu', 'hapu123')
params = pika.ConnectionParameters('localhost',
                                   5672,
                                   '/',
                                   credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange='myexchangename', exchange_type='fanout')
result = channel.queue_declare(queue='') # choose a random queue name
queue_name = result.method.queue
channel.queue_bind(exchange='myexchangename', queue=queue_name)
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