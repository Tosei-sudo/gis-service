try:
    # Python 3
    from http.server import HTTPServer
    from socketserver import ThreadingMixIn

    from decsvr.DecServerHandler import DecServerHandler
except ImportError:
    # Python 2
    from BaseHTTPServer import HTTPServer
    from SocketServer import ThreadingMixIn

    from DecServerHandler import DecServerHandler

class DecServer(ThreadingMixIn, HTTPServer):
    def __init__(self, port = 8000, resoleve_files = False):
        self.__get_endpoints__ = []
        self.__post_endpoints__ = []
        self.__resoleve_files__ = resoleve_files

        HTTPServer.__init__(self, ('', port), DecServerHandler)

    def incude_router(self, router):
        self.__get_endpoints__.extend(router.__get_endpoints__)
        self.__post_endpoints__.extend(router.__post_endpoints__)
    
    def start(self):
        print('Starting WFS server on port %d...' % self.server_address[1])
        self.serve_forever()