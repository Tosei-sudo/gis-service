try:
    import decsvr.ContentType as ContentType
except ImportError:
    import ContentType

class HttpRedirectException(Exception):
    def __init__(self, location):
        self.code = 302
        self.location = location

class HttpException(Exception):
    def __init__(self, code, message, content_type = ContentType.PLANE_TEXT):
        self.code = code
        self.message = message

class Http400Exception(HttpException):
    def __init__(self, message = 'Bad Request', content_type = ContentType.PLANE_TEXT):
        super(Http400Exception, self).__init__(400, message)

class Http400MissingParameterException(Http400Exception):
    def __init__(self, parameters, content_type = ContentType.PLANE_TEXT):
        super(Http400MissingParameterException, self).__init__('Missing parameter: ' + ", ".join(parameters))

class Http403Exception(HttpException):
    def __init__(self, message = 'Forbidden', content_type = ContentType.PLANE_TEXT):
        super(Http403Exception, self).__init__(403, message)

class Http404Exception(HttpException):
    def __init__(self, message = 'Not Found', content_type = ContentType.PLANE_TEXT):
        super(Http404Exception, self).__init__(404, message)

class Http500Exception(HttpException):
    def __init__(self, message = 'Internal Server Error', content_type = ContentType.PLANE_TEXT):
        super(Http500Exception, self).__init__(500, message)