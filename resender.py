import asyncio
import logging
import sys

READ_BUFFER = 4096
HOST = '127.0.0.1'


class Resender:
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

#         self.sv_writer = None
#         self.ts_writer = None
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

    async def initiator_connected(self, reader, writer):
#         if is_ts:
#             self.ts_writer = writer
#             print('TS connected')
#         else:
#             self.stub_writer = writer
#             print('Stub connected')

        while self.running:
            data = await reader.read(READ_BUFFER)
            if data:
                self.log.debug('received {!r}'.format(data.decode('utf-8')))

                response = await self.prepare_response(data)

                self.sv_writer.write(response)
                self.sv_writer.drain()
                self.log.debug('sent {!r}'.format(response.decode('utf-8')))
            else:
                self.log.debug('connection closing')
                self.running = False

    async def connect_initiator():
        await asyncio.start_server(self.initiator_connected, HOST, self.initiator_port, self.loop)
#         await asyncio.start_server(lambda r, w: self.connected(r, w, False),
#                                    HOST, self.port_stub, loop=self.loop)

    async def connect_receiver():
        try:
            reader, writer = await asyncio.open_connection(HOST, self.port_receiver, self.loop)
        except (asyncio.TimeoutError, ConnectionRefusedError) as err:
            print('Error connecting to receiver: {}'.format(err))

    async def start(self):
        await self.connect_initiator()
        await self.connect_receiver()

    async def main_loop(self):
        while self.running:
            try:
                data = await sv_reader.read(READ_BUFFER)
                if data:
                    self.log.debug('received {!r}'.format(data.decode('utf-8')))

                    response = await self.prepare_response(data)

                    self.ts_writer.write(response)
                    self.ts_writer.drain()
                    self.log.debug('sent {!r}'.format(response.decode('utf-8')))
                else:
                    self.log.debug('connection closing')
                    self.running = False
            except Exception as err:
                print(f'Error: {err}')
                self.running = False

    async def stop(self):
        self.running = False
