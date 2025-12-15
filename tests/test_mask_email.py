"""Unit tests for the mask_email utility."""

from app.utils.mask_email import mask_email


class TestMaskEmail:
    """Tests for email masking behavior."""

    def test_mask_email_long_local_part(self):
        """Local part longer than 3 chars should be partially masked."""
        email = "john.doe@example.com"
        result = mask_email(email)

        # "john.doe" -> "joh*****"
        assert result == "joh*****@example.com"

    def test_mask_email_short_local_part(self):
        """Local part with 3 chars or less should show 1 letter instead."""
        email = "abc@domain.com"
        result = mask_email(email)

        assert result == "a**@domain.com"

    def test_mask_email_preserves_domain(self):
        """Domain part should remain unchanged."""
        email = "tester@example.co.uk"
        result = mask_email(email)

        # Local "tester" -> "tes***"
        assert result == "tes***@example.co.uk"


