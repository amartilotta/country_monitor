from datetime import datetime
from http import HTTPStatus

from rest_framework.response import Response


def _get_base_response(status: int, **kwargs) -> Response:
    return Response(kwargs, status=status)


def get_success_response(status: int, **kwargs) -> Response:
    return _get_base_response(status=status, **kwargs)


def get_error_response(status: int, message: str = "", **kwargs) -> Response:
    response = message or HTTPStatus(status).phrase

    return _get_base_response(
        message=response,  # If a message is not provided, one is obtained by default
        timestamp=datetime.now().isoformat(),
        status=status,
        **kwargs
    )
