import re


class PrivacyFilter:
    """Redacts PII from text using regex patterns."""

    # Patterns for common PII
    EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    PHONE_PATTERN = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    SSN_PATTERN = r"\b\d{3}-\d{2}-\d{4}\b"

    @classmethod
    def redact_pii(cls, text: str) -> str:
        """Replace all PII with [REDACTED]."""
        text = re.sub(cls.EMAIL_PATTERN, "[REDACTED]", text)
        text = re.sub(cls.PHONE_PATTERN, "[REDACTED]", text)
        text = re.sub(cls.SSN_PATTERN, "[REDACTED]", text)
        return text
