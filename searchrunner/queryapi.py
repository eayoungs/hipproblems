from __future__ import print_function
from tornado import gen, web, ioloop

import json


class FlightMetaSearchHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.write(json.dumps({"results": [{"provider": "Expedia"}]}))


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
