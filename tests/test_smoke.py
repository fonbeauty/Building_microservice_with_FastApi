import requests
from http import HTTPStatus
import pytest


@pytest.mark.smoke
def test_service_is_up(app_url):
    response = requests.get(f"{app_url}/status")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"database": True}
    assert response.headers["content-type"] == "application/json"


@pytest.mark.smoke
def test_service_is_accessible(app_url):
    response = requests.get(app_url)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Service is running"}


@pytest.mark.smoke
def test_service_responds_on_port_8002(app_url):
    response = requests.get(app_url)
    assert response.status_code == HTTPStatus.OK
    assert ":8002" in app_url


@pytest.mark.smoke
def test_service_response_time(app_url):
    response = requests.get(app_url)
    assert response.elapsed.total_seconds() < 1


@pytest.mark.smoke
def test_service_headers(app_url):
    response = requests.get(app_url)
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'


@pytest.mark.smoke
def test_service_http_access(app_url):
    assert app_url.startswith("http://"), "URL should start with http://"

    response = requests.get(app_url)

    assert response.status_code == HTTPStatus.OK
