# Reproducibility and Evaluation Scope

## What this repository currently supports

The seven numbered files in `release/` reconstruct one frozen ZIP. `release/parts.json` records its size and SHA-256 hash; `manifest.json` records each of the 11 JSON data files' size, hash, and record count. Run the read-only check directly from a clone:

```bash
python scripts/verify_release_archive.py
```

To inspect and run the deeper structural validator, assemble and extract the archive first:

```bash
python scripts/archive_parts.py assemble release/parts.json SEV-Change-v0.1.0-rc2-git.zip
python -m zipfile -e SEV-Change-v0.1.0-rc2-git.zip extracted
python scripts/validate_dataset.py --root extracted
```

The extraction path must contain `data/` directly. `validate_dataset.py` checks record structure and raw/source alignment, but neither script checks semantic equivalence against imagery. The archive contains no source images or masks. See `SOURCES.md`, `DATA_DICTIONARY.md`, and `AUDIT_STATUS.md`.

## Published candidate baseline scope

The working manuscript describes seven common vision-language models: InternVL3-2B, InternVL3-8B, Qwen2.5-VL-7B, Qwen3-VL-2B, Qwen3-VL-4B, Qwen3-VL-32B, and Gemma 3 4B. RSRCC-V has 21,999 evaluated records per model. DisasterM3-V has 29,024 packaged records across eight tasks, but the reported Exact Match baseline uses 11,945 complete records per model from five closed-answer tasks. The other three DisasterM3 task types are not covered by those reported Exact Match results. The two sources have different task and answer spaces; absolute scores are not a controlled cross-source difficulty comparison.

The current repository **does not yet contain the complete code and artifacts needed to reproduce the manuscript's model scores**. Missing items include the exact common sample-ID lists, per-sample predictions, source-specific answer parsers, full scoring and aggregation scripts, generation prompts and transformation-rule version, all model checkpoint revisions, image preprocessing details, and complete RSRCC-V inference configuration. Existing validation scripts only verify the released data files. Do not cite them as the full benchmark implementation.

Before claiming a reproducible final benchmark, freeze and publish those items, document the 42 changed decisions' per-pair reasons, rerun affected predictions on `v0.1.0-rc2`, and record dataset/code revisions together. See `RELEASE_CHECKLIST.md`.
