"""Non-negotiable MVP policies."""

PROHIBITED_CAPABILITIES = frozenset(
    {
        "emotion_inference",
        "facial_recognition",
        "license_plate_recognition",
        "persistent_reidentification",
    }
)


def assert_capability_allowed(capability: str) -> None:
    """Explicitly reject capabilities prohibited by the privacy ADR."""
    if capability.strip().lower() in PROHIBITED_CAPABILITIES:
        raise ValueError(f"capability prohibited in the MVP: {capability}")
