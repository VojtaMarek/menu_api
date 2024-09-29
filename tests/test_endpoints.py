import requests
from http import HTTPStatus
import pytest


URL_PREFIX = 'http://localhost:5000'

endpoints = [
    # app version
    ('get', f'{URL_PREFIX}/'),

    # restaurant
    ('post', f'{URL_PREFIX}/restaurant/test_name1?contact=test_c1&opening_hours=test_h1&address=test_a1'),
    ('post', f'{URL_PREFIX}/restaurant/test_name2?contact=test_c2&opening_hours=test_h2&address=test_a2'),
    ('get', f'{URL_PREFIX}/restaurant/1'),
    ('put', f'{URL_PREFIX}/restaurant/1?name=U%20Vočka&address=Vodičkova'),
    ('get', f'{URL_PREFIX}/restaurants'),

    # add food
    ('post', f'{URL_PREFIX}/food/1/Svíce?day=2024-09-30&price=239'),
    ('post', f'{URL_PREFIX}/food/1/Řízek?day=2024-09-30&price=199.9'),
    ('put', f'{URL_PREFIX}/food/1?day=2024-10-01&price=249'),
    ('get', f'{URL_PREFIX}/foods/1'),
    ('delete', f'{URL_PREFIX}/food/2'),  # řízek došel

    # delete restaurants, within the food (delete cascaded)
    # ('delete', f'{URL_PREFIX}/restaurant/1'),
    # ('delete', f'{URL_PREFIX}/restaurant/2'),
]


# Note, to run the test, start with the empty db - check to see the empty db after
@pytest.mark.parametrize("method, url", endpoints)
def test_endpoint_response(method, url):
    try:
        request_method = getattr(requests, method)
        res = request_method(url)
    except (ConnectionError, TimeoutError) as e:
        assert False, e
    assert res.status_code in {HTTPStatus.OK, HTTPStatus.CREATED}
    print(f'\n{res.content}')