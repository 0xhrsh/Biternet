class HTTPRequest:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = '1.1'  # default to HTTP/1.1
        self.headers = {}  # a dictionary for headers

        self.parse(data.decode("utf-8"))

    def parse(self, data):
        lines = data.strip().split('\r\n')

        request_line = lines[0]
        self.parse_request_line(request_line)
        self._parse_headers(lines)
        
    def _parse_headers(self, lines):
        for index in range(1, len(lines)):
            header = lines[index].split(':')
            self.headers[header[0]] = header[1]

    def parse_request_line(self, request_line):
        words = request_line.split(' ')
        self.method = words[0]
        self.uri = words[1]

        if len(words) > 2:
            self.http_version = words[2]
