from rest_framework.exceptions import APIException


class UserDoesNotExist(APIException):
    status_code = 400
    default_detail = "user does not exists"
    default_code = "users does not exists"
