# Data Files and Field Dictionary

## Files and encoding

All 11 data files are UTF-8 `.json` files. Each file is a top-level array of task-level record objects. No JSON Lines, CSV, Parquet, image, or mask files are included. The file hashes and per-file counts are in `manifest.json`.

| Path | Content |
|---|---|
| `data/rsrcc/rsrcc_test_variants.json` | 21,999 RSRCC test records |
| `data/disasterm3/DisasterM3_<category>_variants.json` | 10 disaster-category files; 29,024 paired-image records in total |

## Shared fields

| Field | Type | Meaning |
|---|---|---|
| `pre_image_path` | string | Relative path to the earlier source image; image absent from this package |
| `post_image_path` | string | Relative path to the later source image; image absent from this package |
| `ground_truth` | string or number | Task-dependent target; may be an answer, count, class, or mask path |
| `variants` | object of eight strings | `raw`, `t1`, `t2`, `t3`, `t4`, `t5`, `t6`, `t7` |

`raw` is the original question/prompt. The other seven strings are generated reformulations. Their exact generation rule version is not frozen in this candidate release; the labels should not be interpreted as a verified semantic-equivalence guarantee.

## RSRCC-specific fields

Every RSRCC record has `id`, `source_index`, `split`, `answer_type`, `ground_truth_option`, `ground_truth_text`, `options_list`, `options_str`, `variant_types`, `source_text`, `_variant_source`, `_llm_model`, `_llm_success`, `transformation_rule_version`, `qc_status`, and `qc_warnings`. Some records also have repair or manual-review metadata. `source_text` contains the original formatted question, candidate answers, and answer; `variants.raw` is the question text within it.

## DisasterM3-specific fields

Every DisasterM3 record has `prompts`, `task`, `_disaster_category`, `_event_name`, `_original_index`, and `_variant_source`. `variants.raw` equals `prompts`. `ground_truth_option`, `options_list`, and `options_str` appear only where the task uses answer options. `image_type`, `post_image_type`, and `cls_description` also vary by task. Some segmentation targets are mask paths rather than answer strings.

## Paths and record scope

DisasterM3 paths currently use backslashes in their original source records; RSRCC paths use forward slashes. Treat both as relative paths and normalize separators on the target operating system. The release keeps only DisasterM3 records containing both `pre_image_path` and `post_image_path`; the exclusion rule is documented in `EXCLUSIONS.md`.

## DisasterM3 task coverage

The following counts are calculated from the ten packaged JSON files. `options_list` identifies the five closed-answer task types used by the current Exact Match baseline; it is not present for every task.

| Task | Packaged records | In closed-answer pool? |
|---|---:|---|
| Building Damage Counting | 4,982 | Yes |
| Disaster Bearing Bodies Recognition | 2,363 | Yes |
| Disaster Type Recognition | 420 | Yes |
| Road Damage Counting | 2,178 | Yes |
| Disaster Scene Recognition | 2,007 | Yes |
| Referring Expression Segmentation | 12,348 | No |
| Disaster Report | 2,363 | No |
| Disaster Restoration Advice | 2,363 | No |
| **Total** | **29,024** | **11,950 with options** |

The working manuscript's seven-model Exact Match baseline uses 11,945 complete shared records, five fewer than the option-bearing pool. The exact common sample-ID list and per-sample predictions are not yet published. The baseline must not be described as covering all 29,024 records or all eight tasks.

## Quality metadata scope

RSRCC records include `qc_status` and `transformation_rule_version`; the current DisasterM3 files do not have equivalent per-record fields. The current data files do not encode the later 1,400-pair human-audit decisions as per-record metadata. Refer to `AUDIT_STATUS.md` before using the candidate variants as a strict semantic-equivalence benchmark.
