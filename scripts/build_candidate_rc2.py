"""Build the rc2 candidate from the verified rc1 archive with six text edits.

This is a versioned, deterministic packaging step. It preserves the rc1 parts,
updates only six DisasterM3 variant strings, and refreshes the data manifest.
It does not validate semantic equivalence or rerun model predictions.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import shutil
import zipfile
from pathlib import Path
from typing import Any


RELEASE_NAME = "SEV-Change-v0.1.0-rc2-git.zip"
CHUNK_SIZE = 1_500_000
REVISIONS: dict[str, tuple[str, str, str, str]] = {
    "S0726": ("conflict", "365", "t3", "Identify and delineate buildings that have been completely destroyed."),
    "S0739": ("conflict", "264", "t4", "Classify and separate buildings that remain structurally sound."),
    "S0826": ("earthquake", "3069", "t6", "Provide a comprehensive description of damage based on the pre- and post-disaster images."),
    "S1009": ("flood", "2225", "t3", "Locate and delineate road surfaces covered by floodwater."),
    "S1078": ("hurricane", "2599", "t3", "Locate and segment road surfaces that remain undamaged."),
    "S1287": ("tsunami", "1464", "t3", "Locate roads blocked by debris and segment those road regions."),
}
OLD_TEXT: dict[str, str] = {
    "S0726": "Locate and delineate man-made structures exhibiting total collapse.",
    "S0739": "Classify and separate the critical infrastructure elements that have sustained no structural harm.",
    "S0826": "Is it true that a comprehensive description of the damage can be derived from comparing the pre- and post-disaster images? Please confirm and elaborate.",
    "S1009": "Pinpoint and demarcate the transportation routes that are covered by floodwater.",
    "S1078": "Identify and outline transportation routes that exhibit no signs of damage.",
    "S1287": "Highlight transportation routes impeded by rubble and segment the impacted zones.",
}
DOCUMENTS = (
    "AUDIT_STATUS.md", "CHANGELOG.md", "DATASET_CARD.md", "DATA_DICTIONARY.md",
    "EXCLUSIONS.md", "LICENSE_STATUS.md", "README.md", "README_zh-CN.md",
    "RELEASE_CHECKLIST.md", "RELEASE_METADATA.md", "REPRODUCIBILITY.md",
    "SCIENTIFIC_DATA_READINESS.md", "SOURCES.md",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def assemble_rc1(release_dir: Path) -> bytes:
    source_manifest = release_dir / "rc1_parts.json"
    if not source_manifest.exists():
        source_manifest = release_dir / "parts.json"
    parts = json.loads(source_manifest.read_text(encoding="utf-8"))
    if parts["archive_name"] != "SEV-Change-v0.1.0-rc1-git.zip":
        raise ValueError("Expected rc1 parts.json; refusing to build from another version")
    chunks: list[bytes] = []
    for part in parts["parts"]:
        payload = (release_dir / part["name"]).read_bytes()
        if len(payload) != part["bytes"] or sha256(payload) != part["sha256"]:
            raise ValueError(f"Invalid rc1 part: {part['name']}")
        chunks.append(payload)
    archive = b"".join(chunks)
    if len(archive) != parts["archive_bytes"] or sha256(archive) != parts["archive_sha256"]:
        raise ValueError("Invalid assembled rc1 archive")
    return archive


def build(root: Path, output_zip: Path, replace_candidate: bool) -> None:
    release_dir = root / "release"
    old_archive = zipfile.ZipFile(io.BytesIO(assemble_rc1(release_dir)))
    manifest = json.loads(old_archive.read("manifest.json"))
    if manifest["release_version"] != "v0.1.0-rc1":
        raise ValueError("Expected rc1 data manifest")

    patched: dict[str, bytes] = {}
    found: set[str] = set()
    for entry in manifest["files"]:
        name = entry["path"]
        payload = old_archive.read(name)
        if not name.startswith("data/disasterm3/"):
            patched[name] = payload
            continue
        category = Path(name).stem.removeprefix("DisasterM3_").removesuffix("_variants")
        revisions = [(sample_id, revision) for sample_id, revision in REVISIONS.items() if revision[0] == category]
        if not revisions:
            patched[name] = payload
            continue
        records = json.loads(payload)
        changed = 0
        for sample_id, (_, original_index, variant_type, revised_text) in revisions:
            matches = [record for record in records if str(record.get("_original_index")) == original_index]
            if len(matches) != 1:
                raise ValueError(f"Expected one packaged record for {sample_id}, got {len(matches)}")
            record = matches[0]
            if record["variants"][variant_type] != OLD_TEXT[sample_id]:
                raise ValueError(f"Old text mismatch for {sample_id}")
            record["variants"][variant_type] = revised_text
            found.add(sample_id)
            changed += 1
        if changed != len(revisions):
            raise ValueError(f"Revision count mismatch in {name}")
        patched[name] = json_bytes(records)
        entry["bytes"] = len(patched[name])
        entry["sha256"] = sha256(patched[name])

    if found != set(REVISIONS):
        raise ValueError(f"Missing revisions: {set(REVISIONS) - found}")
    manifest["release_version"] = "v0.1.0-rc2"
    manifest["release_status"] = "public_candidate_post_adjudication_pending_rerun"
    for dataset in ("RSRCC", "DisasterM3"):
        manifest["totals"][dataset]["bytes"] = sum(
            entry["bytes"] for entry in manifest["files"] if entry["dataset"] == dataset
        )
    manifest_payload = json_bytes(manifest)

    if output_zip.exists():
        raise FileExistsError(f"Refusing to overwrite output ZIP: {output_zip}")
    legacy_manifest = release_dir / "rc1_parts.json"
    if replace_candidate:
        current_parts = json.loads((release_dir / "parts.json").read_text(encoding="utf-8"))
        if not legacy_manifest.exists() or current_parts["archive_name"] != RELEASE_NAME:
            raise ValueError("Replacement requires an existing rc1 backup and rc2 candidate")
        for part in current_parts["parts"]:
            current_payload = (release_dir / part["name"]).read_bytes()
            if len(current_payload) != part["bytes"] or sha256(current_payload) != part["sha256"]:
                raise ValueError(f"Existing rc2 part changed unexpectedly: {part['name']}")
    elif legacy_manifest.exists():
        raise FileExistsError("rc2 already exists; use --replace-candidate after verifying the current parts")
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as target:
        for item in old_archive.infolist():
            name = item.filename
            if item.is_dir():
                target.writestr(name, b"")
            elif name in patched:
                target.writestr(name, patched[name])
            elif name == "manifest.json":
                target.writestr(name, manifest_payload)
            elif name in DOCUMENTS:
                target.writestr(name, (root / name).read_bytes())
            elif name.startswith("scripts/") and (root / name).is_file():
                target.writestr(name, (root / name).read_bytes())
            else:
                target.writestr(name, old_archive.read(name))
        existing = set(old_archive.namelist())
        for name in DOCUMENTS:
            if name not in existing:
                target.writestr(name, (root / name).read_bytes())

    with zipfile.ZipFile(output_zip) as check:
        if check.testzip() is not None:
            raise ValueError("rc2 ZIP failed CRC validation")
        for entry in manifest["files"]:
            payload = check.read(entry["path"])
            if len(payload) != entry["bytes"] or sha256(payload) != entry["sha256"]:
                raise ValueError(f"rc2 manifest mismatch: {entry['path']}")

    archive_bytes = output_zip.read_bytes()
    new_parts: list[dict[str, object]] = []
    for index, offset in enumerate(range(0, len(archive_bytes), CHUNK_SIZE), start=1):
        name = f"{RELEASE_NAME}.part{index:02d}"
        if (release_dir / name).exists() and not replace_candidate:
            raise FileExistsError(name)
        part = archive_bytes[offset:offset + CHUNK_SIZE]
        new_parts.append({"name": name, "bytes": len(part), "sha256": sha256(part)})

    if not legacy_manifest.exists():
        shutil.copy2(release_dir / "parts.json", legacy_manifest)
    for index, offset in enumerate(range(0, len(archive_bytes), CHUNK_SIZE)):
        (release_dir / new_parts[index]["name"]).write_bytes(archive_bytes[offset:offset + CHUNK_SIZE])
    parts_manifest = {
        "archive_name": RELEASE_NAME,
        "archive_bytes": len(archive_bytes),
        "archive_sha256": sha256(archive_bytes),
        "parts": new_parts,
    }
    (release_dir / "parts.json").write_bytes(json_bytes(parts_manifest))
    (root / "manifest.json").write_bytes(manifest_payload)
    print(f"Built {RELEASE_NAME}: {len(new_parts)} parts, six revised strings")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-zip", type=Path, required=True)
    parser.add_argument("--replace-candidate", action="store_true")
    args = parser.parse_args()
    build(Path(__file__).resolve().parent.parent, args.output_zip.resolve(), args.replace_candidate)


if __name__ == "__main__":
    main()
