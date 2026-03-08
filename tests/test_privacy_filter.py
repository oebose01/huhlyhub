from plugins.feedback.privacy import PrivacyFilter


def test_redact_email():
    """Should replace email addresses with [REDACTED]."""
    text = "Contact me at john.doe@example.com for more info."
    expected = "Contact me at [REDACTED] for more info."
    assert PrivacyFilter.redact_pii(text) == expected


def test_redact_phone():
    """Should replace phone numbers with [REDACTED]."""
    text = "Call me at 555-123-4567 or (555) 123-4567."
    expected = "Call me at [REDACTED] or [REDACTED]."
    assert PrivacyFilter.redact_pii(text) == expected


def test_redact_ssn():
    """Should replace social security numbers with [REDACTED]."""
    text = "My SSN is 123-45-6789."
    expected = "My SSN is [REDACTED]."
    assert PrivacyFilter.redact_pii(text) == expected


def test_redact_multiple():
    """Should redact all PII in a single string."""
    text = "Email: test@test.com, Phone: 123-456-7890, SSN: 987-65-4321"
    expected = "Email: [REDACTED], Phone: [REDACTED], SSN: [REDACTED]"
    assert PrivacyFilter.redact_pii(text) == expected


def test_no_pii_unchanged():
    """Text without PII should remain unchanged."""
    text = "This is a normal sentence with no PII."
    assert PrivacyFilter.redact_pii(text) == text
