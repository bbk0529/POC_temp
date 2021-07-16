import numpy as np
import asyncio
import datetime
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

nats_server = "nats://localhost:4222"
properties = ['temperature']

# properties = ['temperature','precipitation','snow','humidity']
    

async def run(loop):
    async def send_data() :     
        sensor_no = np.random.choice(range(12))
        subject = "sensor." + str(sensor_no) + "." + np.random.choice(properties) + "." + str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')[:-1])
        message = round(np.random.randn(),3)
        print(subject, message)

        await nc.publish(subject, str(message).encode())


    nc = NATS()
    await nc.connect(nats_server, loop=loop)
    
    

    while True : 
        await asyncio.sleep(0.2)
        await send_data()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()