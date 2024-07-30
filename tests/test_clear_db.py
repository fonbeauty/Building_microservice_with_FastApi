from http import HTTPStatus

import requests
import pytest


@pytest.mark.order("last")
def test_delete_all_data_db(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    users = response.json().get("items", [])
    for user in users:
        requests.delete(f"{app_url}/api/users/{user['id']}")

    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json().get("items", []) == []
