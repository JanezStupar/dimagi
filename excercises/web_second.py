from BaseHTTPServer import HTTPServer
import datetime

__author__ = 'Janez Stupar'

import web_first
import urlparse


class MemoryStorage(object):
    """
    A simple memory storage database, with a braindead API.

    push and history functions implement the data protocol.
    """

    def __init__(self):
        """
        Schema
        """
        self._storage = []

    def _last_n(self, number=None):
        """
        Return last <number> of entries. If no <number> is specified return all.
        """
        if number is None:
            return self._storage
        return self._storage[-(number):]

    def _from_timestamp(self, timestamp):
        """
        Return the entries since <timestamp>.
        """
        return [x for x in self._storage if x['timestamp'] >= timestamp]

    def push(self, entry):
        """
        Append new entry in the order of arrival.
        """
        self._storage.append(entry)

    def history(self, **kwargs):
        """
        Fetch stuff from history.
        """
        if "last" in kwargs:
            return self._last_n(kwargs['last'])
        elif "timestamp" in kwargs:
            return self._from_timestamp(kwargs['timestamp'])
        else:
            return self._last_n()



class ArithmeticHistoryRequestHandler(web_first.ArithmeticRequestHandler):
    """
    An extension of ArithmeticRequestHandler that adds functionality of storing history of the previous computations
    and enabling access to it.

    All the application logic is handled within a single handler, this is not something one would do in any
    real life scenario. Unless this real life scenario is as dead simple as this one.

    This implementation uses memory storage. The purpose is to make a point of my pragmatism. To that
    end storage is implemented as a backend that should be pretty simple to extend should the
    situation require such.

    Inputs and outputs:

    /history/ takes parameters:
        'last=n' - which returns last n elements.
        'timestamp="<ISO8601_timestamp>"'  - returns elements newer than the specified timestamp
        without any parameters all the results are returned

    /history/ returns a list of json objects containing following fields: ['ip', 'timestamp', 'values', 'sum', 'product']
    """

    def __init__(self, request, client_address, server, storage_backend_cls=MemoryStorage):
        """
        Use server object to persist history storage between requests. Not something one would usually do.
        However since I wanted to use memory based storage this is the simplest way. For any real piece of
        work some more sophisticated and safer method would be used.
        """
        if hasattr(server, '_history'):
            self._history = server._history
        else:
            self._history = storage_backend_cls()
            server._history = self._history
        web_first.ArithmeticRequestHandler.__init__(self, request, client_address, server)

    def _store_history(self, values, results):
        """
        Compute a history entry and push it to the history storage.
        """
        history_entry = {
            "ip": self.client_address[0],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "values": values,
            "sum": results['sum'],
            "product": results['product']
        }
        self._history.push(history_entry)

    def _compute_result(self, values):
        result = web_first.ArithmeticRequestHandler._compute_result(self, values)
        self._store_history(values, result)

        return result

    def _process_arithmetic_request(self, params):
        self._validate_arithmetic_params(params)
        retval = self._compute_result(params['values'])
        return self._serialize_result(retval)

    def _process_history_request(self, params):
        translated_params = {k: v[0] for k, v in params.iteritems()}
        retval = self._history.history(**translated_params)
        return self._serialize_result(retval)

    def resolve_route(self):
        """
        This is a simple url resolver. Quick and dirty, just as it should be in a proof of concept.

        Returns the worker function.
        """
        url = urlparse.urlparse(self.path)
        if url.path == '/history/':
            return self._process_history_request
        else:
            return self._process_arithmetic_request

    def do_GET(self):
        try:
            params = self._parse_get()

            handler = self.resolve_route()
            retval = handler(params)

            self._send_response(200, retval)

        except Exception, e:
            self._send_response(500, {"error": e.message})

    def do_POST(self):
        try:
            params = self._parse_post()

            handler = self.resolve_route()
            retval = handler(params)

            self._send_response(200, retval)

        except Exception, e:
            self._send_response(500, {"error": e.message})


def run(server_class=HTTPServer, handler_class=ArithmeticHistoryRequestHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd on port: %s ...' % port
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run(port=8080)
