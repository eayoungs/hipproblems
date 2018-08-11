from __future__ import print_function
import sys

import json

from tornado import gen, web, ioloop
from tornado.httpclient import AsyncHTTPClient


class FlightMetaSearchHandler(web.RequestHandler):
    def initialize(self, providers):
        self.providers = providers

    @gen.coroutine
    def get(self):
        resp_list = []
        for provider in self.providers:
            resp = yield search_provider_flight(provider)
            if resp.body and (not resp.body.isspace()):
                resp_list.append(json.loads(resp.body))
        # response = sorted(resp_list, key=lambda r: r["agony"])

        print([resp['results'][0]['provider'] for resp in resp_list])
        self.write(resp_list[0])  # response)


@gen.coroutine
def search_provider_flight(provider):
    http_client = AsyncHTTPClient()
    try:
        response = yield http_client.fetch(
            'http://localhost:9000/scrapers/' + provider)
    except Exception as e:
        print(e)
        sys.exit(1)

    raise gen.Return(response)


ROUTES = [
    (r"/flights/search", FlightMetaSearchHandler, dict(
        providers=['expedia', 'orbitz', 'priceline', 'travelocity', 'united'])),
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
