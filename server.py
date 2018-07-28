import json
from aiohttp import web
from manager import Manager

HOST = '127.0.0.1'
PORT = 8000


class Server:
    def __init__(self):
        self.manager = Manager()

    def setup_routes(self, app):
        app.router.add_get('/resenders', self.resender_list)
        app.router.add_get('/resenders/{id}/', self.resender)
        app.router.add_get('/resenders/{id}/start', self.start)
        app.router.add_get('/resenders/{id}/stop', self.stop)
        app.router.add_get('/resenders/start_all', self.start_all)
        app.router.add_get('/resenders/stop_all', self.stop_all)

    def run(self):
        app = web.Application()
        self.setup_routes(app)
        web.run_app(app, host=HOST, port=PORT)

    async def resender_list(self, request):
        lst = await self.manager.resender_list()
        return self.response({'resenders': lst})

    async def resender(self, request):
        id = int(request.match_info.get('id'))
        ret = await self.manager.resender(id)
        if ret:
            return self.response(ret)

    async def start(self, request):
        id = int(request.match_info.get('id'))
        ret = await self.manager.start(id)
        if ret:
            return self.response({'result': ret})

    async def stop(self, request):
        id = int(request.match_info.get('id'))
        ret = await self.manager.stop(id)
        if ret:
            return self.response({'result': ret})

    async def start_all(self, request):
        ret = await self.manager.start_all()
        return self.response({'result': ret})

    async def stop_all(self, request):
        ret = await self.manager.stop_all()
        return self.response({'result': ret})

    @staticmethod
    def response(obj):
        return web.Response(status=200, body=json.dumps(obj))

    @staticmethod
    def error(msg):
        print(f'Error: {msg}')
        return web.Response(status=400, body=msg)


if __name__ == '__main__':
    server = Server()
    server.run()
