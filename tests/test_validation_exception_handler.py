"""Tests for the global validation exception handler."""
import json
import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from fastapi.exceptions import RequestValidationError
from app.exception_handlers import validation_exception_handler

mockErrorsWithMultiTypesMissing = [{'type': 'missing', 'loc': ('body', 'first_name'), 'msg': 'Field required', 'input': {'email': 'tassio@hotmail', 'password': 'SecurePass!12', 'password_confirmation': 'SecurePass!12'}, 'url': 'https://errors.pydantic.dev/2.5/v/missing'}, {'type': 'missing', 'loc': ('body', 'last_name'), 'msg': 'Field required', 'input': {'email': 'tassio@hotmail', 'password': 'SecurePass!12', 'password_confirmation': 'SecurePass!12'}, 'url': 'https://errors.pydantic.dev/2.5/v/missing'}, {'type': 'value_error', 'loc': ('body', 'email'), 'msg': 'value is not a valid email address: The part after the @-sign is not valid. It should have a period.', 'input': 'tassio@hotmail', 'ctx': {'reason': 'The part after the @-sign is not valid. It should have a period.'}}]
mockErrorWithCustomValueError = [{'type': 'missing', 'loc': ('body', 'last_name'), 'msg': 'Field required', 'input': {'email': 'tassio123@hotmail.com', 'password': 'Secur', 'password_confirmation': 'Secur', 'first_name': 'tas'}, 'url': 'https://errors.pydantic.dev/2.5/v/missing'}, {'type': 'value_error', 'loc': ('body', 'password'), 'msg': "Value error, ('WEAK_PASSWORD', 'Password must be at least 8 characters long')", 'input': 'Secur', 'ctx': {'error': ValueError('WEAK_PASSWORD', 'Password must be at least 8 characters long')}, 'url': 'https://errors.pydantic.dev/2.5/v/value_error'}]



class TestValidationExceptionHandler:
    """Tests that Pydantic validation errors are handled consistently."""

    def test_weak_password_uses_custom_error_format(
        self,
        client: TestClient,
        weak_password_data: dict,
    ):
        """Weak passwords should return 400 with our custom error structure."""
        # Add required fields that are not part of the shared fixture
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            **weak_password_data,
        }

        response = client.post("/api/v1/auth/register", json=payload)

        assert response.status_code == 400
        data = response.json()

        assert data["success"] is False
        assert "error" in data
        assert isinstance(data["error"], list)
        assert len(data["error"]) >= 1

        first_error = data["error"][0]
        assert "code" in first_error
        # For weak passwords coming from the password validator we expect
        # the custom WEAK_PASSWORD error code.
        assert first_error["code"] == "WEAK_PASSWORD"

        assert "timestamp" in data
        assert data["timestamp"].endswith("Z")

    def test_missing_required_field_returns_missing_field_error(
        self,
        client: TestClient,
        valid_user_data: dict,
    ):
        """Omitting a required field should be surfaced via our handler."""
        # Remove a required field from an otherwise valid payload
        payload = {
            "last_name": "Doe",
            "email": valid_user_data["email"],
            "password": valid_user_data["password"],
            "password_confirmation": valid_user_data["password_confirmation"],
        }

        response = client.post("/api/v1/auth/register", json=payload)

        assert response.status_code == 400
        data = response.json()

        assert data["success"] is False
        assert isinstance(data["error"], list)
        assert len(data["error"]) >= 1

        # We don't assert the exact structure of every item, but we do
        # ensure that at least one error entry contains a code.
        assert any("code" in e for e in data["error"])

    @pytest.mark.asyncio
    async def test_multi_errors_types(self):
        exc = RequestValidationError(errors=mockErrorsWithMultiTypesMissing)

        request = Request(scope={"type": "http"})

        response = await validation_exception_handler(request, exc)

        data = json.loads(response.body)

        assert data["success"] is False
        assert len(data["error"]) == 3
        assert data["error"][0] ==  {
                "msg": "first_name is required",
                "code": "MISSING_FIELD",
                "field": "first_name",
            }
        assert data["error"][1] == {
                "msg": "last_name is required",
                "code": "MISSING_FIELD",
                "field": "last_name"
            }
        assert data["error"][2] == {
                "field": "email",
                "msg": "value is not a valid email address: The part after the @-sign is not valid. It should have a period.",
                "code": "VALIDATION_ERROR"
            }

    @pytest.mark.asyncio
    async def test_multi_errors_types_with_value_error_instance(self):
        exc = RequestValidationError(errors=mockErrorWithCustomValueError)

        request = Request(scope={"type": "http"})

        response = await validation_exception_handler(request, exc)

        data = json.loads(response.body)

        assert data["success"] is False
        assert len(data["error"]) == 2
        assert data["error"][0] ==  {
            "msg": "last_name is required",
            "code": "MISSING_FIELD",
            "field": "last_name"
        }
        assert data["error"][1] == {
            "msg": "Password must be at least 8 characters long",
            "code": "WEAK_PASSWORD"
        }


