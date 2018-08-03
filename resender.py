import asyncio
import logging
import sys

READ_BUFFER = 4096
HOST = '127.0.0.1'


class Resender:
    SourceType = {
        Initiator,
        Receiver,
        Stub
    }
    
    def __init__(self, data, loop):
        self.id = data['id']
        self.name = data['name']

        self.ts_initiator = data['ts_initiator']
        self.initiator_port = data['initiator_port']
        self.receiver_port = data['receiver_port']
#         self.stub_port = data['stub_port']
#         self.use_stub = data['use_stub']

        self.running = True
        self.loop = loop

        self.initiator_writer = None
        self.receiver_writer = None
#         self.stub_writer = None

        self.setup_logger()
        self.queue = asyncio.Queue()
        self.log = logging.getLogger('{}'.format(self.name))

    @staticmethod
    def setup_logger():
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(name)s: %(message)s',
            stream=sys.stdout,
        )

    @staticmethod
    async def prepare_response(data):
        return data

    async def main_loop(self, reader, writer)
        while self.running:
            data = await reader.read(READ_BUFFER)
            if data:
                self.log.debug('received {!r}'.format(data.decode('utf-8')))

                response = await self.prepare_response(data)

                self.writer.write(response)
                self.writer.drain()
                self.log.debug('sent {!r}'.format(response.decode('utf-8')))
            else:
                self.log.debug('connection closing')
                self.writer.close()
                self.running = False

    async def initiator_connected(self, initiator_reader, initiator_writer):
        try:
            receiver_reader, receiver_writer = await asyncio.open_connection(HOST, self.port_receiver, self.loop)
            await self.main_loop(receiver_reader, initiator_writer)  # receiver to initiator
            await self.main_loop(initiator_reader, receiver_writer)  # initiator to receiver
        except (asyncio.TimeoutError, ConnectionRefusedError) as err:
            print(f'Connection error: {err}')
            self.running = False

    async def start(self):
        self.running = True
        await asyncio.start_server(self.initiator_connected, HOST, self.initiator_port, loop=self.loop)

    async def stop(self):
        self.running = False
