import json

try:
    # Python 3
    from urllib.parse import urlparse, parse_qs
    
    from http.server import BaseHTTPRequestHandler
    import decsvr.ContentType as ContentType
except ImportError:
    # Python 2
    from urlparse import urlparse, parse_qs

    from BaseHTTPServer import BaseHTTPRequestHandler
    import ContentType

class GetRequest(object):
    def __init__(self, path, query):
        self.path = path
        self.query = query

class PostRequest(object):
    def __init__(self, path, query, body):
        self.path = path
        self.query = query
        self.body = body

class BasicHandler(BaseHTTPRequestHandler):
    def send_http_response(self, status_code = 200, content_type = ContentType.PLANE_TEXT, content = None, extend = {}):
        
        if content_type == ContentType.APPLICATION_JSON:
            content = json.dumps(content)

        self.send_response(status_code)
        
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        
        if content:
            self.send_header('Content-Length', str(len(content)))        
        self.send_header('Connection', 'keep-alive')
        self.send_header('Last-Modified', self.date_time_string())
        
        self.send_header('Content-type', ContentType.get_mime_by_content_code(content_type))
        
        for key in extend.keys():
            self.send_header(key, extend[key])
        
        self.end_headers()
        
        try:
            content = bytes(content, 'UTF-8')
        except:
            pass
        
        self.wfile.write(content)

    def do_GET(self):
        parsed_path = urlparse(self.path)

        query = parse_qs(parsed_path.query)
        request_info = GetRequest(parsed_path.path, query)
        self.handle_get_request(request_info)
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_info = PostRequest(parsed_path.path, query, post_data)
        self.handle_post_request(request_info)
    
    def do_OPTIONS(self):
        self.send_http_response(200, ContentType.PLANE_TEXT, 'OK')