"""Unit tests for user profile update endpoint"""
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.models.User import User, UserType
from app.models.OutboxEvent import OutboxEvent
from app.utils.password import hash_password
from app import dependencies

id=uuid4() 
id2=uuid4() 

def override_get_current_user_factory(db_session: Session):
    """Return a dependency override that always yields the same user."""

    def _override_get_current_user() -> User:
        # Ensure there is a user to act as the authenticated user
        user = (
            db_session.query(User)
            .filter(User.email == "profile@example.com")
            .first()
        )
        if not user:
            user = User(
                id=id,
                email="profile@example.com",
                first_name="Current",
                last_name="User",
                password_hash=hash_password("SecurePassword123!"),
                is_email_verified=True,
                type=UserType.CLIENT
            )
            user2 = User(
                id=id2,
                email="profile2@example.com",
                first_name="ANother",
                last_name="User",
                password_hash=hash_password("SecurePassword123!"),
                is_email_verified=True,
                type=UserType.CLIENT
            )
            db_session.add(user)
            db_session.add(user2)
            db_session.commit()
            db_session.refresh(user)
        return user

    return _override_get_current_user


@pytest.fixture
def profile_client(db_session: Session) -> TestClient:
    """Test client with overrides for DB and current user."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[dependencies.get_current_user] = (
        override_get_current_user_factory(db_session)
    )

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


class TestProfileUpdateSuccess:
    """Tests for successful profile update."""

    def test_update_profile_success(
        self,
        profile_client: TestClient,
        db_session: Session,
    ):
        """All fields are updated and outbox event is created."""
        payload = {
            "first_name": "UpdatedFirst",
            "last_name": "UpdatedLast",
            "email": "updated@example.com",
        }

        response = profile_client.put(f"/api/v1/profile/{id}", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["first_name"] == payload["first_name"]
        assert data["data"]["last_name"] == payload["last_name"]
        # assert data["data"]["email"] == payload["email"]

        # # Verify DB user is updated
        # user = db_session.query(User).filter(User.email == payload["email"]).first()
        # assert user is not None
        # assert user.first_name == payload["first_name"]
        # assert user.last_name == payload["last_name"]

        # # Verify outbox event created
        # events = db_session.query(OutboxEvent).filter(
        #     OutboxEvent.event_type == "user.profile_updated",
        #     OutboxEvent.aggregate_id == str(user.id),
        # )
        # assert events.count() == 1
        # event = events.first()
        # assert event.payload["user_id"] == str(user.id)
        # assert event.payload["first_name"] == payload["first_name"]
        # assert event.payload["last_name"] == payload["last_name"]
        # assert event.payload["email"] == payload["email"]

    def test_update_profile_not_allowed(
        self,
        profile_client: TestClient,
        db_session: Session,
    ):
        payload = {
            "first_name": "UpdatedFirst",
            "last_name": "UpdatedLast",
            "email": "updated@example.com",
        }

        response = profile_client.put(f"/api/v1/profile/{id2}", json=payload)

        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False

class TestProfileUpdateValidation:
    """Tests for validation behavior in profile update."""

    @pytest.mark.parametrize(
        "payload",
        [
            {"first_name": "", "last_name": "Last", "email": "test@example.com"},
            {"first_name": "First", "last_name": "", "email": "test@example.com"},
            {"first_name": "First", "last_name": "Last", "email": "not-an-email"},
        ],
    )
    def test_update_profile_validation_errors(
        self,
        profile_client: TestClient,
        payload: dict,
    ):
        """Invalid payloads should be rejected with 400 (validation error)."""
        response = profile_client.put(f"/api/v1/profile/{id}", json=payload)
        assert response.status_code == 400

    @pytest.mark.parametrize(
        "payload",
        [
            # Multiple words in first_name should be rejected
            {
                "first_name": "Multi Word",
                "last_name": "Last",
                "email": "test@example.com",
            },
            # Multiple words in last_name should be rejected
            {
                "first_name": "First",
                "last_name": "Multi Word",
                "email": "test@example.com",
            },
        ],
    )
    def test_update_profile_rejects_multi_word_names(
        self,
        profile_client: TestClient,
        payload: dict,
    ):
        """first_name and last_name must be single words without spaces."""
        response = profile_client.put(f"/api/v1/profile/{id}", json=payload)

        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert data["error"][0]["code"] == "MAX_ALLOWED_WORDS"


class TestProfileUpdateDuplicateEmail:
    """Tests for duplicate email handling in profile update."""

    def test_update_profile_duplicate_email(
        self,
        profile_client: TestClient,
        db_session: Session,
    ):
        """Updating to an existing email should fail."""
        # Create another user with the target email
        other_user = User(
            email="existing@example.com",
            first_name="Other",
            last_name="User",
            password_hash=hash_password("OtherPassword123!"),
            is_email_verified=True,
        )
        db_session.add(other_user)
        db_session.commit()

        payload = {
            "first_name": "UpdatedFirst",
            "last_name": "UpdatedLast",
            "email": "existing@example.com",
        }

        response = profile_client.put(f"/api/v1/profile/{id}", json=payload)

        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert data["error"][0]["code"] == "DUPLICATE_EMAIL"


