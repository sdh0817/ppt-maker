#!/usr/bin/env python3
"""Add placeholder TTS narration to preview_v01.mp4.

Uses espeak-ng (offline, robotic but timing-accurate) to generate one
WAV per scene, pads/trims each to the scene's allotted duration, concats
into a full 60s track, then muxes onto the silent preview video.

Output: <project>/06-output/preview_v02_voiced.mp4
"""
import argparse
import subprocess
import sys
from pathlib import Path


# (scene_id, duration_seconds, plain text, espeak rate wpm)
SCRIPT = [
    ("S01", 4.0,
     "AI에게, 알아서 끝내줘, 라고 말할 수 있다면, 어떨까요?",
     150),
    ("S02", 10.0,
     "기존 AI는 답을 주는 도구였습니다. "
     "에이전틱 AI는 일을 끝내는 동료입니다. "
     "리서치하고, 초안을 쓰고, 메일을 보내고, 일정까지 잡습니다. 스스로요.",
     170),
    ("S03", 14.0,
     "원리는 단순합니다. "
     "계획하고, 실행하고, 결과를 확인한 뒤, 스스로 수정합니다. "
     "그리고 이걸 반복하죠. "
     "필요하면 웹을 검색하고, 코드를 짜고, 파일을 열고, 캘린더를 씁니다. 사람처럼요.",
     170),
    ("S04", 14.0,
     "그래서 무슨 일을 시킬 수 있냐면요. "
     "코드를 짜서 피알을 직접 올리고, "
     "자료를 모아 보고서까지 써냅니다. "
     "일정을 조율하고, 흩어진 데이터를, 그래프로 정리합니다. "
     "지금까지 사람 손이 가던 일을, 에이전트 하나가 끝내줍니다.",
     175),
    ("S05", 12.0,
     "가트너는 2028년까지, "
     "기업용 소프트웨어의 약 3분의 1이, "
     "에이전틱 AI를 탑재할 거라고 전망했어요. "
     "2024년엔 1퍼센트도 안 됐는데 말이죠.",
     170),
    ("S06", 6.0,
     "AI는 이제 쓰는 게 아니라, 맡기는 도구입니다. "
     "다음 편에선 에이전트를 직접 만들어보겠습니다.",
     170),
]


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def synth_scene(scene_id, text, rate, out_wav):
    run([
        "espeak-ng", "-v", "ko", "-s", str(rate), "-p", "45", "-a", "180",
        "-w", str(out_wav), text,
    ])


def probe_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def fit_to_duration(in_wav, out_wav, target_sec):
    """Pad with silence (front 0.15s, back fill) or speed up if overrun."""
    cur = probe_duration(in_wav)
    if cur > target_sec - 0.05:
        # speed up using atempo (max 2x per filter, chain if needed)
        factor = cur / (target_sec - 0.1)
        factor = min(factor, 1.6)  # don't squeeze too hard
        run([
            "ffmpeg", "-y", "-loglevel", "error", "-i", str(in_wav),
            "-filter:a", f"atempo={factor:.3f}",
            str(out_wav),
        ])
        cur = probe_duration(out_wav)
        src = out_wav
    else:
        src = in_wav

    pad = max(0.0, target_sec - cur - 0.15)
    final = out_wav.with_suffix(".final.wav")
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
        "-af",
        f"adelay=150|150,apad=pad_dur={pad}",
        "-t", f"{target_sec}",
        "-ar", "44100", "-ac", "2",
        str(final),
    ])
    final.replace(out_wav)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_output_dir",
                    help="e.g. projects/agentic-ai-60s/06-output")
    ap.add_argument("--in-video", default="preview_v01.mp4")
    ap.add_argument("--out-video", default="preview_v02_voiced.mp4")
    args = ap.parse_args()

    out_dir = Path(args.project_output_dir).expanduser().resolve()
    in_video = out_dir / args.in_video
    if not in_video.exists():
        sys.stderr.write(f"input video not found: {in_video}\n")
        sys.exit(1)

    voice_dir = out_dir / "preview_voice"
    voice_dir.mkdir(parents=True, exist_ok=True)

    fitted = []
    for sid, dur, text, rate in SCRIPT:
        raw = voice_dir / f"{sid}.raw.wav"
        fit = voice_dir / f"{sid}.wav"
        print(f"[tts] {sid} ({dur}s) rate={rate}")
        synth_scene(sid, text, rate, raw)
        d_raw = probe_duration(raw)
        print(f"      raw={d_raw:.2f}s -> fit to {dur:.2f}s")
        fit_to_duration(raw, fit, dur)
        fitted.append(fit)

    # concat all wavs
    concat_list = voice_dir / "concat.txt"
    concat_list.write_text(
        "".join(f"file '{p.name}'\n" for p in fitted), encoding="utf-8",
    )
    full_wav = voice_dir / "voice_full.wav"
    run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:a", "pcm_s16le", "-ar", "44100", "-ac", "2",
        str(full_wav),
    ])
    print(f"[mix] full voice = {probe_duration(full_wav):.2f}s")

    # mux audio onto silent video
    out_video = out_dir / args.out_video
    run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(in_video), "-i", str(full_wav),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        str(out_video),
    ])
    print(f"[done] {out_video}")


if __name__ == "__main__":
    main()
