"""Políticas no negociables del MVP."""

PROHIBITED_CAPABILITIES = frozenset(
    {
        "emotion_inference",
        "facial_recognition",
        "license_plate_recognition",
        "persistent_reidentification",
    }
)


def assert_capability_allowed(capability: str) -> None:
    """Rechaza explícitamente capacidades prohibidas por el ADR de privacidad."""
    if capability.strip().lower() in PROHIBITED_CAPABILITIES:
        raise ValueError(f"capacidad prohibida en el MVP: {capability}")
