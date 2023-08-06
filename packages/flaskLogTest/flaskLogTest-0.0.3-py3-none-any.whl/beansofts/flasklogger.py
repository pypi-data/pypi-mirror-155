import json
import string
from traceback import print_tb
from flask import jsonify,request
from werkzeug.security import check_password_hash,generate_password_hash
import socket
import geocoder
import os
import pika
def channelInfo(usrInfo):
    #!/usr/bin/env python
    #establishig a connection
    # convertion of the data to string
    usrInfo=json.dumps(usrInfo)
    url = os.environ.get('CLOUDAMQP_URL', 'amqps://tnmldbri:STSB8LTzIx8PRW8sgaiAslc0iCocUvXe@puffin.rmq2.cloudamqp.com/tnmldbri')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='leon') # Declare a queue
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=usrInfo) #collection of data
    # print(" [x] Sent 'Hello World!'")
    connection.close()
def registerUser(f):
    def wrapper(*args,**kwargs):
        if request.method=="POST":
            """getiing user location"""
            ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr) #acquiring use ip address
            def check_ip(ip):
                """
                this function will check if the ip address of the use
                is a local or public ip address
                """
                ip_tuple=socket.gethostbyaddr(ip)
                hostname=ip_tuple[0]
                return hostname
            hostname=check_ip(ip_addr)
            if hostname=='localhost':
                location=geocoder.ip("me")
                city=location.city
            else:
                location=geocoder.ip(ip_addr)
                city=location.city
            # adding the data to the database
            content=request.get_json()
            try:
                password=content["password"]
                hashed_password=generate_password_hash(password)
                content["password"]=hashed_password
            except:
                pass
            content['ip']=ip_addr
            content['city']=city
            content['url']=request.host
            channelInfo(content)
            print(request.host)
            return jsonify({"response":content})
        else:
           return f(*args,**kwargs)
    return wrapper
# @registerUser
# def userdetails(*args,**kwargs):
    # pass

# userdetails("martin","phone","Machakos","Kabarak")
