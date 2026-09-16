# MVP Architecture

## Context and boundaries

The system will run on-premises. **Frigate/go2rtc is an external dependency**, not a component copied, embedded, or deployed by this repository. It is responsible for ingesting camera feeds, maintaining streams and recordings, and publishing events/references. Operational configuration for cameras and credentials remains outside this codebase.

## Planned flow

```text
Cameras -> external Frigate/go2rtc -> recording/event reference
                                         |
                                         v
                              custom importer/normalizer
                                         |
                       +-----------------+------------------+
                       |                                    |
             RF-DETR (ONNX/OpenVINO)              normalized metadata
                       |
               ephemeral tracking
                       |
               permitted crops -> SigLIP 2 -> pgvector/PostgreSQL
```

The inference blocks are **planned, not implemented**. No weights are downloaded, and the future contract must accept local paths to reviewed artifacts.

## Components

- `domain.py`: provider-independent events, detections, and recording references.
- `config.py`: configuration from environment variables, without making connections.
- `cli.py`: local smoke test for configuration and policies.
- PostgreSQL/pgvector: the only Compose service, for future persistence.
- Frigate adapter (pending): will import references and normalize timestamps/cameras/types; it will not assume direct camera access.
- RF-DETR/SigLIP 2 adapters (pending): local inference with pinned, audited artifacts and no implicit downloads.
- Tracker (pending): memory limited to one session, with no persistent identity.

## Data principles

- Minimization: persist only strictly necessary events and embeddings.
- Configurable retention; automatic deletion is pending implementation.
- Keep camera/event identifiers separate from human identities.
- Do not store biometric data or build profiles of people.
- Logs must contain no frames, credentials, or signed URLs.

## Existing-solutions preflight

A lightweight evaluation based on documentation and ecosystem knowledge, without installing services:

- **Frigate/go2rtc**: a maintained solution specialized in ingestion/NVR; reuse it externally instead of rebuilding RTSP, recording, and restreaming.
- **ONNX Runtime/OpenVINO**: mature backends for local inference; validate the specific choice against target hardware and the RF-DETR export.
- **PostgreSQL/pgvector**: avoids introducing a separate vector database in the MVP and supports transactional filters alongside embeddings.
- **Existing trackers** (ByteTrack/OC-SORT): candidates for evaluation; none is selected or integrated yet, preserving minimal, ephemeral tracking.

## Pending decisions

1. Repository license and license/weight compatibility for RF-DETR and SigLIP 2.
2. Exact model versions/exports, embedding dimensions, and hardware-specific backend.
3. Frigate import contract (API, webhook, or controlled filesystem).
4. SQL schema/migrations, retention policies, and verifiable deletion.
5. Tracker, thresholds, and metrics using representative, authorized data.
6. Authentication, encryption, observability, and backup operations.
