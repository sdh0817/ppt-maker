"""Previz core helpers: canvas, fonts, easing, render+encode pipeline."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess

W, H = 540, 960
FPS = 24
BG = (10, 10, 10)
GRAY = (160, 160, 160)
LIGHT = (220, 220, 220)
DIM = (90, 90, 90)
YELLOW = (255, 208, 0)
CYAN = (0, 224, 255)

KR_FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
KR_REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"


def font(size, bold=True):
    return ImageFont.truetype(KR_FONT if bold else KR_REG, size)


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_in(t):
    t = max(0.0, min(1.0, t))
    return t ** 3


def text_size(d, text, fnt):
    b = d.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0], b[3] - b[1]


def draw_centered(d, text, y, fnt, color):
    w, _ = text_size(d, text, fnt)
    d.text(((W - w) // 2, y), text, font=fnt, fill=color)


def new_frame():
    return Image.new("RGB", (W, H), BG)


def render_scene(scene_id, duration, frame_func, out_dir):
    """frame_func(t_seconds) -> PIL.Image. Returns path to encoded mp4."""
    out_dir = Path(out_dir)
    tmp = out_dir / "_frames" / scene_id
    tmp.mkdir(parents=True, exist_ok=True)
    n = int(round(duration * FPS))
    for i in range(n):
        t = i / FPS
        img = frame_func(t)
        img.save(tmp / f"f{i:04d}.jpg", quality=85)
    out = out_dir / f"{scene_id}.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-framerate", str(FPS),
            "-i", str(tmp / "f%04d.jpg"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-r", "30",
            str(out),
        ],
        check=True,
    )
    return out


def lerp(a, b, t):
    return a + (b - a) * t
