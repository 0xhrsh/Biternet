import os
from .HTTPRequest import HTTPRequest
from .TCPServer import TCPServer


class HTTPServer(TCPServer):
    headers = {
        'Server': 'CrudeServer',
        'Content-Type': 'text/html',
    }
    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
    }

    def handle_request(self, data):
        # create an instance of HTTPRequest
        request = HTTPRequest(data)

        # Calling the Appropriate handler
        try:
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            handler = self.HTTP_501_handler

        response = handler(request)

        return response

    def handle_OPTIONS(self, request):
        response_line = self.response_line(200)

        extra_headers = {'Allow': 'OPTIONS, GET'}
        response_headers = self.response_headers(extra_headers)

        blank_line = "\r\n"

        return "%s%s%s" % (
            response_line,
            response_headers,
            blank_line
        )

    def handle_GET(self, request):
        filename = request.uri.strip('/')
        if os.path.exists(filename):
            response_line = self.response_line(200)
            response_headers = self.response_headers()
            with open(filename) as f:
                response_body = f.read()
        else:
            response_line = self.response_line(404)
            response_headers = self.response_headers()
            response_body = "<h1>404 Not Found</h1>"

        blank_line = "\r\n"

        return "%s%s%s%s" % (
            response_line,
            response_headers,
            blank_line,
            response_body
        )

    def HTTP_501_handler(self, request):
        response_line = self.response_line(status_code=501)
        response_headers = self.response_headers()
        blank_line = "\r\n"
        response_body = "<h1>501 Not Implemented</h1>"

        return "%s%s%s%s" % (
            response_line,
            response_headers,
            blank_line,
            response_body
        )

    def response_line(self, status_code):
        # Returns response line
        reason = self.status_codes[status_code]
        return "HTTP/1.1 %s %s\r\n" % (status_code, reason)

    def response_headers(self, extra_headers=None):
        headers_copy = self.headers.copy()  # make a local copy of headers

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in self.headers:
            headers += "%s: %s\r\n" % (h, self.headers[h])
        return headers
