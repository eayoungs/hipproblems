from __future__ import print_function

from tornado import gen, web, ioloop
from searchrunner.scrapers.common import Query


class FlightMetaSearchHandler(web.RequestHandler):
    def initialize(self, providers):
        self.providers = providers

    @gen.coroutine
    def get(self):
        query = Query()
        try:
            results = yield query.run_all(self.providers)
            self.write({
                "results": [r.serialize() for r in results],
            })
        except:
            raise

    def handle_responses(response):
        pass


ROUTES = [
    (r"/flights/search", FlightMetaSearchHandler, dict(
        providers=['expedia',
                   'orbitz',
                   'priceline',
                   'travelocity',
                   'united'
                   ]
        )
    ),
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
