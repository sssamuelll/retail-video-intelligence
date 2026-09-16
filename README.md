# Retail Video Intelligence

Scaffold mínimo para un MVP **on-premise** de analítica de CCTV orientada a retail. El repositorio no contiene un NVR, modelos, pesos ni procesamiento de vídeo real: define los límites, el dominio y una ruta de integración verificable sin red, GPU ni descargas.

## Alcance del MVP

Flujo previsto:

1. **Frigate + go2rtc (externos)** reciben cámaras y administran grabaciones/streams.
2. Este servicio importa referencias a grabaciones y normaliza eventos.
3. **RF-DETR exportado a ONNX/OpenVINO** será el detector (adaptador pendiente).
4. Un tracker efímero asociará detecciones solo durante una sesión corta.
5. **SigLIP 2** generará embeddings para búsqueda semántica (adaptador pendiente).
6. PostgreSQL + pgvector almacenará eventos y embeddings.

Este scaffold implementa únicamente configuración, modelos de dominio y una CLI de smoke test. No afirma que detección, tracking, embeddings ni conexión con Frigate estén implementados.

## Guardrails obligatorios

El MVP **prohíbe**:

- reconocimiento o identificación facial;
- inferencia de emociones o estados sensibles;
- lectura automática de matrículas;
- reidentificación persistente de personas entre cámaras o sesiones.

El tracking será efímero y sus identificadores no tendrán significado fuera de la sesión de procesamiento. Véase [ADR-0001](docs/adr/0001-licencias-privacidad.md).

## Inicio rápido (sin red, GPU ni modelos)

Requiere Python 3.11+.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
rvi smoke
python -m unittest discover -s tests -v
```

Alternativa sin instalar el paquete:

```bash
PYTHONPATH=src python -m retail_video_intelligence smoke
PYTHONPATH=src python -m unittest discover -s tests -v
```

El smoke test valida configuración y guardrails; no abre conexiones ni descarga artefactos.

## PostgreSQL + pgvector

```bash
cp .env.example .env
# Cambiar las credenciales antes de un entorno compartido.
docker compose up -d postgres
```

El compose inicia solamente PostgreSQL con pgvector. No incluye Frigate, go2rtc ni este servicio. Para la integración prevista, Frigate debe permanecer desplegado y gestionado externamente; este servicio consumirá referencias a grabaciones/eventos mediante un adaptador explícito, con acceso mínimo y sin copiar su código.

## Desarrollo

```bash
make smoke
make test
make lint
```

`make lint` usa `ruff` si está instalado y siempre valida que los módulos compilen. La arquitectura y las decisiones abiertas están en [`docs/architecture.md`](docs/architecture.md).

## Licencia

**Pendiente de decisión.** Este repositorio no concede todavía una licencia de uso o redistribución; consulte [`LICENSE`](LICENSE) y el ADR antes de incorporar dependencias/modelos.
