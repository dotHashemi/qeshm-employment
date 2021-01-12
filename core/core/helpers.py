from rest_framework.response import Response


class Error():
    def throw(message, status):
        return Response({
            "detail": message
        }, status=status)


class Success():
    def responseWithData(data, status):
        return Response({
            "data": data
        }, status=status)

    def response(message, status):
        return Response({
            "detail": message
        }, status=status)
