"""Verify the published split archive against parts.json and manifest.json.

This script is read-only and uses only the Python standard library. It checks
bytes, hashes, JSON structure, variant completeness, and record counts. It
does not establish that question variants are semantically equivalent.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path
from typing import Any


VARIANT_KEYS = ("raw", "t1", "t2", "t3", "t4", "t5", "t6", "t7")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def assemble_in_memory(parts_path: Path) -> bytes:
    parts_manifest = load_json(parts_path)
    chunks: list[bytes] = []
    for part in parts_manifest["parts"]:
        name = part["name"]
        if Path(name).name != name:
            raise ValueError(f"Unsafe part filename: {name}")
        chunk = (parts_path.parent / name).read_bytes()
        if len(chunk) != part["bytes"] or sha256_bytes(chunk) != part["sha256"]:
            raise ValueError(f"Part size or SHA-256 mismatch: {name}")
        chunks.append(chunk)
    archive = b"".join(chunks)
    if len(archive) != parts_manifest["archive_bytes"]:
        raise ValueError("Assembled archive size mismatch")
    if sha256_bytes(archive) != parts_manifest["archive_sha256"]:
        raise ValueError("Assembled archive SHA-256 mismatch")
    return archive


def verify_data_file(archive: zipfile.ZipFile, entry: dict[str, Any]) -> None:
    name = entry["path"]
    payload = archive.read(name)
    if len(payload) != entry["bytes"] or sha256_bytes(payload) != entry["sha256"]:
        raise ValueError(f"Data file size or SHA-256 mismatch: {name}")
    records = json.loads(payload.decode("utf-8"))
    if not isinstance(records, list) or len(records) != entry["records"]:
        raise ValueError(f"Record count mismatch: {name}")
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"Non-object record: {name}[{index}]")
        variants = record.get("variants")
        if not isinstance(variants, dict) or tuple(variants) != VARIANT_KEYS:
            raise ValueError(f"Variant keys/order mismatch: {name}[{index}]")
        if any(not isinstance(variants[key], str) or not variants[key].strip() for key in VARIANT_KEYS):
            raise ValueError(f"Empty or non-string variant: {name}[{index}]")
    expected_expressions = len(records) * len(VARIANT_KEYS)
    if entry["question_expressions"] != expected_expressions:
        raise ValueError(f"Expression count mismatch: {name}")
    print(f"OK {name}: {len(records):,} records")


def verify(parts_path: Path, manifest_path: Path) -> None:
    archive_bytes = assemble_in_memory(parts_path)
    manifest = load_json(manifest_path)
    entries = manifest["files"]
    expected_files = {entry["path"] for entry in entries}
    if len(expected_files) != 11 or len(entries) != 11:
        raise ValueError("Expected exactly 11 distinct data files in manifest")

    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise ValueError(f"Corrupt ZIP member: {bad_member}")
        names = set(archive.namelist())
        if not expected_files.issubset(names):
            raise ValueError(f"Missing data files: {sorted(expected_files - names)}")
        actual_data_files = {
            name for name in names if name.startswith("data/") and name.endswith(".json")
        }
        if actual_data_files != expected_files:
            raise ValueError("Archive data-file list differs from manifest")
        for entry in entries:
            verify_data_file(archive, entry)

    for dataset in ("RSRCC", "DisasterM3"):
        subset = [entry for entry in entries if entry["dataset"] == dataset]
        reported = manifest["totals"][dataset]
        if reported["files"] != len(subset):
            raise ValueError(f"File total mismatch: {dataset}")
        if reported["records"] != sum(entry["records"] for entry in subset):
            raise ValueError(f"Record total mismatch: {dataset}")
        if reported["question_expressions"] != sum(entry["question_expressions"] for entry in subset):
            raise ValueError(f"Expression total mismatch: {dataset}")
        if reported["bytes"] != sum(entry["bytes"] for entry in subset):
            raise ValueError(f"Byte total mismatch: {dataset}")
    print("Archive, 11 data files, and manifest verified.")
    print("Semantic equivalence and source-image availability are NOT verified by this script.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parts", type=Path, default=Path("release/parts.json"))
    parser.add_argument("--manifest", type=Path, default=Path("manifest.json"))
    args = parser.parse_args()
    try:
        verify(args.parts, args.manifest)
    except (OSError, KeyError, TypeError, ValueError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
