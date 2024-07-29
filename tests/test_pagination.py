from http import HTTPStatus

import pytest
import requests
from app.models.paginated import PaginatedResponse
from app.models.error import ErrorResponse

TOTAL_USERS = 12


@pytest.mark.usefixtures("fill_test_data")
@pytest.mark.parametrize("size, page", [(5, 1), (3, 2), (2, 3), (1, 4), (1, 5)])
def test_pagination_with_default_values(app_url, size, page):
    response = requests.get(f"{app_url}/api/users/?size={size}&page={page}")
    assert response.status_code == HTTPStatus.OK
    data = PaginatedResponse.model_validate(response.json())
    assert len(data.items) == size
    assert data.total > size
    assert data.page == page


@pytest.mark.parametrize("size, page", [(0, 1), (1, 0), (0, 0), (-1, 1), (1, -1), (-1, -1)])
def test_pagination_with_invalid_values(app_url, size, page):
    response = requests.get(f"{app_url}/api/users/?size={size}&page={page}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    errors = ErrorResponse.model_validate(response.json()).detail
    assert any('Input should be greater than or equal to 1' in error.msg for error in errors)


def test_pagination_without_size_and_only_first_page(app_url):
    response = requests.get(f"{app_url}/api/users/?page=1")
    assert response.status_code == HTTPStatus.OK
    data = PaginatedResponse.model_validate(response.json())
    assert len(data.items) == data.total


@pytest.mark.usefixtures("fill_test_data")
@pytest.mark.parametrize("page", [2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_pagination_without_size_and_pages(app_url, page):
    response = requests.get(f"{app_url}/api/users/?page={page}")
    assert response.status_code == HTTPStatus.OK
    data = PaginatedResponse.model_validate(response.json())
    assert len(data.items) == 0
    assert data.size == 50


@pytest.mark.parametrize("size", [0, -1, -10])
def test_pagination_without_size_and_invalid_page(app_url, size):
    response = requests.get(f"{app_url}/api/users/?size={size}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    errors = ErrorResponse.model_validate(response.json()).detail
    assert any('Input should be greater than or equal to 1' in error.msg for error in errors)


@pytest.mark.usefixtures("fill_test_data")
@pytest.mark.parametrize("size", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_pagination_with_only_size(app_url, size):
    response = requests.get(f"{app_url}/api/users/?size={size}")
    assert response.status_code == HTTPStatus.OK
    data = PaginatedResponse.model_validate(response.json())
    assert len(data.items) == size
    assert data.page == 1


@pytest.mark.parametrize("size", [-1, 0, -10])
def test_pagination_without_page_and_invalid_size(app_url, size):
    response = requests.get(f"{app_url}/api/users/?size={size}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    errors = ErrorResponse.model_validate(response.json()).detail
    assert any('Input should be greater than or equal to 1' in error.msg for error in errors)


@pytest.mark.parametrize("size", [1, 2, 3, 4, 5])
def test_correct_number_of_pages(app_url, size):
    response = requests.get(f"{app_url}/api/users/?size={size}&page=1")
    assert response.status_code == HTTPStatus.OK
    data = PaginatedResponse.model_validate(response.json())
    total_pages = (data.total + size - 1) // size
    assert data.pages == total_pages


def test_different_data_for_different_pages(app_url):
    # Request data for page 1
    response_page_1 = requests.get(f"{app_url}/api/users/?size=2&page=1")
    assert response_page_1.status_code == HTTPStatus.OK
    data_page_1 = PaginatedResponse.model_validate(response_page_1.json())

    # Request data for page 2
    response_page_2 = requests.get(f"{app_url}/api/users/?size=2&page=2")
    assert response_page_2.status_code == HTTPStatus.OK
    data_page_2 = PaginatedResponse.model_validate(response_page_2.json())

    # Ensure the data for page 1 and page 2 are different
    assert data_page_1.items != data_page_2.items
