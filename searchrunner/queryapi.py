from __future__ import print_function

import json

from tornado import gen, web, ioloop
from tornado.httpclient import AsyncHTTPClient


class FlightMetaSearchHandler(web.RequestHandler):
    def initialize(self, provider):
        self.provider = provider

    @gen.coroutine
    def get(self):
        resp = yield search_provider_flight(self.provider)
        resp_dict = json.loads(resp.body)

        self.write(resp_dict)


@gen.coroutine
def search_provider_flight(provider):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(
        'http://localhost:9000/scrapers/' + provider)
    if not response:
        raise web.HTTPError(404)

    raise gen.Return(response)


ROUTES = [
    (r"/flights/search", FlightMetaSearchHandler, dict(provider='expedia')),
]


def run():
    app = web.Application(
        ROUTES,
        debug=True
    )

    app.listen(8000)
    print("Server (re)started on port 8000")

    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()
