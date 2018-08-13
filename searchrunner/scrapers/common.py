from __future__ import print_function
import sys

from datetime import datetime, timedelta
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from .exceptions import FlightResultException


class FlightResult(object):

    def __init__(self, provider, price, flight_num,
                 depart_time, arrive_time):
        self.provider = provider
        self.price = price
        self.flight_num = flight_num
        self.depart_time = depart_time
        self.arrive_time = arrive_time

    @property
    def agony(self):
        duration = self.arrive_time - self.depart_time
        return duration.total_seconds() / self.price

    def serialize(self):
        return {
            "provider": self.provider,
            "agony": self.agony,
            "price": self.price,
            "flight_num": self.flight_num,
            "depart_time": self.depart_time.isoformat(),
            "arrive_time": self.arrive_time.isoformat(),
        }


class Scraper(object):

    provider = None

    @gen.coroutine
    def run(self):
        self.results = []

        # wait a bit
        yield gen.sleep(2)

        self.load_results()
        self.results.sort(key=lambda r: r.agony)

        raise gen.Return(self.results)

    def load_results(self):
        raise NotImplementedError

    def load_fake_results(self, range_iter):
        now = datetime.utcnow().replace(second=0, microsecond=0)
        for i in range_iter:
            price = 2000 - i
            flight_num = "UA%s" % (1000 + i)
            depart_time = now + timedelta(hours=i)
            arrive_time = depart_time + timedelta(hours=1, minutes=i / 20)
            self.add_result(
                price,
                flight_num,
                depart_time,
                arrive_time,
            )

    def add_result(self, price, flight_num,
                   depart_time, arrive_time):
        result = FlightResult(
            self.provider,
            price,
            flight_num,
            depart_time,
            arrive_time,
        )
        self.results.append(result)


class Query(Scraper):
    """"  """
    @gen.coroutine
    def run_all(self, providers):
        """  """
        self.results = []

        # wait a bit
        yield gen.sleep(2)

        self.load_results(providers)
        self.results.sort(key=lambda r: r.agony)

        raise gen.Return(self.results)

    def load_results(self, providers):
        """  """
        for provider in providers:
            response = yield self.query_providers_flights(providers)
            for key, value in response:
                provider = value['provider']
                price = value['price']
                flight_num = value['flight_num']
                depart_time = value['depart_time']
                arrive_time = value['arrive_time']
                self.add_result(
                    provider,
                    price,
                    flight_num,
                    depart_time,
                    arrive_time,
                )

    def add_result(self, provider, price, flight_num,
                   depart_time, arrive_time):
        result = FlightResult(
            provider,
            price,
            flight_num,
            depart_time,
            arrive_time,
        )
        self.results.append(result)
        sys.exit(0)

    @gen.coroutine
    def query_all_providers_flights(self, providers):
        """ Query flight providers' APIs and return a dictionary containing a
        single list

        Args:
            providers (list)
        Returns:
            resp_dict (dictionary)
        """
        http_client = AsyncHTTPClient()
        try:
            fetch_dict = {}
            for provider in providers:
                fetch_dict[provider] = http_client.fetch(
                    'http://localhost:9000/scrapers/' + provider)
            resp_dict = yield fetch_dict
            sys.exit(0)
        except Exception as e:
            print(e)
            sys.exit(1)

        raise gen.Return(resp_dict)
