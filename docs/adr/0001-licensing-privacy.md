# ADR-0001: Licensing and Privacy Boundaries

- Status: accepted for the scaffold; license selection pending
- Date: 2026-09-16

## Context

CCTV analytics can produce personal data or enable disproportionate surveillance. In addition, the code, models, and their weights may have different licenses. Choosing a repository license before reviewing those obligations could create incompatibilities.

## Decision

1. Keep the repository license **pending** until dependencies, models, weights, and datasets have been reviewed.
2. Do not include weights, datasets, or Frigate/go2rtc code.
3. Prohibit facial recognition, emotion inference, license plate recognition, and persistent re-identification in the MVP.
4. Use ephemeral tracking only: random per-session identifiers, with no durable mapping table or comparison across cameras/sessions.
5. Design minimal, configurable retention; do not log images or secrets.
6. Require human review of purpose, legal basis, signage, access, and retention period before a real-world pilot.

## Consequences

- Some queries or metrics are deliberately out of scope.
- Any guardrail change requires a new ADR and legal/privacy review; it is not merely a technical change.
- Public distribution remains blocked until a license is selected.
- Model adapters must verify licenses and hashes of local artifacts, without automatic downloads.
