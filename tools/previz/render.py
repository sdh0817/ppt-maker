#!/usr/bin/env python3
"""Render the agentic-ai-60s previz video.

Usage:
    python3 tools/previz/render.py <output_dir>

Generates per-scene mp4s in <output_dir>/preview_clips/, then concats
them into <output_dir>/preview_v01.mp4.
"""
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from scenes_a import s01, s02, s03  # noqa: E402
from scenes_b import s04, s05, s06  # noqa: E402
from core import render_scene  # noqa: E402


SCENES = [
    ("S01", 4.0,  s01),
    ("S02", 10.0, s02),
    ("S03", 14.0, s03),
    ("S04", 14.0, s04),
    ("S05", 12.0, s05),
    ("S06", 6.0,  s06),
]


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: render.py <output_dir>\n")
        sys.exit(1)
    out_dir = Path(sys.argv[1]).expanduser().resolve()
    clips_dir = out_dir / "preview_clips"
    clips_dir.mkdir(parents=True, exist_ok=True)

    paths = []
    for sid, dur, fn in SCENES:
        print(f"[render] {sid} ({dur}s) ...", flush=True)
        p = render_scene(sid, dur, fn, clips_dir)
        paths.append(p)
        print(f"         -> {p}")

    # build concat list
    concat_file = clips_dir / "concat.txt"
    concat_file.write_text(
        "".join(f"file '{p.name}'\n" for p in paths),
        encoding="utf-8",
    )

    final = out_dir / "preview_v01.mp4"
    print(f"[concat] -> {final}")
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            str(final),
        ],
        check=True,
    )
    print(f"[done] {final}")


if __name__ == "__main__":
    main()
