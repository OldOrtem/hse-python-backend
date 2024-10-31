from datetime import datetime
from http import HTTPStatus

from pydantic import SecretStr
import pytest
from fastapi.testclient import TestClient

from lecture_4.demo_service.api.main import create_app
from lecture_4.demo_service.api.utils import initialize
from lecture_4.demo_service.core.users import UserInfo, UserRole, UserService, password_is_longer_than_8


@pytest.fixture()
def test_client():
    app = create_app()
    user_service = UserService(password_validators=[password_is_longer_than_8])
    user_service.register(
        UserInfo(
            username="admin",
            name="admin",
            birthdate=datetime(2001, 12, 10),
            role=UserRole.ADMIN,
            password=SecretStr("123456789"),
        )
    )
    app.state.user_service = user_service
    return TestClient(app)


def test_correct_register_user(test_client):
    response = test_client.post(
        "/user-register",
        json={
            "username": "Vadik",
            "name": "Vadim",
            "birthdate": "2000-10-10",
            "password": "123456789",
        },
    )
    print(response.json())
    assert response.status_code == HTTPStatus.OK

    response_data = response.json()

    

def test_error_username_register(test_client):
    test_client.post(
        "/user-register",
        json = {
            "username": "test_user",
            "name": "Test User",
            "birthdate": "2000-01-01",
            "role": "USER",
            "password": "123456789"
        },
    )
    
    response = test_client.post(
        "/user-register",
        json = {
            "username": "test_user",
            "name": "Test User New",
            "birthdate": "2000-01-01",
            "role": "USER",
            "password": "1234567899"
        },
    )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    
def test_error_password_register(test_client):
    response = test_client.post(
        "/user-register",
        json = {
            "username": "test_user",
            "name": "Test User",
            "birthdate": "2000-01-01",
            "role": "USER",
            "password": "1234567"
        },
    )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    
def test_user_get_by_id_admin(test_client):
    response = test_client.post(
        "/user-get",
        params = {"id": 1},
        auth = ("admin", "123456789")
    )
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    
    assert data["uid"] == 1
    assert data['username'] == "admin"
    assert data['name'] == "admin"
    assert data['birthdate'] == "2001-12-10T00:00:00"
    assert data['role'] == "admin"

def test_error_params_user_get(test_client):
    response = test_client.post(
        "/user-get",
        params = {"id": 10, "username": "test_user"},
        auth = ("admin", "123456789")
    )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    
def test_error_none_params_user_get(test_client):
    response = test_client.post(
        "/user-get",
        params = {},
        auth = ("admin", "123456789")
    )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_error_get_by_id(test_client):
    response = test_client.post(
        "/user-get",
        params = {"id": 1},
        auth = ("admin", "1234456789")
    )
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    
def test_user_get_by_username_admin(test_client):
    response = test_client.post(
        "/user-get",
        params = {"username": "admin"},
        auth = ("admin", "123456789")
    )
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['uid'] == 1
    assert data['username'] == "admin"
    assert data['name'] == "admin"
    assert data['birthdate'] == "2001-12-10T00:00:00"
    assert data['role'] == "admin"

def test_error_get_by_username(test_client):
    response = test_client.post(
        "/user-get",
        params = {"username": "test_user_52"},
        auth = ("admin", "123456789")
    )
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_user_promote(test_client):
    response = test_client.post(
        "/user-promote",
        params = {"id": 1},
        auth = ("admin", "123456789")
    )
    
    assert response.status_code == HTTPStatus.OK
    
def test_error_id_user_promote(test_client):
    response = test_client.post(
        "/user-promote",
        params = {"id": 52},
        auth = ("admin", "123456789")
    )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    
def test_fail_403_promote_user_without_admin(test_client):
    test_client.post(
        "/user-register",
        json={
            "username": "test_user",
            "name": "Joe",
            "birthdate": "2000-05-20",
            "password": "123456789",
        },
    )

    response = test_client.post(
        "/user-promote",
        params={"id": 1},
        auth=("test_user", "123456789"),
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    
@pytest.mark.asyncio
async def test_initialize():
    app = create_app()
    async with initialize(app):
        user_service = app.state.user_service
        admin = user_service.get_by_username("admin")
        
        assert admin.uid == 1
        assert admin.info.username == "admin"
        assert admin.info.name == "admin"
        assert admin.info.birthdate == datetime.fromtimestamp(0.0)
        assert admin.info.role == UserRole.ADMIN
        assert admin.info.password == SecretStr("superSecretAdminPassword123")