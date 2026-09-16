"""Domain models without infrastructure dependencies."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4


class EventKind(StrEnum):
    OBJECT_DETECTED = "object_detected"
    ZONE_ENTERED = "zone_entered"
    ZONE_EXITED = "zone_exited"


@dataclass(frozen=True, slots=True)
class RecordingRef:
    camera_id: str
    source_uri: str
    starts_at: datetime
    ends_at: datetime

    def __post_init__(self) -> None:
        if not self.camera_id.strip():
            raise ValueError("camera_id cannot be empty")
        if self.starts_at.tzinfo is None or self.ends_at.tzinfo is None:
            raise ValueError("timestamps must include a time zone")
        if self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be later than starts_at")


@dataclass(frozen=True, slots=True)
class BoundingBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def __post_init__(self) -> None:
        values = (self.x_min, self.y_min, self.x_max, self.y_max)
        if not all(0.0 <= value <= 1.0 for value in values):
            raise ValueError("coordinates must be normalized between 0 and 1")
        if self.x_min >= self.x_max or self.y_min >= self.y_max:
            raise ValueError("invalid bounding box")


@dataclass(frozen=True, slots=True)
class Detection:
    label: str
    confidence: float
    box: BoundingBox
    ephemeral_track_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("label cannot be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class NormalizedEvent:
    camera_id: str
    occurred_at: datetime
    kind: EventKind
    source_event_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    event_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not self.camera_id.strip():
            raise ValueError("camera_id cannot be empty")
        if self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at must include a time zone")

    @classmethod
    def now(cls, camera_id: str, kind: EventKind) -> "NormalizedEvent":
        return cls(camera_id=camera_id, occurred_at=datetime.now(UTC), kind=kind)
