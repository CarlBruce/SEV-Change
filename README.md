# SEV-Change

SEV-Change is a paired-question benchmark for evaluating semantic invariance in remote-sensing change visual question answering. Each task-level record contains one original question (`raw`) and seven controlled variants (`t1`–`t7`) while preserving the associated bitemporal image paths, answer space, and ground-truth answer.

[中文说明](README_zh-CN.md)

> Release status: **candidate, not a final benchmark release**. The author's stratified review records 1,400/1,400 final equivalent decisions after 42 re-adjudications, but the changed decisions lack per-pair reasons. Six DisasterM3 strings have been revised in segmentation or report tasks outside the reported closed-answer main experiment. A downstream reuse license, formal archival identifier, full generation/scoring code, and frozen transformation rules remain outstanding.

Repository: [CarlBruce/SEV-Change](https://github.com/CarlBruce/SEV-Change). Candidate version: `v0.1.0-rc2`. No dataset DOI or GitHub release tag has been minted. See `RELEASE_METADATA.md` for publication status.

## Verify and download the complete data package

From a clean clone, first verify the numbered parts, assembled ZIP contents, all 11 JSON files, and `manifest.json` without extracting anything:

```bash
python scripts/verify_release_archive.py
```

The 11 JSON files are preserved inside one ZIP, distributed as numbered parts under `release/` because this upload route timed out on large individual files. The `rc2` candidate changes six DisasterM3 question strings relative to `rc1`; record counts are unchanged. Download every part named by `release/parts.json`, then run:

```bash
python scripts/archive_parts.py assemble release/parts.json SEV-Change-v0.1.0-rc2-git.zip
```

The assembly script verifies each part and the ZIP against SHA-256 hashes in `release/parts.json`. Extract it to access `data/rsrcc/` and `data/disasterm3/`. The older `rc1` parts remain for versioned comparison and are described by `release/rc1_parts.json`; do not mix parts across versions. No images or masks are included. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the structural-validation command after extraction.

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

For record-level errors, use the [data issue template](.github/ISSUE_TEMPLATE/data_issue.md). Do not attach upstream images or masks unless redistribution is permitted. Changes to the candidate documentation are recorded in [CHANGELOG.md](CHANGELOG.md).

## Data format

All data files are UTF-8 JSON arrays. Every record contains:

- `pre_image_path`, `post_image_path`: paths expected relative to the corresponding upstream image dataset;
- `ground_truth`: answer, count, class, or target-mask metadata, depending on the task;
- `variants`: an object with exactly eight string fields in order: `raw`, `t1`, ..., `t7`.

RSRCC records additionally contain stable IDs, split, answer-type, candidate-option, and source-text metadata. DisasterM3 records additionally contain task, event, category, and original-index metadata; candidate-option fields exist only for applicable VQA tasks, while segmentation records use mask paths as ground truth. Images and masks are **not** included in this package.

The annotations are derived from [RSRCC](https://huggingface.co/datasets/google/RSRCC) and [DisasterM3](https://github.com/Junjue-Wang/DisasterM3). Cite the relevant original datasets when using either subset; source links and verified citation details are collected in `SOURCES.md`.

## Validation and audit status

The read-only archive verifier and structural validator use only the Python standard library. **Do not run the structural validator directly in the repository root:** the JSON files are inside the ZIP, not in a root `data/` directory. After extraction, run:

```bash
python -m zipfile -e SEV-Change-v0.1.0-rc2-git.zip extracted
python scripts/validate_dataset.py --root extracted
```

The validator checks JSON structure, required fields, variant completeness/order, empty text, raw/source alignment, and duplicate logical records. The repository-root `manifest.json` records file size and SHA-256 values generated from the packaged data. These checks **do not prove semantic equivalence**.

One RSRCC raw-task identity occurs twice (`test_003550` and `test_009075`). The two records have different generated variants and are retained pending an upstream-source audit; the validator reports this as a warning rather than silently deleting either record.

The author's earlier review workbook labeled 1,358 of 1,400 sampled pairs equivalent and 42 non-equivalent. The supplied final-adjudication workbook changes those 42 final decisions to equivalent, yielding 1,400/1,400 in the stratified sample; six corrected DisasterM3 strings are included in this `rc2` candidate. The per-pair reasons for the changed decisions are not recorded, and the sample does not establish full-dataset equivalence. See [AUDIT_STATUS.md](AUDIT_STATUS.md). The six edits fall outside the reported five-task closed-answer baseline, but exact sample-ID and prediction artifacts have not yet been published for independent verification. [REPRODUCIBILITY.md](REPRODUCIBILITY.md) states which evaluation artifacts are missing.

## Before final release

Do not present this candidate as a final audited benchmark until the items in `RELEASE_CHECKLIST.md` are resolved. The 29,024 DisasterM3 count is obtained by the documented paired-image eligibility rule in `EXCLUSIONS.md`. [SCIENTIFIC_DATA_READINESS.md](SCIENTIFIC_DATA_READINESS.md) maps the current repository against the journal's data and code requirements. GitHub availability alone does not establish long-term data deposition or a reuse license.

## Citation

Citation metadata has not yet been finalized. Add a verified paper citation and `CITATION.cff` only after the title, authors, venue/preprint identifier, and release version are frozen.
