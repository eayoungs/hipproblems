from __future__ import print_function
from tornado import gen, web, ioloop
from tornado.httpclient import AsyncHTTPClient


class FlightMetaSearchHandler(web.RequestHandler):
    def initialize(self, provider):
        self.provider = provider

    @gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(
            'http://localhost:9000/scrapers/' + self.provider)

        # print(response.body)
        self.write(response.body)


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
