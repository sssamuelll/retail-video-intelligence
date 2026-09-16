# ADR-0001: licencias y límites de privacidad

- Estado: aceptado para el scaffold; selección de licencia pendiente
- Fecha: 2026-09-16

## Contexto

La analítica de CCTV puede producir datos personales o facilitar vigilancia desproporcionada. Además, el código, los modelos y sus pesos pueden tener licencias distintas. Elegir una licencia del repositorio antes de revisar esas obligaciones puede crear incompatibilidades.

## Decisión

1. Mantener la licencia del repositorio como **pendiente** hasta revisar dependencias, modelos, pesos y datasets.
2. No incluir pesos, datasets ni código de Frigate/go2rtc.
3. Prohibir en el MVP reconocimiento facial, inferencia de emociones, lectura de matrículas y reidentificación persistente.
4. Usar únicamente tracking efímero: identificadores aleatorios por sesión, sin tabla de correspondencia duradera ni comparación entre cámaras/sesiones.
5. Diseñar retención mínima y configurable; no registrar imágenes o secretos en logs.
6. Requerir revisión humana de finalidad, base legal, señalización, acceso y plazo de conservación antes de un piloto real.

## Consecuencias

- Algunas consultas o métricas quedan deliberadamente fuera de alcance.
- Cualquier cambio de guardrails exige un ADR nuevo y revisión legal/privacidad; no es un simple cambio técnico.
- La distribución pública queda bloqueada hasta seleccionar una licencia.
- Los adaptadores de modelos deberán verificar licencias y hashes de artefactos locales, sin descarga automática.
