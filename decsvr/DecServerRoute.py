import ContentType
import HttpException
import re

class DecServerRoute:
    def __init__(self, path, function, content_type = ContentType.APPLICATION_JSON, reqiure_params = []):
        self.function = function
        self.path = path
        
        self.content_type = content_type
        self.reqiure_params = reqiure_params
        
        if path.find('{') == -1:
            self.path_pattern = None
        else:
            self.path_pattern = re.compile(re.sub(r'\{.*?\}', '\w+', path))

    def match(self, pattern):
        if self.path == pattern:
            return True
        elif self.path[-1] == "*" and pattern.startswith(self.path[:-1]):
            return True
        elif self.path_pattern and self.path_pattern.match(pattern):
            return True
    
    def check_params(self, request_info):
        missing_params = []
        for param in self.reqiure_params:
            if param not in request_info.query:
                missing_params.append(param)
        if missing_params:
            raise HttpException.Http400MissingParameterException(missing_params)
        return