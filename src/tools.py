from http import HTTPStatus as Status
from typing import Type

from flask import jsonify


def status_json(code: int, message: str, data = None) -> tuple[Type[jsonify], int]:
    http_code_ranges = {"informational": Status(code).is_informational,
                        "success": Status(code).is_success,
                        "redirection": Status(code).is_redirection,
                        "client error": Status(code).is_client_error,
                        "server error": Status(code).is_server_error}
    res: dict = {
        "status": next(k for k, v in http_code_ranges.items() if v),
        "message": message,
        "errors": {
            "code": code,
            "detail": "Invalid input data." if code == 400 else "Error."
        },
        "data": data,
    }
    if not data:
        res.pop('data')
    else:
        res.pop('errors')
    return jsonify(res), code
