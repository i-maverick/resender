import json
from aiohttp import web
from data import resender_data

from resender import Resender

HOST = '127.0.0.1'
PORT = 8000

NOT_FOUND = 'Resender id={} is not found'
NOT_SUPPORTED = 'Action {} is not supported'

resenders = {}

routes = web.RouteTableDef()


@routes.get('/resenders')
def resender_list(request):
    res = [res.__dict__ for res in resenders.values()]
    return response({'resenders': res})


@routes.get('/resenders/{id}/')
def resender(request):
    id = int(request.match_info.get('id'))
    if id not in resenders:
        return error(NOT_FOUND.format(id))
    return response({'resender': resenders[id].__dict__})


@routes.get('/resenders/{id}/{action}')
def action(request):
    id = int(request.match_info.get('id'))
    action = request.match_info.get('action')
    if id not in resenders:
        return error(NOT_FOUND.format(id))
    res = resenders[id]
    try:
        ret = getattr(res, action)()
        return response({'result': ret})
    except AttributeError:
        return error(NOT_SUPPORTED.format(action))


@routes.get('/resenders/start_all')
def start_all():
    for res in resenders.values():
        res.start()
    return response({'result': 'Ok'})


def response(obj):
    return web.Response(status=200, body=json.dumps(obj))


def error(msg):
    print(f'Error: {msg}')
    return web.Response(status=400, body=msg)


if __name__ == '__main__':
    resenders = {res['id']: Resender(res) for res in resender_data}
    app = web.Application()
    app.router.add_routes(routes)
    web.run_app(app, host=HOST, port=PORT)
