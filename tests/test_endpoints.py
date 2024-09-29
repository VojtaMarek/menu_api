from typing import Final
import requests
from http import HTTPStatus
import pytest
import json

def get_access_token():
    try:
        res = requests.get(f'{url_prefix}/token')
        return json.loads(res.text).get('data').get('token')
    except Exception:
        return 'Failed-to-get-token.'


# constants
url_prefix: Final[str] = 'http://localhost:5000'
headers: Final[dict] = {'Authorization': f'Bearer {get_access_token()}'}

endpoints = [
    # app version
    ('get', f'{url_prefix}/'),

    # restaurant
    ('post', f'{url_prefix}/restaurant/test_name1?contact=test_c1&opening_hours=test_h1&address=test_a1'),
    ('post', f'{url_prefix}/restaurant/test_name2?contact=test_c2&opening_hours=test_h2&address=test_a2'),
    ('get', f'{url_prefix}/restaurant/1'),
    ('put', f'{url_prefix}/restaurant/1?name=U%20Vočka&address=Vodičkova'),
    ('get', f'{url_prefix}/restaurants'),

    # add food
    ('post', f'{url_prefix}/food/1/Svíce?day=2024-09-30&price=239'),
    ('post', f'{url_prefix}/food/1/Řízek?day=2024-09-30&price=199.9'),
    ('put', f'{url_prefix}/food/1?day=2024-10-01&price=249'),
    ('get', f'{url_prefix}/foods/1'),
    ('delete', f'{url_prefix}/food/2'),  # řízek došel

    # delete restaurants, within the food (delete cascaded)
    ('delete', f'{url_prefix}/restaurant/1'),
    ('delete', f'{url_prefix}/restaurant/2'),
]


# Note, to run the test, start with the empty db - check to see the empty db after
@pytest.mark.parametrize("method, url", endpoints)
def test_endpoint_response(method, url):
    try:
        request_method = getattr(requests, method)
        res = request_method(url, headers=[] if method == 'get' else headers)
    except (ConnectionError, TimeoutError) as e:
        assert False, e
    assert res.status_code in {HTTPStatus.OK, HTTPStatus.CREATED}
    print(f'\n{res.content}')