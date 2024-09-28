import requests
from http import HTTPStatus

from src.menu_api import __version__

STATUS_OK = 200

def test_version():
    try:
        res = requests.get("http://localhost:5000/version")
    except (ConnectionError, TimeoutError):
        res = None
    assert res.status_code == HTTPStatus.OK
    assert __version__ in str(res.content)
