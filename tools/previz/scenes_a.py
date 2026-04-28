"""Scenes S01, S02, S03 frame functions."""
from PIL import ImageDraw
from core import (
    new_frame, font, draw_centered, text_size,
    W, H, GRAY, LIGHT, DIM, YELLOW, CYAN,
    ease_out, lerp,
)
import math


# ---------- S01 hook (4s) ----------
def s01(t):
    img = new_frame()
    d = ImageDraw.Draw(img)
    f_main = font(58)
    f_sub = font(34)
    f_yel = font(78)

    line1 = "AI에게,"
    chars = max(0, min(len(line1), int((t - 0.4) / 0.18)))
    typed = line1[:chars] if t >= 0.4 else ""
    if t < 1.6 and t >= 0.4 and (int(t * 4) % 2 == 0):
        typed = typed + "_"
    if typed:
        draw_centered(d, typed, 320, f_main, LIGHT)

    if t >= 1.6:
        # "알아서 끝내줘" drops in with bounce
        p = ease_out((t - 1.6) / 0.7)
        y = int(lerp(180, 430, p))
        bounce = int(8 * math.sin(min(p, 1.0) * math.pi))
        draw_centered(d, "“알아서 끝내줘”", y - bounce, f_yel, YELLOW)

    if t >= 2.6:
        a = ease_out(min((t - 2.6) / 0.6, 1.0))
        c = tuple(int(GRAY[i] * a) for i in range(3))
        draw_centered(d, "라고 말할 수 있다면?", 560, f_sub, c)

    return img


# ---------- S02 split compare (10s) ----------
def _chip(d, x, y, w, h, color, text=None, fnt=None, fill=None):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, outline=color, width=2,
                        fill=fill)
    if text and fnt:
        tw, th = text_size(d, text, fnt)
        d.text((x + (w - tw) // 2, y + (h - th) // 2 - 4), text, font=fnt, fill=color)


def s02(t):
    img = new_frame()
    d = ImageDraw.Draw(img)
    fl = font(28)
    fs = font(22, False)
    fc = font(36)

    # split line grows
    if t >= 0.0:
        p = ease_out(min(t / 0.5, 1.0))
        line_h = int(H * p)
        x = W // 2
        d.line([(x, (H - line_h) // 2), (x, (H + line_h) // 2)], fill=CYAN, width=2)

    # left side: 기존 AI
    if t >= 0.6:
        draw_centered_in(d, 0, W // 2, "기존 AI", 120, fl, GRAY)
    # bubbles on left
    if 1.0 <= t < 5.0:
        # user bubble (?)
        if t >= 1.0:
            _chip(d, 50, 250, 110, 60, GRAY, "?", fc, fill=(28, 28, 28))
        # bot bubble (!)
        if t >= 2.4:
            _chip(d, 110, 360, 110, 60, LIGHT, "!", fc, fill=(28, 28, 28))
    if t >= 4.2:
        a = min((t - 4.2) / 0.6, 1.0)
        c = tuple(int(GRAY[i] * a) for i in range(3))
        draw_centered_in(d, 0, W // 2, "→ 답을 준다", 540, fs, c)

    # right side: 에이전틱 AI
    if t >= 5.0:
        draw_centered_in(d, W // 2, W, "에이전틱 AI", 120, fl, YELLOW)
        # ?
        _chip(d, W // 2 + 30, 250, 110, 60, GRAY, "?", fc, fill=(28, 28, 28))
        # checklist
        items = ["리서치", "초안 작성", "메일 발송", "일정 등록"]
        for i, it in enumerate(items):
            row_t = 5.6 + i * 0.7
            if t >= row_t:
                yy = 350 + i * 50
                check = "☑" if t >= row_t + 0.15 else "☐"
                f_chk = font(26)
                d.text((W // 2 + 30, yy), f"{check}  {it}", font=f_chk,
                       fill=YELLOW if t >= row_t + 0.15 else GRAY)
    if t >= 8.8:
        a = min((t - 8.8) / 0.6, 1.0)
        c = tuple(int(YELLOW[i] * a) for i in range(3))
        draw_centered_in(d, W // 2, W, "→ 일을 끝낸다", 600, fs, c)

    return img


def draw_centered_in(d, x0, x1, text, y, fnt, color):
    w, _ = text_size(d, text, fnt)
    d.text((x0 + ((x1 - x0) - w) // 2, y), text, font=fnt, fill=color)


# ---------- S03 agent loop (14s) ----------
def s03(t):
    img = new_frame()
    d = ImageDraw.Draw(img)
    f_node = font(22)
    f_cap = font(20)
    f_center = font(34)
    f_tool = font(18, False)

    # caption top
    if t >= 0.4:
        a = min((t - 0.4) / 0.6, 1.0)
        c = tuple(int(CYAN[i] * a) for i in range(3))
        draw_centered(d, "Agentic AI Loop", 110, f_cap, c)

    cx, cy = W // 2, H // 2 + 40
    R = 170
    nodes = [
        ("계획", -90),  # top
        ("실행", 0),    # right
        ("확인", 90),   # bottom
        ("개선", 180),  # left
    ]
    # node pop-in
    for i, (label, deg) in enumerate(nodes):
        appear = 0.2 + i * 0.2
        if t < appear:
            continue
        ax = cx + R * math.cos(math.radians(deg))
        ay = cy + R * math.sin(math.radians(deg))
        # decide if "lit" by rotating arrow position
        loop_t = (t - 1.5)
        lit = False
        if loop_t > 0:
            # arrow goes around once over 5.5s
            angle = (loop_t / 5.5) * 360 - 90
            # lit if arrow is near this node
            cur_idx = int(((angle + 90) % 360) // 90)
            if cur_idx == i and loop_t < 5.5 + 0.5:
                lit = True
        col = YELLOW if lit else LIGHT
        size = 70
        d.rounded_rectangle(
            [ax - size, ay - size // 2, ax + size, ay + size // 2],
            radius=14, outline=col, width=3, fill=(20, 20, 20),
        )
        tw, th = text_size(d, label, f_node)
        d.text((ax - tw // 2, ay - th // 2 - 3), label, font=f_node, fill=col)

    # rotating arrow
    if t >= 1.5 and t <= 7.0:
        loop_t = t - 1.5
        angle = (loop_t / 5.5) * 360 - 90
        ax = cx + (R - 90) * math.cos(math.radians(angle))
        ay = cy + (R - 90) * math.sin(math.radians(angle))
        d.ellipse([ax - 10, ay - 10, ax + 10, ay + 10], fill=CYAN)

    # center 반복 pulse
    if t >= 7.0:
        pulse = 1.0 + 0.08 * math.sin((t - 7.0) * 6.0)
        size = int(36 * pulse)
        f_p = font(size)
        draw_centered(d, "반복", cy - 20, f_p, CYAN)

    # tool icons orbiting (small dots with labels)
    if t >= 9.0:
        tools = ["Web", "Code", "Files", "Calendar"]
        for i, name in enumerate(tools):
            ang = ((t - 9.0) * 60 + i * 90) % 360
            r = 90
            tx = cx + r * math.cos(math.radians(ang))
            ty = cy + r * math.sin(math.radians(ang)) + 30
            d.ellipse([tx - 22, ty - 14, tx + 22, ty + 14], outline=CYAN, width=1,
                      fill=(20, 20, 20))
            tw, _ = text_size(d, name, f_tool)
            d.text((tx - tw // 2, ty - 9), name, font=f_tool, fill=CYAN)

    return img
