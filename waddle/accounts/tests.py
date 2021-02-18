import json
import pytest
from graphene_django.utils.testing import graphql_query
from graphql_jwt.exceptions import PermissionDenied

from django.contrib.auth import get_user_model


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)
    return func


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def login_user(db, client_query, create_user):
    def make_login(user=None):
        if user is None:
            user = create_user(
                name="Tested Tester",
                email="testeduser@mail.com",
                mobile="+2348100000001",
                password="helloworld"
            )

        query = client_query(
            """
            mutation tokenAuth($email: String!, $password: String!) {
                tokenAuth(email: $email, password: $password) {
                    token
                    payload
                    refreshExpiresIn
                }
            }
            """,
            op_name="tokenAuth",
            variables={
                "email": user.email,
                "password": "helloworld",
            }
        )
        return f"JWT {query.json()['data']['tokenAuth']['token']}"
    return make_login


@pytest.mark.django_db
def test_user_create(client_query):
    query = client_query(
        """
        mutation createUser(
            $email: String!, $mobile: String!, $name: String!, $password: String!
        ) {
            createUser(
                email: $email, mobile: $mobile, name: $name, password: $password
            ) {
                user {
                    id
                    name
                    email
                    mobile
                    password
                }
            }
        }
        """,
        op_name='createUser',
        variables={
            "name": "Tested Tester",
            "email": "testeduser@mail.com",
            "mobile": "+2348100000001",
            "password": "helloword",
        },
    )

    data = query.json()["data"]["createUser"]["user"]

    assert "errors" not in query.json()
    assert data["id"] == str(1)
    assert data["name"] == "Tested Tester"
    assert data["email"] == "testeduser@mail.com"
    assert data["mobile"] == "+2348100000001"
    assert data["password"] != "helloworld"


def test_user_login(client_query, create_user):
    user = create_user(
        name="Test User",
        email="testeduser@mail.com",
        mobile="+2348100000001",
        password="helloworld"
    )

    query = client_query(
        """
        mutation tokenAuth($email: String!, $password: String!) {
            tokenAuth(email: $email, password: $password) {
                token
                payload
                refreshExpiresIn
            }
        }
        """,
        op_name="tokenAuth",
        variables={
            "email": user.email,
            "password": "helloworld",
        }
    )

    data = query.json()["data"]["tokenAuth"]

    assert "errors" not in query.json()
    assert "token" in data
    assert "payload" in data
    assert "refreshExpiresIn" in data


def test_user_profile_authenticated(client_query, login_user):
    token = login_user()

    query = client_query(
        """
        query userProfile {
            userProfile {
                id
                name
                email
                mobile
                password
                created
                modified
                isActive
            }
        }
        """,
        op_name="userProfile",
        headers={
            "HTTP_AUTHORIZATION": token
        }
    )

    data = query.json()["data"]["userProfile"]

    assert "errors" not in query.json()
    assert data["id"] == str(1)
    assert data["name"] == "Tested Tester"
    assert data["email"] == "testeduser@mail.com"
    assert data["mobile"] == "+2348100000001"
    assert data["password"] != "helloworld"


def test_user_profile_unauthenticated(client_query):
    query = client_query(
        """
        query userProfile {
            userProfile {
                id
                name
                email
                mobile
                password
                created
                modified
                isActive
            }
        }
        """,
        op_name="userProfile"
    )

    assert "errors" in query.json()
    assert query.json()["errors"][0]["message"] == \
        "You do not have permission to perform this action"
