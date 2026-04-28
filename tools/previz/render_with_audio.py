#!/usr/bin/env python3
"""Render previz with user's recorded audio.

Uses scene boundaries to (1) slice the user's m4a into 6 per-scene WAVs,
(2) re-render the previz video with each scene stretched to match the
user's natural pace, (3) mux real audio onto the new video.

Output: <project>/06-output/preview_v03_voiced.mp4
"""
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from scenes_a import s01, s02, s03  # noqa: E402
from scenes_b import s04, s05, s06  # noqa: E402
from core import render_scene  # noqa: E402


# (scene_id, start_sec, end_sec, frame_func)
SCENES = [
    ("S01", 0.0,  9.1,  s01),
    ("S02", 9.1,  21.5, s02),
    ("S03", 21.5, 40.5, s03),
    ("S04", 40.5, 59.4, s04),
    ("S05", 59.4, 74.5, s05),
    ("S06", 74.5, 83.8, s06),
]


def run(cmd):
    return subprocess.run(cmd, check=True)


def slice_audio(in_audio, start, end, out_wav):
    run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(in_audio),
        "-ss", f"{start}", "-to", f"{end}",
        "-ar", "44100", "-ac", "2",
        "-c:a", "pcm_s16le",
        str(out_wav),
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_output_dir",
                    help="e.g. projects/agentic-ai-60s/06-output")
    ap.add_argument("--audio", required=True,
                    help="path to recording (m4a/wav/mp4 etc.)")
    ap.add_argument("--out-video", default="preview_v03_voiced.mp4")
    args = ap.parse_args()

    out_dir = Path(args.project_output_dir).expanduser().resolve()
    audio_in = Path(args.audio).expanduser().resolve()
    if not audio_in.exists():
        sys.stderr.write(f"audio not found: {audio_in}\n")
        sys.exit(1)

    clips_dir = out_dir / "preview_clips_v03"
    clips_dir.mkdir(parents=True, exist_ok=True)
    voice_dir = out_dir / "preview_voice_v03"
    voice_dir.mkdir(parents=True, exist_ok=True)

    video_paths = []
    audio_paths = []
    for sid, start, end, fn in SCENES:
        dur = end - start
        print(f"[{sid}] {start:.2f}-{end:.2f} ({dur:.2f}s)")
        # render video at this duration
        v = render_scene(sid, dur, fn, clips_dir)
        video_paths.append(v)
        # slice audio
        a = voice_dir / f"{sid}.wav"
        slice_audio(audio_in, start, end, a)
        audio_paths.append(a)

    # concat scene videos
    v_list = clips_dir / "concat.txt"
    v_list.write_text(
        "".join(f"file '{p.name}'\n" for p in video_paths), encoding="utf-8",
    )
    final_v = clips_dir / "_video.mp4"
    run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(v_list),
        "-c", "copy", str(final_v),
    ])

    # concat audio
    a_list = voice_dir / "concat.txt"
    a_list.write_text(
        "".join(f"file '{p.name}'\n" for p in audio_paths), encoding="utf-8",
    )
    final_a = voice_dir / "_voice.wav"
    run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(a_list),
        "-c:a", "pcm_s16le", "-ar", "44100", "-ac", "2",
        str(final_a),
    ])

    # mux
    out = out_dir / args.out_video
    run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(final_v), "-i", str(final_a),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
        "-shortest",
        str(out),
    ])
    print(f"[done] {out}")


if __name__ == "__main__":
    main()
