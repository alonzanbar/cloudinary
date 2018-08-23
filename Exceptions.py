from flask import jsonify

class HTTP_Error_Hanlder(Exception):
    status_code = 404
    def __init__(self, message='Image URL is not available', status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class URLNotFound(HTTP_Error_Hanlder):

    def __init__(self, message='Image URL is not available', payload=None):
        super(URLNotFound,self).__init__(message,404,payload)



class InternalServerError(HTTP_Error_Hanlder):
    status_code = 500

    def __init__(self, message='Remote Server is having some issues, please try later', status_code=None, payload=None):
        super(InternalServerError, self).__init__(message, self.status_code, payload)