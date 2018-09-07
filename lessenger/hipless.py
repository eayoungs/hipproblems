from __future__ import print_function
import tornado.ioloop
import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "http://hipmunk.github.io")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', ' POST, DELETE, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


class MainHandler(BaseHandler):

    def get(self):
        self.write("GET some!")

    def post(self):
        self.write({
                    "messages": [
                        {
                            "type": "text",
                            "text": "Sorry, I don't have any sandwiches, but have a picture instead:"
                        },
                        {
                            "type": "rich",
                            "html": "<img src='http://i.imgur.com/J9DLQ.png'>"
                        }
                    ]
                })


def make_app():
    return tornado.web.Application([
        (r"/chat/messages", MainHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(9000)
    tornado.ioloop.IOLoop.current().start()
