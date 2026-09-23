from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_archive(archive: Path, output_dir: Path, chunk_size: int) -> None:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if not archive.is_file():
        raise FileNotFoundError(archive)
    output_dir.mkdir(parents=True, exist_ok=True)
    data = archive.read_bytes()
    parts: list[dict[str, object]] = []
    for index, offset in enumerate(range(0, len(data), chunk_size), start=1):
        name = f"{archive.name}.part{index:02d}"
        chunk = data[offset:offset + chunk_size]
        part_path = output_dir / name
        with part_path.open("xb") as handle:
            handle.write(chunk)
        parts.append({"name": name, "bytes": len(chunk), "sha256": sha256_bytes(chunk)})

    manifest = {
        "archive_name": archive.name,
        "archive_bytes": len(data),
        "archive_sha256": sha256_bytes(data),
        "parts": parts,
    }
    manifest_path = output_dir / "parts.json"
    with manifest_path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Created {len(parts)} parts: {manifest_path}")


def assemble_archive(manifest_path: Path, output_path: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if output_path.name != manifest["archive_name"]:
        raise ValueError(f"output filename must be {manifest['archive_name']}")
    digest = hashlib.sha256()
    total_bytes = 0
    with output_path.open("xb") as output:
        for part in manifest["parts"]:
            part_path = manifest_path.parent / part["name"]
            data = part_path.read_bytes()
            if len(data) != part["bytes"] or sha256_bytes(data) != part["sha256"]:
                raise ValueError(f"part failed validation: {part_path}")
            output.write(data)
            digest.update(data)
            total_bytes += len(data)
    if total_bytes != manifest["archive_bytes"] or digest.hexdigest() != manifest["archive_sha256"]:
        output_path.unlink()
        raise ValueError("assembled archive failed validation")
    print(f"Verified archive: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Split or assemble a verified release ZIP")
    subparsers = parser.add_subparsers(dest="command", required=True)
    split_parser = subparsers.add_parser("split")
    split_parser.add_argument("archive", type=Path)
    split_parser.add_argument("output_dir", type=Path)
    split_parser.add_argument("--chunk-size", type=int, default=1_500_000)
    assemble_parser = subparsers.add_parser("assemble")
    assemble_parser.add_argument("manifest", type=Path)
    assemble_parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.command == "split":
        split_archive(args.archive, args.output_dir, args.chunk_size)
    else:
        assemble_archive(args.manifest, args.output)


if __name__ == "__main__":
    main()
