import requests
from http import HTTPStatus
import pytest
from models.app_status import AppStatus


@pytest.mark.smoke
def test_service_is_up(app_url):
    response = requests.get(f"{app_url}/status")
    assert response.status_code == HTTPStatus.OK
    status = AppStatus.model_validate(response.json())
    assert status.users is True
    assert response.headers["content-type"] == "application/json"


@pytest.mark.smoke
def test_service_is_accessible(app_url):
    response = requests.get(app_url)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Service is running"}


@pytest.mark.smoke
def test_service_response_time(app_url):
    response = requests.get(app_url)
    assert response.elapsed.total_seconds() < 1


@pytest.mark.smoke
def test_service_headers(app_url):
    response = requests.get(app_url)
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'
