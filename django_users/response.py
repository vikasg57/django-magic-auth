from rest_framework import status as http_status
from rest_framework.response import Response


class APIResponse(Response):

    def __init__(self, data=None, status=http_status.HTTP_200_OK, success=None, content_type='application/json', **kwargs):
        success = (http_status.is_success(status)
                   if success is None
                   else success)

        key = "data" if success else "error"
        response_data = {
            'success': success,
            key: data
        }
        super(APIResponse, self).__init__(data=response_data,
                                          status=status,
                                          content_type=content_type,
                                          **kwargs)