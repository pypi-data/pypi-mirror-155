class PPIException(Exception):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value


class PPIInvalidCredentials(PPIException):
    pass


class PPIHTTPException(PPIException):
    def __init__(self, httpStatus, message):
        self.httpStatus = httpStatus
        self.message = message

    def __repr__(self):
        return self.httpStatus
