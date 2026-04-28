#!/usr/bin/env python3
"""Whisper Large v3 로 MP4/오디오를 전사합니다.

사용법:
  ./tools/transcribe.py <input.mp4> [-o <output_dir>] [-l ko]

기본 출력 (입력 파일 폴더에 동일 stem 으로):
  <stem>.txt   전체 텍스트
  <stem>.srt   자막 (편집/업로드용)
  <stem>.json  단어 단위 타임스탬프 + 세그먼트 메타

예:
  ./tools/transcribe.py projects/intro/02-recordings/S01_take02.mp4 \\
      -o projects/intro/02-recordings/transcripts
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from faster_whisper import WhisperModel
except ImportError:
    sys.stderr.write(
        "faster-whisper 가 설치되어 있지 않습니다. 다음을 실행하세요:\n"
        "  pip install -r tools/requirements.txt\n"
    )
    sys.exit(1)


def format_srt_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds - h * 3600 - m * 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def main() -> int:
    parser = argparse.ArgumentParser(description="Whisper Large v3 transcriber")
    parser.add_argument("input", help="audio/video file path (mp4/wav/m4a 등)")
    parser.add_argument("-o", "--output-dir",
                        help="출력 폴더 (기본: 입력 파일과 동일 폴더)")
    parser.add_argument("-l", "--language", default="ko",
                        help="언어 코드 (기본: ko)")
    parser.add_argument("--device", default="auto",
                        choices=["auto", "cpu", "cuda"],
                        help="실행 디바이스 (기본: auto)")
    parser.add_argument("--compute-type", default="default",
                        help="default / float16 / int8 / int8_float16 등")
    parser.add_argument("--initial-prompt", default=None,
                        help="도메인 용어 힌트 (예: '하이퍼프레임, 모션 그래픽')")
    args = parser.parse_args()

    in_path = Path(args.input).expanduser().resolve()
    if not in_path.exists():
        sys.stderr.write(f"입력 파일을 찾을 수 없습니다: {in_path}\n")
        return 1

    out_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir else in_path.parent
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = in_path.stem

    print(f"[load] Whisper large-v3  device={args.device}  compute={args.compute_type}")
    model = WhisperModel(
        "large-v3",
        device=args.device,
        compute_type=args.compute_type,
    )

    print(f"[transcribe] {in_path}  lang={args.language}")
    segments, info = model.transcribe(
        str(in_path),
        language=args.language,
        word_timestamps=True,
        vad_filter=True,
        initial_prompt=args.initial_prompt,
    )

    full_text: list[str] = []
    srt_lines: list[str] = []
    json_segments: list[dict] = []

    for i, seg in enumerate(segments, start=1):
        text = seg.text.strip()
        full_text.append(text)

        srt_lines.append(str(i))
        srt_lines.append(
            f"{format_srt_timestamp(seg.start)} --> {format_srt_timestamp(seg.end)}"
        )
        srt_lines.append(text)
        srt_lines.append("")

        json_segments.append({
            "id": i,
            "start": seg.start,
            "end": seg.end,
            "text": text,
            "words": [
                {
                    "start": w.start,
                    "end": w.end,
                    "word": w.word,
                    "probability": w.probability,
                }
                for w in (seg.words or [])
            ],
        })
        print(
            f"  [{format_srt_timestamp(seg.start)} -> "
            f"{format_srt_timestamp(seg.end)}] {text}"
        )

    txt_path = out_dir / f"{stem}.txt"
    srt_path = out_dir / f"{stem}.srt"
    json_path = out_dir / f"{stem}.json"

    txt_path.write_text("\n".join(full_text) + "\n", encoding="utf-8")
    srt_path.write_text("\n".join(srt_lines), encoding="utf-8")
    json_path.write_text(
        json.dumps(
            {
                "model": "whisper-large-v3",
                "source": str(in_path),
                "language": info.language,
                "language_probability": info.language_probability,
                "duration": info.duration,
                "segments": json_segments,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print(f"[done] {txt_path}")
    print(f"[done] {srt_path}")
    print(f"[done] {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
