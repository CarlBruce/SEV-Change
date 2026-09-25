# Changelog

## `v0.1.0-rc2` candidate — 2026-09-25

- Recorded the author-supplied final adjudication of 1,400 sampled pairs as 1,400 equivalent and zero non-equivalent; preserved the earlier 1,358/42 decision history.
- Revised six DisasterM3 question variants to restore the original target category or task. The six revised strings are the only question-text changes relative to `v0.1.0-rc1`; record counts and the RSRCC subset are unchanged.
- Synchronized the candidate archive, SHA-256 manifest, and audit documentation. The earlier split archive remains available as legacy `rc1` parts.
- Corrected the manifest's candidate-status field and recomputed per-source byte totals from the revised files; the verifier now checks those totals.
- Per-pair reasons for the 42 changed decisions are absent from the supplied workbook. The six revised questions belong to segmentation or report tasks outside the reported closed-answer main experiment; no new model predictions or aggregate scores are claimed for this revision.
- Confirmed the six revised task types against the 11,945-record closed-answer evaluation scope and corrected the version-boundary wording; the exact public sample-ID and prediction files are still missing.

## Unreleased candidate documentation update — 2026-09-24

- Added a read-only archive verifier and GitHub Actions check for the seven ZIP parts, 11 JSON files, record counts and SHA-256 manifest.
- Clarified how to extract the archive before running the structural validator.
- Documented the author's 1,400-pair review and the 42 original negative labels now pending re-adjudication, without changing any data file or model result.
- Added task-level data dictionary detail, evaluation-scope limits, and a Scientific Data readiness/gap assessment.
- Updated the repository-root candidate status; the existing `v0.1.0-rc1` ZIP remains byte-for-byte unchanged and contains older documentation.

This entry is not a new dataset version or a final release announcement. A frozen replacement archive, tag, DOI and license have not yet been issued.
