# publisher.py
import pika, os, logging
logging.basicConfig()

# add to env variable
# CLOUDAMQP_URL will be a combination of your user, password, host and vhost like so:
#amqp(s)://USERNAME:PASSWORD@HOST-NAME/VHOST
# default: guest/guest

# If you want to listen to rabbitmq 
# you need to connect through port 5672 - not 15672. 

# Parse CLODUAMQP_URL (fallback to localhost)
#url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost/%2f')
#print('url: '+ str(url))
'''
url=''
params = pika.URLParameters(url)
params.socket_timeout = 5
'''
credentials = pika.PlainCredentials('hapu', 'hapu123')
params = pika.ConnectionParameters('localhost',
                                   5672,
                                   '/',
                                   credentials)
                                   
connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue='pdfprocess') # Declare a queue
# send a message

channel.basic_publish(exchange='', routing_key='pdfprocess', body='User information')
print ("[x] Message sent to consumer")
connection.close()
