from __future__ import print_function
import json

from tornado import gen, web, ioloop
from searchrunner.scrapers.common import Query


class FlightMetaSearchHandler(web.RequestHandler):
    def initialize(self, providers):
        self.providers = providers

    @gen.coroutine
    def get(self):
        query = Query()
        resp_list = []
        try:
            resp_dict = yield query.search_provider_flight(self.providers)
        except:
            raise
        for resp in resp_dict.values():
            if resp.body and (not resp.body.isspace()):
                resp_list = resp_list + json.loads(resp.body)['results']
            response = sorted(resp_list, key=lambda r: r["agony"])
            combined_resp_dict = {'results': response}

        self.write(combined_resp_dict)


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
