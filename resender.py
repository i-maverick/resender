import asyncio
import logging
import sys

READ_BUFFER = 4096
HOST = '127.0.0.1'


class Resender:
    def __init__(self, data, loop):
        self.id = data['id']
        self.name = data['name']
        self.port_sv = data['port_sv']
        self.port_ts = data['port_ts']
        self.port_stub = data['port_stub']
        self.skip_ts = data['skip_ts']
        self.running = True
        self.loop = loop

        self.sv_writer = None
        self.ts_writer = None
        self.stub_writer = None

        self.setup_logger()
        self.log = logging.getLogger('{}'.format(self.name))

    @staticmethod
    def setup_logger():
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(name)s: %(message)s',
            stream=sys.stdout,
        )

    @staticmethod
    async def get_connection(host, port, loop):
        try:
            reader, writer = await asyncio.open_connection(host=host, port=port, loop=loop)
            return reader, writer
        except (asyncio.TimeoutError, ConnectionRefusedError) as err:
            print('Error connecting to SV: {}'.format(err))
            return None, None

    @staticmethod
    async def prepare_response(data):
        return data

    async def start(self):
        await asyncio.start_server(lambda r, w: self.connected(r, w, True),
                                   HOST, self.port_ts, loop=self.loop)
        await asyncio.start_server(lambda r, w: self.connected(r, w, True),
                                   HOST, self.port_stub, loop=self.loop)

    async def connected(self, reader, writer, is_ts):
        if is_ts:
            self.ts_writer = writer
            print('TS connected')
        else:
            self.stub_writer = writer
            print('Stub connected')

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

    async def main_loop(self):
        sv_reader, self.sv_writer = await self.get_connection(HOST, self.port_sv, self.loop)
        if not sv_reader or not self.sv_writer:
            return

        await self.start()  # should be called from rest api

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
