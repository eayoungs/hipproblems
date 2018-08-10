from __future__ import print_function
from tornado import gen, web, ioloop


class GenAsyncHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        print("flights/search")


ROUTES = [
    (r"/flights/search", GenAsyncHandler),
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
