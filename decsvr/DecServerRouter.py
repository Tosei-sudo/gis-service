try:
    import decsvr.ContentType as ContentType
    import decsvr.DecServerRoute as DecServerRoute
except ImportError:
    import ContentType
    import DecServerRoute

class DecServerRouter():
    def __init__(self):
        self.__get_endpoints__ = []
        self.__post_endpoints__ = []
    
    def get(self, path, content_type = ContentType.APPLICATION_JSON, reqiure_params = []):
        def wrapper(func):
            self.__get_endpoints__.append(DecServerRoute.DecServerRoute(path, func, content_type, reqiure_params))
            return func
        return wrapper
    
    def post(self, path, content_type = ContentType.APPLICATION_JSON, reqiure_params = []):
        def wrapper(func):
            self.__post_endpoints__.append(DecServerRoute.DecServerRoute(path, func, content_type, reqiure_params))
            return func
        return wrapper