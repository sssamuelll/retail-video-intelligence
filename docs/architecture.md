# Arquitectura del MVP

## Contexto y límites

El sistema se ejecutará on-premise. **Frigate/go2rtc es una dependencia externa**, no un componente copiado, embebido ni desplegado por este repositorio. Su responsabilidad es ingerir cámaras, mantener streams y grabaciones y publicar eventos/referencias. La configuración operativa de cámaras y credenciales queda fuera de este código.

## Flujo previsto

```text
Cámaras -> Frigate/go2rtc externo -> referencia a grabación/evento
                                      |
                                      v
                           importador/normalizador propio
                                      |
                    +-----------------+------------------+
                    |                                    |
          RF-DETR (ONNX/OpenVINO)             metadatos normalizados
                    |
            tracking efímero
                    |
            recortes permitidos -> SigLIP 2 -> pgvector/PostgreSQL
```

Los bloques de inferencia son **previstos, no implementados**. No se descargan pesos y el contrato futuro deberá aceptar rutas locales a artefactos revisados.

## Componentes

- `domain.py`: eventos, detecciones y referencias a grabaciones independientes del proveedor.
- `config.py`: configuración desde variables de entorno, sin efectuar conexiones.
- `cli.py`: smoke test local de configuración y políticas.
- PostgreSQL/pgvector: único servicio del compose, para persistencia futura.
- Adaptador Frigate (pendiente): importará referencias y normalizará timestamps/cámaras/tipos; no asumirá acceso directo a cámaras.
- Adaptadores RF-DETR/SigLIP 2 (pendientes): inferencia local, artefactos fijados y auditados, sin descarga implícita.
- Tracker (pendiente): memoria acotada a una sesión, sin identidad persistente.

## Principios de datos

- Minimización: persistir eventos y embeddings estrictamente necesarios.
- Retención configurable; borrado automático pendiente de implementación.
- Separar identificadores de cámara/evento de identidades humanas.
- No almacenar biometría ni construir perfiles de personas.
- Logs sin fotogramas, credenciales ni URLs firmadas.

## Preflight de soluciones existentes

Evaluación ligera basada en documentación/conocimiento del ecosistema, sin instalar servicios:

- **Frigate/go2rtc**: solución mantenida y especializada en ingestión/NVR; se reutiliza externamente en vez de reconstruir RTSP, grabación y restreaming.
- **ONNX Runtime/OpenVINO**: backends maduros para inferencia local; la elección concreta se validará con hardware objetivo y exportación RF-DETR.
- **PostgreSQL/pgvector**: evita introducir una base vectorial separada en el MVP y permite filtros transaccionales junto a embeddings.
- **Trackers existentes** (ByteTrack/OC-SORT): candidatos a evaluar; no se selecciona ni integra uno todavía para mantener el tracking efímero y mínimo.

## Decisiones pendientes

1. Licencia del repositorio y compatibilidad de licencias/pesos de RF-DETR y SigLIP 2.
2. Versión/exportación exacta de modelos, dimensiones de embeddings y backend por hardware.
3. Contrato de importación con Frigate (API, webhook o filesystem controlado).
4. Esquema SQL/migraciones, políticas de retención y borrado verificable.
5. Tracker, umbrales y métricas sobre datos representativos y autorizados.
6. Autenticación, cifrado, observabilidad y operación de backups.
