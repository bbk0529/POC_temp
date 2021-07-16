import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import numpy as np
import requests
import json

server_nats = "nats://localhost:4222"
server_organizer = "http://localhost:5000"
list_of_subscription = [0,1,2]

class Subscriber() : 
    def __init__ (self, list_of_subscription, property) :
        self.subscription = list_of_subscription
        self.property = property


    async def run(self):
        nc = NATS()
        await nc.connect(server_nats)

        async def message_handler(msg):
            subject = msg.subject
            data = msg.data.decode()
            print(f"{subject} redceived data {data}")
            requests.post(server_organizer, data = json.dumps({
                "id": 1,
                "subject": subject, 
                "data": data
            }))

        for i in self.subscription: 
            subject = "sensor." + str(i) + "." + self.property + ".>"
            print(subject)
            await nc.subscribe(subject, cb=message_handler)

        await asyncio.sleep(1000000)    
        await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    subscriber = Subscriber(list_of_subscription, "temperature")
    loop.run_until_complete(subscriber.run())
    loop.close()