import logging
import re
import sys

# Patterns to identify and scrub sensitive parameters/values from log records
SENSITIVE_PATTERNS = [
    re.compile(
        r"(password|passwd|api_key|apikey|secret|token|session|auth|authorization|verification_code|code)[\"']?\s*[:=]\s*[\"']?([^\"'\s,]+)",
        re.IGNORECASE,
    ),
    re.compile(r"(Bearer\s+)[A-Za-z0-9\-_.]+", re.IGNORECASE),
    re.compile(r"(gsk_[A-Za-z0-9]{20,})", re.IGNORECASE),  # Groq API key pattern
]


def sanitize_message(msg: str) -> str:
    for pattern in SENSITIVE_PATTERNS:
        msg = pattern.sub(r"\1: [REDACTED]", msg)
    return msg


class SensitiveDataFormatter(logging.Formatter):
    """Formats log records and ensures sensitive strings in messages are scrubbed."""

    def format(self, record: logging.LogRecord) -> str:
        if isinstance(record.msg, str):
            record.msg = sanitize_message(record.msg)
        return super().format(record)


_old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs) -> logging.LogRecord:
    record = _old_factory(*args, **kwargs)
    if isinstance(record.msg, str):
        record.msg = sanitize_message(record.msg)
    return record


def setup_logging(log_level: str = "INFO") -> None:
    """Configures root application logging with formatting and sensitive data filtering."""
    logging.setLogRecordFactory(record_factory)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level.upper())

    if not root_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = SensitiveDataFormatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
