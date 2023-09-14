from rest_framework.response import Response


# here a general handler for unexpected errors, I used it as annotation in views, it helps to keep application running.
# important for availability.
def error_handler(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as ex:
            res = {'error': str(ex)}
            return Response(res)

    return wrapper
