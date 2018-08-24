from __future__ import print_function
import sys
import json

from searchrunner.scrapers.common import Query

from tornado import gen, web, ioloop
from tornado.httpclient import AsyncHTTPClient


class FlightMetaSearchHandler(web.RequestHandler):
    def initialize(self, providers):
        self.providers = providers

    @gen.coroutine
    def get(self):
        try:
            combined_resp_dict = yield self.search_provider_flight()
        except:
            raise
        query = Query()
        results = yield query.run(combined_resp_dict['results'])
        self.write({
            "results": [r.serialize() for r in results],
        })

    @gen.coroutine
    def search_provider_flight(self):
        http_client = AsyncHTTPClient()
        try:
            fetch_dict = {}
            for provider in self.providers:
                fetch_dict[provider] = http_client.fetch(
                    'http://localhost:9000/scrapers/' + provider)
            resp_dict = yield fetch_dict
        except Exception as e:
            print(e)
            sys.exit(1)

        resps_list = []
        for resp in resp_dict.values():
            if resp.body and (not resp.body.isspace()):
                new_resp_list = json.loads(resp.body)['results']
                resps_list.append(new_resp_list)
        for index, resps_list in enumerate(resps_list):
            try:
                if resps_list[index][0]['agony'] > resps_list[index+1][len(resps_list[index+1])-1]['agony']:
                    temp = resps_list[index]
                    resps_list[index] = resps_list[index+1]
                    resps_list[index+1] = temp
            except:
                pass
        response = [resp for resp in resps_list]
        combined_resp_dict = {'results': response}

        raise gen.Return(combined_resp_dict)


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
