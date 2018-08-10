from __future__ import print_function
from tornado import gen, web, ioloop
from tornado.httpclient import AsyncHTTPClient
from searchrunner.scrapers import get_scraper


class FlightMetaSearchHandler(web.RequestHandler):
    @gen.coroutine
    def get(self, *providers):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(
            'http://localhost:9000/scrapers/expedia')

        # print(response.body)
        self.write(response.body)


ROUTES = [
    (r"/flights/search", FlightMetaSearchHandler),
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
