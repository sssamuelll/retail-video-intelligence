# Retail Video Intelligence

A minimal scaffold for an **on-premises** retail CCTV analytics MVP. The repository contains no NVR, models, weights, or actual video processing: it defines boundaries, the domain model, and a verifiable integration path that requires no network, GPU, or downloads.

## MVP scope

Planned flow:

1. **Frigate + go2rtc (external)** receive camera feeds and manage recordings/streams.
2. This service imports recording references and normalizes events.
3. **RF-DETR exported to ONNX/OpenVINO** will be the detector (adapter pending).
4. An ephemeral tracker will associate detections only during a short session.
5. **SigLIP 2** will generate embeddings for semantic search (adapter pending).
6. PostgreSQL + pgvector will store events and embeddings.

This scaffold implements only configuration, domain models, and a smoke-test CLI. It does not claim that detection, tracking, embeddings, or a Frigate connection are implemented.

## Mandatory guardrails

The MVP **prohibits**:

- facial recognition or identification;
- inference of emotions or sensitive states;
- automatic license plate recognition;
- persistent re-identification of people across cameras or sessions.

Tracking will be ephemeral, and its identifiers will have no meaning outside the processing session. See [ADR-0001](docs/adr/0001-licensing-privacy.md).

## Quick start (no network, GPU, or models)

Requires Python 3.11+.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
rvi smoke
python -m unittest discover -s tests -v
```

Alternatively, without installing the package:

```bash
PYTHONPATH=src python -m retail_video_intelligence smoke
PYTHONPATH=src python -m unittest discover -s tests -v
```

The smoke test validates configuration and guardrails; it opens no connections and downloads no artifacts.

## PostgreSQL + pgvector

```bash
cp .env.example .env
# Change the credentials before using a shared environment.
docker compose up -d postgres
```

The Compose configuration starts only PostgreSQL with pgvector. It does not include Frigate, go2rtc, or this service. For the planned integration, Frigate must remain deployed and managed externally; this service will consume recording/event references through an explicit adapter, with minimal access and without copying its code.

## Development

```bash
make smoke
make test
make lint
```

`make lint` uses `ruff` when installed and always validates that the modules compile. The architecture and open decisions are documented in [`docs/architecture.md`](docs/architecture.md).

## License

**Pending a decision.** This repository does not yet grant a license to use or redistribute the software; consult [`LICENSE`](LICENSE) and the ADR before adding dependencies or models.
