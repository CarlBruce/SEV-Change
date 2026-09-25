# GitHub Release Checklist

## Blocking issues

- [x] Reconcile 30,042 source DisasterM3 records with the 29,024 paired-image release count; see `EXCLUSIONS.md`.
- [x] Document the author's 1,400-pair stratified review, original statistics, and 42 changed final decisions in `AUDIT_STATUS.md`.
- [x] Record final equivalent decisions for the 42 originally negative pairs in the author's working workbook; synchronize the six revised DisasterM3 strings in the candidate archive.
- [ ] Document per-pair adjudication reasons for the 42 changed decisions and publish an appropriately shareable audit trail.
- [ ] Rerun affected model results on the revised data before claiming a frozen equivalence benchmark.
- [ ] Freeze and publish the exact transformation rules, prompts, model/version, decoding parameters, and rule version.
- [x] Record publicly stated source terms and links in `LICENSE_STATUS.md`.
- [x] Obtain uploader confirmation of redistribution rights for DisasterM3-derived fields (2026-09-23; not independent legal verification).
- [ ] Select an explicit downstream license for the derivative annotations.
- [ ] Add verified paper/preprint citation metadata; do not invent authors, DOI, or venue.
- [ ] Audit the repeated RSRCC raw-task identity retained as `test_003550` and `test_009075`.

## Repository metadata

- [x] Set the planned repository name and local candidate version in `RELEASE_METADATA.md`.
- [x] Create the repository and confirm its public URL (`https://github.com/CarlBruce/SEV-Change`).
- [ ] Add repository description, topics, and maintainer contact.
- [x] Provide an issue template for record-level correction reports.
- [ ] Add `CITATION.cff` after bibliographic metadata is final.
- [ ] Add changelog and semantic version tag (for example, `v1.0.0`).
- [x] Preserve the 11 JSON files inside a SHA-256-verified ZIP, distributed as numbered repository parts due large-file API timeouts.
- [x] Add `scripts/verify_release_archive.py` and CI to validate the public split archive against `manifest.json`.
- [ ] Deposit the frozen complete dataset in a formal long-term data repository and verify its persistent identifier.

## Reproducibility

- [x] Verify the current public ZIP parts and all 11 data files against the candidate manifest.
- [ ] Run `python scripts/validate_dataset.py --root extracted` on the final frozen files and update the manifest if the data change.
- [ ] Confirm all SHA-256 hashes in `manifest.json` after the final edit.
- [ ] Publish the answer-normalization and evaluation scripts.
- [ ] Publish the exact model inference configurations used in the paper.
- [ ] Publish per-sample predictions and the common sample-ID lists used for every reported result.
- [ ] Publish the original generation prompts/rules and source-specific answer parsers and aggregation code.
- [ ] Document how users obtain and align the upstream image datasets.

## Privacy and cleanup

- [ ] Search all files for local absolute paths, API keys, tokens, usernames, and private URLs.
- [ ] Confirm that no model output logs or unpublished credentials are included.
- [ ] Inspect a clean clone/archive before creating the public GitHub release.
