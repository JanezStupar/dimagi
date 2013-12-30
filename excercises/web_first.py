__author__ = 'Janez Stupar'

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import json
import cgi


def product(numbers):
    """
    Calculate a product of list of numbers
    """
    tmp = 1
    for num in numbers:
        tmp *= num
    return tmp


class ArithmeticRequestHandler(BaseHTTPRequestHandler):
    """
    Simple service that takes a list of numbers as URL query string parameters or POST form data and computes
    their sum and product.

    Input: field named "values" with value specified as a JSON list of numbers

    Output: JSON object containing the sum and product of inputs.

    Examples:
        GET /?values=[1,2,4,-7]
        > {"sum": 0, "product": -56}

        POST /
        DATA: "values=[1,2,4,-7]"
        > {"sum": 0, "product": -56}
    """

    def _compute_result(self, values):
        """
        Takes a list of field values as parsed from querystring or POST form data and returns a JSON object
        containing the product and sum.
        """
        _sum = 0
        _product = 1

        # HTTP allows for multiple instances of same field to appear.
        for numbers in values:
            _sum += sum(numbers)
            _product *= product(numbers)

        return {
            'sum': _sum,
            'product': _product
        }

    @staticmethod
    def _serialize_result(value):
        return json.dumps(value)

    @staticmethod
    def _parse_json_params(params):
        """
        Take a dictionary containing list of field values and parse them as json values.
        """
        # Parse parameter values from JSON to Python
        for k, v in params.iteritems():
            parsed_val = []
            for value in v:
                parsed_val.append(json.loads(value))
            params[k] = parsed_val

        return params

    @staticmethod
    def _validate_arithmetic_params(params):
        """
        Sanity check.
        """
        _MANDATORY_FIELDS = ['values']

        for field in _MANDATORY_FIELDS:
            if not field in params:
                raise ValueError("Mandatory field %s is missing" % field)

            if params[field] is None:
                raise ValueError("Mandatory field %s value is missing" % field)

    def _send_response(self, code, retval):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(retval)
        self.wfile.write("\r\n")

    def _parse_get(self):
        """
        Handle the querystring parameters.
        """
        url = urlparse.urlparse(self.path)
        tmp = urlparse.parse_qs(urlparse.unquote(url.query))

        return self._parse_json_params(tmp)

    def _parse_post(self):
        """
        Handle the POST data parameters.
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'], }
        )

        params = {}
        for entry in form.list:
            if entry.name in params:
                params[entry.name].append(entry.value)
            else:
                params[entry.name] = [entry.value]

        return self._parse_json_params(params)

    def do_GET(self):
        params = self._parse_get()
        self._validate_arithmetic_params(params)

        retval = self._compute_result(params['values'])
        retval = self._serialize_result(retval)
        self._send_response(200, retval)

    def do_POST(self):
        params = self._parse_post()
        self._validate_arithmetic_params(params)

        retval = self._compute_result(params['values'])
        retval = self._serialize_result(retval)
        self._send_response(200, retval)


def run(server_class=HTTPServer, handler_class=ArithmeticRequestHandler, port=80):
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


