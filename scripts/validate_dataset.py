from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


VARIANT_KEYS = ("raw", "t1", "t2", "t3", "t4", "t5", "t6", "t7")
COMMON_KEYS = (
    "pre_image_path",
    "post_image_path",
    "ground_truth",
    "variants",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_records(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"{path}: top-level JSON value must be a list")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError(f"{path}: every record must be an object")
    return data


def record_identity(record: dict[str, Any]) -> str:
    identity = {
        "pre_image_path": record.get("pre_image_path"),
        "post_image_path": record.get("post_image_path"),
        "raw": record.get("variants", {}).get("raw"),
        "ground_truth": record.get("ground_truth"),
        "options_list": record.get("options_list"),
    }
    payload = json.dumps(identity, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_file(path: Path, root: Path) -> tuple[dict[str, Any], list[str], list[str]]:
    records = load_records(path)
    errors: list[str] = []
    warnings: list[str] = []
    identities: Counter[str] = Counter()
    raw_mismatch = 0

    is_rsrcc = "rsrcc" in path.parts
    dataset = "RSRCC" if is_rsrcc else "DisasterM3"
    required = list(COMMON_KEYS)
    required.extend(("id", "source_index", "split", "answer_type") if is_rsrcc else (
        "prompts",
        "task",
        "_disaster_category",
        "_event_name",
        "_original_index",
    ))

    for index, record in enumerate(records):
        missing = [key for key in required if key not in record]
        if missing:
            errors.append(f"{path.name}[{index}] missing keys: {', '.join(missing)}")
            continue

        variants = record.get("variants")
        if not isinstance(variants, dict):
            errors.append(f"{path.name}[{index}].variants is not an object")
            continue
        if tuple(variants.keys()) != VARIANT_KEYS:
            errors.append(
                f"{path.name}[{index}] variant keys/order are {tuple(variants.keys())}, "
                f"expected {VARIANT_KEYS}"
            )
        empty = [key for key in VARIANT_KEYS if not isinstance(variants.get(key), str) or not variants[key].strip()]
        if empty:
            errors.append(f"{path.name}[{index}] empty/non-string variants: {', '.join(empty)}")

        source_raw = record.get("source_text") if is_rsrcc else record.get("prompts")
        raw_text = variants.get("raw")
        if is_rsrcc:
            aligned = isinstance(source_raw, str) and isinstance(raw_text, str) and raw_text in source_raw
        else:
            aligned = raw_text == source_raw
        if not aligned:
            raw_mismatch += 1
        identities[record_identity(record)] += 1

    duplicate_records = sum(count - 1 for count in identities.values() if count > 1)
    if duplicate_records:
        warnings.append(f"{path.name}: {duplicate_records} duplicate raw-task identities")
    if raw_mismatch:
        warnings.append(f"{path.name}: {raw_mismatch} raw/source text mismatches")

    entry = {
        "path": path.relative_to(root).as_posix(),
        "dataset": dataset,
        "records": len(records),
        "question_expressions": len(records) * len(VARIANT_KEYS),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "duplicate_raw_task_identities": duplicate_records,
        "raw_source_mismatches": raw_mismatch,
    }
    if not is_rsrcc:
        entry["category"] = path.stem.removeprefix("DisasterM3_").removesuffix("_variants")
    return entry, errors, warnings


def validate(root: Path, write_manifest: bool) -> int:
    data_root = root / "data"
    paths = sorted(data_root.rglob("*.json"))
    if not paths:
        print(f"ERROR: no JSON files found under {data_root}")
        return 1

    entries: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    for path in paths:
        entry, file_errors, file_warnings = validate_file(path, root)
        entries.append(entry)
        errors.extend(file_errors)
        warnings.extend(file_warnings)
        print(f"OK  {entry['path']}: {entry['records']:,} records")

    totals: dict[str, dict[str, int]] = {}
    for dataset in ("RSRCC", "DisasterM3"):
        subset = [entry for entry in entries if entry["dataset"] == dataset]
        totals[dataset] = {
            "files": len(subset),
            "records": sum(entry["records"] for entry in subset),
            "question_expressions": sum(entry["question_expressions"] for entry in subset),
            "bytes": sum(entry["bytes"] for entry in subset),
        }

    manifest = {
        "release_name": "SEV-Change",
        "release_version": "v0.1.0-rc1",
        "release_status": "public_candidate_pending_adjudication",
        "format_version": "1.0",
        "variant_keys": list(VARIANT_KEYS),
        "totals": totals,
        "files": entries,
        "validation": {
            "errors": len(errors),
            "warnings": len(warnings),
        },
    }
    if write_manifest:
        manifest_path = root / "manifest.json"
        with manifest_path.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(manifest, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        print(f"WROTE {manifest_path}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors[:50]:
        print(f"ERROR: {error}")
    if len(errors) > 50:
        print(f"ERROR: {len(errors) - 50} additional errors omitted")

    print(
        "TOTALS: "
        f"RSRCC={totals['RSRCC']['records']:,} records; "
        f"DisasterM3={totals['DisasterM3']['records']:,} records; "
        f"errors={len(errors)}; warnings={len(warnings)}"
    )
    return 1 if errors else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate SEV-Change release data and generate manifest.json")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Release root containing data/ (default: parent of scripts/)",
    )
    parser.add_argument("--write-manifest", action="store_true", help="Write manifest.json after validation")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return validate(args.root.resolve(), args.write_manifest)


if __name__ == "__main__":
    raise SystemExit(main())
