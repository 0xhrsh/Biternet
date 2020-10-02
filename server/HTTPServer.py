from FileDistribution import FileDistributor
from HTTPRequest import HTTPRequest
from TCPServer import TCPServer

blank_line = "\r\n"


class HTTPServer(TCPServer):
    headers = {
        'Server': 'CrudeServer',
        'Content-Type': 'text/html',
    }
    status_codes = {
        200: 'OK',
        201: 'File Downloaded Successfully',
        400: 'Bad Request',
        404: 'Not Found',
        501: 'Not Implemented',
    }
    Sessions = {}

    def handle_request(self, data):
        # create an instance of HTTPRequest
        request = HTTPRequest(data)

        # Calling the Appropriate handler
        try:
            handler = getattr(self, "handle_" + request.method)
        except AttributeError:
            handler = self.HTTP_501_handler

        response = handler(request)

        return response

    def handle_OPTIONS(self, request):
        response_line = self.response_line(200)

        extra_headers = {'Allow': 'OPTIONS, GET, BIT'}
        response_headers = self.response_headers(extra_headers)

        return "%s%s%s" % (
            response_line,
            response_headers,
            blank_line
        )

    def handle_GET(self, request):
        cmd = request.uri.strip('/')

        try:
            get = cmd.split('/')[0]
            if(get == "token"):
                return self.get_token(cmd.split('/')[1])
            elif(get == "chunk"):
                return self.get_chunk(cmd.split('/')[1])
            else:
                response_line = self.response_line(400)
                response_headers = self.response_headers()
                response_body = "<h1>400 No Such Operation</h1>"
        except IndexError:
            response_line = self.response_line(400)
            response_headers = self.response_headers()
            response_body = "<h1>400 Bad Request</h1>"

        return "%s%s%s%s" % (
            response_line,
            response_headers,
            blank_line,
            response_body
        )

    def get_token(self, fileID):
        file = FileDistributor(fileID)

        if file.valid:
            response_line = self.response_line(200)
            response_headers = self.response_headers()
            sessionID = file.create_session()
            self.Sessions[str(sessionID)] = file
            response_body = sessionID
        else:
            response_line = self.response_line(404)
            response_headers = self.response_headers()
            response_body = "<h1>404 File Not Found</h1>"

        return "%s%s%s%s" % (
            response_line,
            response_headers,
            blank_line,
            response_body
        )

    def get_chunk(self, sessionID):
        chunk_no = -1

        try:
            chunk_no, response_body = self.Sessions[sessionID].get_next_chunk()
            response_line = self.response_line(200)
            response_headers = self.response_headers()

            if(not response_body):
                del self.Sessions[sessionID]
                response_line = self.response_line(201)

        except KeyError:
            response_body = "<h1>404 Session Not Found</h1>"
            response_line = self.response_line(404)
            response_headers = self.response_headers()

        data = {
            "chunkNum": chunk_no,
            "text": response_body,
        }

        return "%s%s%s%s" % (
            response_line,
            response_headers,
            blank_line,
            str(data),
        )

    def HTTP_501_handler(self, request):
        response_line = self.response_line(status_code=501)
        response_headers = self.response_headers()
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
