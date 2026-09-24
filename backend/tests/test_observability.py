import logging
from typing import cast

from sentry_sdk.types import Event, Hint

from app.core.logging import setup_logging
from app.core.sentry import init_sentry, scrub_sensitive_data


def test_log_sanitization(caplog):
    setup_logging("DEBUG")
    logger = logging.getLogger("test_logger")

    with caplog.at_level(logging.INFO):
        logger.info("User login attempt with password=super_secret_password123")
        logger.info("Calling Groq with api_key=gsk_1234567890abcdef1234567890")
        logger.info("Authorization header: Bearer my_secret_token_value")
        logger.info("Verification code: verification_code=123456")

    output = caplog.text
    assert "super_secret_password123" not in output
    assert "gsk_1234567890abcdef1234567890" not in output
    assert "my_secret_token_value" not in output
    assert "123456" not in output
    assert "[REDACTED]" in output


def test_sentry_scrub_sensitive_data():
    raw_event = {
        "request": {
            "headers": {
                "authorization": "Bearer secret_bearer_token",
                "cookie": "session_id=opaque_token_123",
                "x-api-key": "secret_key",
                "content-type": "application/json",
            },
            "cookies": {"session_id": "opaque_token_123"},
        }
    }
    event = cast(Event, raw_event)
    hint = cast(Hint, {})
    scrubbed = scrub_sensitive_data(event, hint)
    assert scrubbed is not None
    request_dict = scrubbed.get("request")
    assert isinstance(request_dict, dict)
    headers = request_dict.get("headers")
    assert isinstance(headers, dict)
    assert headers["authorization"] == "[REDACTED]"
    assert headers["cookie"] == "[REDACTED]"
    assert headers["x-api-key"] == "[REDACTED]"
    assert headers["content-type"] == "application/json"
    assert request_dict.get("cookies") == "[REDACTED]"


def test_sentry_init_without_dsn():
    # Should complete without error when SENTRY_DSN is None/empty
    init_sentry()
