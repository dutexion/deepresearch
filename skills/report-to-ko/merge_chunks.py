#!/usr/bin/env python3
"""Merge translated chunks back into a single report."""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Merge translated chunks into final report")
    parser.add_argument("--chunks-dir", "-d", default="chunks", help="Directory containing chunks")
    parser.add_argument("--output", "-o", help="Output file path (default: report_ko.md)")
    args = parser.parse_args()

    manifest_path = f"{args.chunks_dir}/manifest.json"
    try:
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Manifest not found: {manifest_path}")
        print("Run chunk_report.py first.")
        sys.exit(1)

    total_chunks = manifest["total_chunks"]
    merged_lines = []
    missing = []
    completed = []

    for chunk in manifest["chunks"]:
        ko_file = chunk["output"]
        idx = chunk["index"]
        try:
            with open(ko_file, encoding="utf-8") as f:
                content = f.read()
            merged_lines.append(content)
            if not content.endswith("\n"):
                merged_lines.append("\n")
            completed.append(idx)
        except FileNotFoundError:
            missing.append(idx)
            print(f"[WARN] Missing: chunk_{idx:02d}_ko.md")

    if missing:
        print(f"\n[ERROR] {len(missing)} chunks missing: {missing}")
        print(f"Completed: {len(completed)}/{total_chunks}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        source = manifest.get("source", "report.md")
        base = source.rsplit(".", 1)[0]
        output_path = f"{base}_ko.md"

    merged_content = "".join(merged_lines)
    total_output_lines = merged_content.count("\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(merged_content)

    # Validation
    source_lines = manifest["total_lines"]
    ratio = total_output_lines / source_lines if source_lines > 0 else 0

    print(f"\n{'=' * 50}")
    print(f"Merge complete!")
    print(f"{'=' * 50}")
    print(f"Source lines:  {source_lines}")
    print(f"Output lines:  {total_output_lines}")
    print(f"Ratio:         {ratio:.2f}x")
    print(f"Chunks merged: {len(completed)}/{total_chunks}")
    print(f"Output:        {output_path}")

    if ratio < 0.5 or ratio > 2.0:
        print(f"\n[WARN] Line ratio {ratio:.2f}x is outside expected range (0.5x-2.0x)")


if __name__ == "__main__":
    main()
