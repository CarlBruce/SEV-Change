# GitHub Release Checklist

## Blocking issues

- [x] Reconcile 30,042 source DisasterM3 records with the 29,024 paired-image release count; see `EXCLUSIONS.md`.
- [ ] Verify that each `raw` + `t1`–`t7` group is semantically equivalent through a documented human audit.
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
- [ ] Add `CITATION.cff` after bibliographic metadata is final.
- [ ] Add changelog and semantic version tag (for example, `v1.0.0`).
- [x] Preserve the 11 JSON files inside a SHA-256-verified ZIP, uploaded as seven numbered repository parts due large-file API timeouts.

## Reproducibility

- [ ] Run `python scripts/validate_dataset.py --write-manifest` on the final files.
- [ ] Confirm all SHA-256 hashes in `manifest.json` after the final edit.
- [ ] Publish the answer-normalization and evaluation scripts.
- [ ] Publish the exact model inference configurations used in the paper.
- [ ] Document how users obtain and align the upstream image datasets.

## Privacy and cleanup

- [ ] Search all files for local absolute paths, API keys, tokens, usernames, and private URLs.
- [ ] Confirm that no model output logs or unpublished credentials are included.
- [ ] Inspect a clean clone/archive before creating the public GitHub release.
