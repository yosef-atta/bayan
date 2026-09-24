import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.types import Event, Hint

from app.core.config import settings

SENSITIVE_HEADERS = {"authorization", "cookie", "x-api-key", "x-session-token"}


def scrub_sensitive_data(event: Event, hint: Hint) -> Event | None:
    """Scrubs sensitive headers, cookies, and tokens from Sentry error reports."""
    if "request" in event:
        request_info = event["request"]
        if "headers" in request_info and isinstance(request_info["headers"], dict):
            for header in list(request_info["headers"].keys()):
                if header.lower() in SENSITIVE_HEADERS:
                    request_info["headers"][header] = "[REDACTED]"
        if "cookies" in request_info:
            request_info["cookies"] = "[REDACTED]"

    return event


def init_sentry() -> None:
    """Initializes Sentry SDK if SENTRY_DSN is configured."""
    if not settings.SENTRY_DSN:
        return

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.SENTRY_ENVIRONMENT or settings.ENVIRONMENT,
        traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
        send_default_pii=False,
        before_send=scrub_sensitive_data,
        integrations=[
            StarletteIntegration(transaction_style="endpoint"),
            FastApiIntegration(transaction_style="endpoint"),
        ],
    )
