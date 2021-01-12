from rest_framework.response import Response
from core.helpers import Error


class DoesNotVerify(Exception):
    pass


class DoesNotMatch(Exception):
    pass


class Exist(Exception):
    pass


class DoesNotValid(Exception):
    pass


class TimeDoesNotValid(Exception):
    pass
