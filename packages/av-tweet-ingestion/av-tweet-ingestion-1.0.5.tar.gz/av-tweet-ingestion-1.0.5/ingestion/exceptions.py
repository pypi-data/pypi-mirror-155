
class InvalidDataTypeForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Invalid data type {type(data)} for ingestion."
        super().__init__(self.message)


class InvalidParameterType(Exception):
    def __init__(self,param, expected):
        self.param = param
        self.expected = expected
        self.message = f"Invalid parameter datatype {param}, {expected} was expected."
        super().__init__(self.message)



class QueryErrorException(Exception):
    def __init__(self, message):
        self.message = f"Invalid query, message: {message}."
        super().__init__(self.message)


class AccessUnauthorizedException(Exception):
    def __init__(self, response_number):
        self.message = f"Access Unauthorized - Response Code {response_number}."
        super().__init__(self.message)