import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import numpy as np
import requests
import json
import uuid


server_nats = "nats://localhost:4222"
server_organizer = "http://localhost:5000"
list_of_subscription = [0,1,2,3,4,5,6,7,8,9,10,11]

class Subscriber() : 
    def __init__ (self, list_of_subscription, property) :
        self.list_of_subscription = list_of_subscription
        self.property = property


    async def run(self):
        nc = NATS()
        await nc.connect(server_nats)

        async def message_handler(msg):
            subject = msg.subject
            data = msg.data.decode()
            print(f"{subject} redceived data {data}")
            requests.post(server_organizer, data = json.dumps({
                "id": get_id(subject),
                "subject": subject, 
                "data": data
            }))

        def get_id(subject):
            return int(subject.split('.')[1]) % 2

        async def subscribe(lst) : 
            for i in lst :          
                subject = "sensor." + str(i) + "." + self.property + ".>"
                print(subject)
                await nc.subscribe(subject, cb=message_handler)

        await subscribe([0,1,2,3,4,5,6,7,8,9])
        await asyncio.sleep(1000000)    
        await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    subscriber = Subscriber(list_of_subscription, "temperature")
    loop.run_until_complete(subscriber.run())
    loop.close()