"""CLI local que no abre red ni inicializa aceleradores."""

import argparse
import json
from collections.abc import Sequence

from .config import Settings
from .domain import EventKind, NormalizedEvent
from .policy import PROHIBITED_CAPABILITIES


def smoke() -> dict[str, object]:
    settings = Settings.from_env()
    event = NormalizedEvent.now("smoke-camera", EventKind.OBJECT_DETECTED)
    return {
        "status": "ok",
        "camera_id": event.camera_id,
        "retention_days": settings.retention_days,
        "guardrails": sorted(PROHIBITED_CAPABILITIES),
        "network_used": False,
        "models_loaded": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rvi")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("smoke", help="valida configuración y políticas localmente")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "smoke":
        print(json.dumps(smoke(), ensure_ascii=False, sort_keys=True))
        return 0
    return 2
