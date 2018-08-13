class SearchRunnerException(Exception):
    """docstring for SearchRunnerException"""
    def __init__(self, msg, original_exception):
        super(SearchRunnerException, self).__init__(
            msg + (": {}".format(original_exception)))
        self.msg = msg


class FlightResultException(Exception):
    """docstring for FlightResultException"""
    def __init__(self, FlightResult, msg=None):
        if msg is None:
            msg = "An error occured with {}".format(FlightResult)
        super(FlightResultException, self).__init__(msg)
        self.FlightResult = FlightResult
