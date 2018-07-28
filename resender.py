import asyncio


class Resender:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.running = False

    async def start(self):
        self.running = True
        while self.running:
            print(f'Recender id={self.id} is started')
            await asyncio.sleep(1)

    async def stop(self):
        self.running = False
