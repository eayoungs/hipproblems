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
        try:
            resp_dict = yield search_provider_flight(self.providers)
        except:
            raise
        for resp in resp_dict.values():
            if resp.body and (not resp.body.isspace()):
                resp_list = resp_list + json.loads(resp.body)['results']
            response = sorted(resp_list, key=lambda r: r["agony"])
            combined_resp_dict = {'results': response}

        self.write(combined_resp_dict)


@gen.coroutine
def search_provider_flight(providers):
    http_client = AsyncHTTPClient()
    try:
        fetch_dict = {}
        for provider in providers:
            fetch_dict[provider] = http_client.fetch(
                'http://localhost:9000/scrapers/' + provider)
        resp_dict = yield fetch_dict
    except Exception as e:
        print(e)
        sys.exit(1)

    raise gen.Return(resp_dict)


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
