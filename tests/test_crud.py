from http import HTTPStatus

import requests
from utils.random_data import generate_random_data
from app.models.user import UserResponse


def create_user(app_url):
    name, surname, email, avatar = generate_random_data()
    response = requests.post(f"{app_url}/api/users/",
                             json={"email": email, "first_name": name, "last_name": surname, "avatar": avatar})
    assert response.status_code == HTTPStatus.CREATED
    response = UserResponse.model_validate(response.json())
    return response, name, surname, email, avatar


def test_create_user(app_url):
    user, name, surname, email, avatar = create_user(app_url)
    assert user.first_name == name
    assert user.last_name == surname
    assert user.email == email
    assert str(user.avatar) == avatar
    assert user.id is not None


def test_update_user(app_url, fill_test_data):
    user_id = fill_test_data[0]
    name, surname, email, avatar = generate_random_data()
    response = requests.patch(f"{app_url}/api/users/{user_id}",
                              json={"email": email, "first_name": name, "last_name": surname, "avatar": avatar})
    assert response.status_code == HTTPStatus.OK
    user = UserResponse.model_validate(response.json())
    assert user.first_name == name
    assert user.last_name == surname
    assert user.email == email
    assert str(user.avatar) == avatar
    assert user.id == user_id


def test_delete_user(app_url, fill_test_data):
    user_id = fill_test_data[0]
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_crud(app_url):
    user, name, surname, email, avatar = create_user(app_url)
    assert user.first_name == name
    user_id = user.id

    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    user = UserResponse.model_validate(response.json())
    assert user.first_name == name

    response = requests.patch(f"{app_url}/api/users/{user_id}",
                              json={"email": f'1{email}'})
    assert response.status_code == HTTPStatus.OK
    user = UserResponse.model_validate(response.json())
    assert user.email == f'1{email}'

    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_get_after_create_and_update(app_url):
    user, name, surname, email, avatar = create_user(app_url)
    user_id = user.id

    # Get user after creation
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    user = UserResponse.model_validate(response.json())
    assert user.first_name == name

    # Update user
    new_name = "UpdatedName"
    response = requests.patch(f"{app_url}/api/users/{user_id}",
                              json={"first_name": new_name})
    assert response.status_code == HTTPStatus.OK

    # Get user after update
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    user = UserResponse.model_validate(response.json())
    assert user.first_name == new_name


def test_method_not_allowed(app_url):
    response = requests.put(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED  # 405 status code


def test_delete_patch_errors(app_url):
    # Test 404 on delete
    response = requests.delete(f"{app_url}/api/users/999999")
    assert response.status_code == HTTPStatus.NOT_FOUND

    # Test 404 on patch
    response = requests.patch(f"{app_url}/api/users/999999",
                              json={"email": "nonexistent@example.com"})
    assert response.status_code == HTTPStatus.NOT_FOUND

    # Create user
    user, name, surname, email, avatar = create_user(app_url)
    user_id = user.id

    # Test 422 on patch with invalid data
    response = requests.patch(f"{app_url}/api/users/{user_id}",
                              json={"email": "invalid-email"})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_404_on_deleted_user(app_url):
    # Create user
    user, name, surname, email, avatar = create_user(app_url)
    user_id = user.id

    # Delete user
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK

    # Test 404 on get deleted user
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_validity_of_test_data(app_url):
    name, surname, email, avatar = generate_random_data()
    # Create user with invalid email
    response = requests.post(f"{app_url}/api/users/",
                             json={"email": "invalid-email",
                                   "first_name": name,
                                   "last_name": surname,
                                   "avatar": avatar})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Create user with invalid URL
    response = requests.post(f"{app_url}/api/users/",
                             json={"email": email,
                                   "first_name": name,
                                   "last_name": surname,
                                   "avatar": "invalid-url"})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user_without_required_field(app_url):
    name, surname, email, avatar = generate_random_data()
    response = requests.post(f"{app_url}/api/users/",
                             json={"first_name": name, "last_name": surname, "avatar": avatar})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
