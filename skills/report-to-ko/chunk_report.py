#!/usr/bin/env python3
"""Split a large markdown report into chunks at heading boundaries."""

import argparse
import json
import os
import sys


def find_heading_positions(lines):
    """Find line indices where ## or ### headings appear."""
    positions = []
    for i, line in enumerate(lines):
        if line.startswith("## ") or line.startswith("### "):
            positions.append(i)
    return positions


def chunk_report(lines, min_chunk_size=300, max_chunk_size=600):
    """Split lines into chunks at heading boundaries."""
    headings = find_heading_positions(lines)
    if not headings:
        return [(0, len(lines))]

    chunks = []
    current_start = 0

    for pos in headings:
        chunk_size = pos - current_start
        if chunk_size >= min_chunk_size:
            chunks.append((current_start, pos))
            current_start = pos

    # Last chunk
    if current_start < len(lines):
        last_size = len(lines) - current_start
        # Merge tiny last chunk with previous
        if last_size < 100 and chunks:
            prev_start, _ = chunks.pop()
            chunks.append((prev_start, len(lines)))
        else:
            chunks.append((current_start, len(lines)))

    return chunks


def get_context(lines, start, end, num_lines=20):
    """Extract context lines."""
    selected = lines[start:end]
    return "".join(selected)


def main():
    parser = argparse.ArgumentParser(description="Split markdown report into chunks")
    parser.add_argument("report", help="Path to report.md")
    parser.add_argument("--output-dir", "-o", default="chunks", help="Output directory for chunks")
    parser.add_argument("--min-size", type=int, default=300, help="Minimum chunk size in lines")
    parser.add_argument("--max-size", type=int, default=600, help="Maximum chunk size in lines")
    args = parser.parse_args()

    with open(args.report, encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)
    print(f"Total lines: {total_lines}")

    chunks = chunk_report(lines, args.min_size, args.max_size)
    print(f"Number of chunks: {len(chunks)}")

    os.makedirs(args.output_dir, exist_ok=True)

    manifest = {
        "source": os.path.abspath(args.report),
        "total_lines": total_lines,
        "total_chunks": len(chunks),
        "chunks": [],
    }

    for i, (start, end) in enumerate(chunks):
        chunk_file = os.path.join(args.output_dir, f"chunk_{i:02d}.md")
        ko_file = os.path.join(args.output_dir, f"chunk_{i:02d}_ko.md")

        with open(chunk_file, "w", encoding="utf-8") as f:
            f.writelines(lines[start:end])

        # Context: last 20 lines of previous chunk (raw English)
        if i > 0:
            prev_start = max(chunks[i - 1][0], chunks[i - 1][1] - 20)
            context_before = "".join(lines[prev_start : chunks[i - 1][1]])
        else:
            context_before = ""

        # Context: first 10 lines of next chunk (raw English)
        if i < len(chunks) - 1:
            next_end = min(chunks[i + 1][0] + 10, chunks[i + 1][1])
            context_after = "".join(lines[chunks[i + 1][0] : next_end])
        else:
            context_after = ""

        chunk_info = {
            "index": i,
            "file": os.path.abspath(chunk_file),
            "output": os.path.abspath(ko_file),
            "start_line": start + 1,
            "end_line": end,
            "num_lines": end - start,
            "context_before": context_before,
            "context_after": context_after,
        }
        manifest["chunks"].append(chunk_info)

        print(f"  chunk_{i:02d}.md: lines {start + 1}-{end} ({end - start} lines)")

    manifest_path = os.path.join(args.output_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\nManifest written to {manifest_path}")
    print(f"Ready for translation: {len(chunks)} chunks")


if __name__ == "__main__":
    main()
