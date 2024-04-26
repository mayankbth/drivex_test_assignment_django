from rest_framework import status


def context_data_generator(info=None, status_code=status.HTTP_200_OK, error_message=None, data=None):
    context = {
        "info": info,
        "status_code": status_code,
        "error_message": error_message,
        "data": data
    }
    return context