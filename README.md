# SEV-Change

SEV-Change is a paired-question benchmark for evaluating semantic invariance in remote-sensing change visual question answering. Each task-level record contains one original question (`raw`) and seven controlled variants (`t1`–`t7`) while preserving the associated bitemporal image paths, answer space, and ground-truth answer.

[中文说明](README_zh-CN.md)

> Release status: **public candidate, not a final benchmark release**. The data files are organized and machine-validated. An explicit reuse license, permanent citation, transformation-rule specification, and human semantic-equivalence audit remain outstanding.

Repository: [CarlBruce/SEV-Change](https://github.com/CarlBruce/SEV-Change). Candidate version: `v0.1.0-rc1`. No dataset DOI or GitHub release tag has been minted. See `RELEASE_METADATA.md` for publication status.

## Download the complete data package

The original 11 JSON files are preserved inside one ZIP, distributed as seven numbered parts under `release/` because this upload route timed out on large individual files. Download all seven parts and `release/parts.json`, then run:

```bash
python scripts/archive_parts.py assemble release/parts.json SEV-Change-v0.1.0-rc1-git.zip
```

The script verifies each part and the assembled ZIP against SHA-256 hashes in `release/parts.json`. Extract the ZIP to access `data/rsrcc/` and `data/disasterm3/`. The ZIP's `manifest.json` records the pre-upload freeze state; this repository's `RELEASE_METADATA.md` records current publication status. No images or masks are included.

## Contents inside the assembled ZIP

```text
SEV-Change/
├── data/
│   ├── rsrcc/
│   │   └── rsrcc_test_variants.json
│   └── disasterm3/
│       └── DisasterM3_<category>_variants.json  # 10 categories
├── scripts/
│   └── validate_dataset.py
├── DATASET_CARD.md
├── DATA_DICTIONARY.md
├── EXCLUSIONS.md
├── LICENSE_STATUS.md
├── RELEASE_METADATA.md
├── SOURCES.md
├── RELEASE_CHECKLIST.md
├── manifest.json
└── README.md
```

The current files contain:

| Source subset | Files | Task-level records | Question expressions |
|---|---:|---:|---:|
| RSRCC test | 1 | 21,999 | 175,992 |
| DisasterM3 (10 categories) | 10 | 29,024 | 232,192 |
| Total | 11 | 51,023 | 408,184 |

These counts are derived directly from the packaged JSON files. They supersede the stale local `DisasterM3/index.json`, which described only an early three-sample landslide run and is intentionally excluded. The source variant files also contained 1,018 single-image relational-reasoning records; they are outside the paired-image benchmark definition and are documented in `EXCLUSIONS.md`.

## Data format

All data files are UTF-8 JSON arrays. Every record contains:

- `pre_image_path`, `post_image_path`: paths expected relative to the corresponding upstream image dataset;
- `ground_truth`: answer, count, class, or target-mask metadata, depending on the task;
- `variants`: an object with exactly eight string fields in order: `raw`, `t1`, ..., `t7`.

RSRCC records additionally contain stable IDs, split, answer-type, candidate-option, and source-text metadata. DisasterM3 records additionally contain task, event, category, and original-index metadata; candidate-option fields exist only for applicable VQA tasks, while segmentation records use mask paths as ground truth. Images and masks are **not** included in this package.

The annotations are derived from [RSRCC](https://huggingface.co/datasets/google/RSRCC) and [DisasterM3](https://github.com/Junjue-Wang/DisasterM3). Cite the relevant original datasets when using either subset; source links and verified citation details are collected in `SOURCES.md`.

## Validation

No third-party Python package is required:

```bash
python scripts/validate_dataset.py --write-manifest
```

The validator checks JSON structure, required fields, variant completeness/order, empty text, raw/source alignment, duplicate logical records, file size, and SHA-256 hashes. `manifest.json` is generated from the actual files rather than manually maintained counts.

One RSRCC raw-task identity occurs twice (`test_003550` and `test_009075`). The two records have different generated variants and are retained pending an upstream-source audit; the validator reports this as a warning rather than silently deleting either record.

## Before final release

Do not present this candidate as a final audited benchmark until the items in `RELEASE_CHECKLIST.md` are resolved. The 29,024 DisasterM3 count is obtained by the documented paired-image eligibility rule in `EXCLUSIONS.md`.

## Citation

Citation metadata has not yet been finalized. Add a verified paper citation and `CITATION.cff` only after the title, authors, venue/preprint identifier, and release version are frozen.
