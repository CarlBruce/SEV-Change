# SEV-Change Dataset Card (Draft)

Public candidate version: `v0.1.0-rc2` at [CarlBruce/SEV-Change](https://github.com/CarlBruce/SEV-Change). The complete data package is distributed as verified ZIP parts; no DOI is available. See `RELEASE_METADATA.md`.

## Summary

SEV-Change evaluates whether a vision-language model preserves its answer under controlled, intended-to-be semantically equivalent question reformulations for bitemporal remote-sensing imagery. The release combines variants derived from the RSRCC test split and ten DisasterM3 disaster categories.

## Intended use

- Robustness evaluation for change visual question answering.
- Comparison of raw-question accuracy with semantic-invariance metrics.
- Analysis by transformation type, question type, task, or disaster category.

The dataset is not intended to establish causal claims about model architecture or linguistic competence without paired statistical tests and manual equivalence validation.

## Variants

Each record has `raw` plus `t1`–`t7`. The working manuscript describes the seven transformations as temporal-reference, predicate/state, entity/category, attribute/degree, reference/order, polarity, and register/style reformulations. These labels are provisional until the generation prompts and rule version are audited and published.

## Source data and images

This package contains question/answer annotations and image paths only. It does not redistribute RSRCC or DisasterM3 imagery. Users must obtain the source imagery under the terms set by the respective dataset owners and reconstruct the expected path layout.

DisasterM3 is task-heterogeneous. Candidate-option fields are present for applicable VQA records but are not required for segmentation records, whose ground truth may be a mask path.

## Current statistics

- RSRCC: 21,999 task-level records; 175,992 question expressions.
- DisasterM3: 29,024 task-level records; 232,192 question expressions.
- Combined: 51,023 task-level records; 408,184 question expressions.

The source DisasterM3 variant files contained 30,042 records. The release excludes 1,018 single-image relational-reasoning records that lack paired pre-/post-disaster paths. The eligibility rule and reproducible filter are documented in `EXCLUSIONS.md`.

## Known limitations

- The author's stratified review records final equivalent judgments for all 1,400 sampled pairs after 42 re-adjudications. Six DisasterM3 strings were revised and synchronized in this candidate. This is not a full-dataset quality guarantee; the 42 per-pair reasons and full review workbook are not public. See `AUDIT_STATUS.md`.
- The transformation prompts, generation parameters, and exact rule definitions are not yet frozen.
- The image data are external dependencies.
- The uploader attested redistribution rights, but no explicit downstream reuse license has been assigned.
- Existing experiments cover a filtered comparable subset rather than every packaged DisasterM3 record.
- The six revised strings occur in segmentation or report tasks outside the reported five-task closed-answer baseline. That baseline has not been recomputed, and its full sample-ID, inference, and scoring artifacts are not yet public.
- English-language variants do not measure multilingual robustness.

## Licensing and ethics

No onward reuse license is asserted by this candidate package. The official RSRCC dataset page labels its dataset `apache-2.0`; the official DisasterM3 repository restricts images and associated annotations to academic, non-commercial use. The applicable license for this combined derivative annotation release is still unresolved. See `LICENSE_STATUS.md` for source links and the exact status.

## Maintenance

Confirm the maintainer contact, version history, issue-reporting procedure, and archival DOI before the final release.
