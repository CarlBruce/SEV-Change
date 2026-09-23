from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def is_bitemporal(record: dict[str, Any]) -> bool:
    return bool(record.get("pre_image_path")) and bool(record.get("post_image_path"))


def filter_file(input_path: Path, output_path: Path) -> tuple[int, int]:
    with input_path.open("r", encoding="utf-8") as handle:
        records = json.load(handle)
    if not isinstance(records, list) or not all(isinstance(item, dict) for item in records):
        raise ValueError("input must be a JSON array of objects")

    kept = [record for record in records if is_bitemporal(record)]
    excluded = [record for record in records if not is_bitemporal(record)]
    unexpected = [
        record
        for record in excluded
        if record.get("task") != "Relational Reasoning" or not record.get("image_path")
    ]
    if unexpected:
        raise ValueError(
            f"refusing to filter: {len(unexpected)} excluded records are not the expected "
            "single-image Relational Reasoning records"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(kept, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return len(kept), len(excluded)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Keep only DisasterM3 records with both pre- and post-disaster image paths"
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    kept, excluded = filter_file(args.input, args.output)
    print(f"kept={kept:,}; excluded={excluded:,}; output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
