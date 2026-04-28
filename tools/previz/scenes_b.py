"""Scenes S04, S05, S06 frame functions."""
from PIL import ImageDraw
from core import (
    new_frame, font, draw_centered, text_size,
    W, H, GRAY, LIGHT, DIM, YELLOW, CYAN,
    ease_out, lerp,
)
import math


def _card(d, x, y, w, h, label, label_color):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, outline=GRAY, width=2,
                        fill=(20, 20, 20))
    f_lbl = font(18, False)
    tw, _ = text_size(d, label, f_lbl)
    d.text((x + w // 2 - tw // 2, y + 10), label, font=f_lbl, fill=label_color)


# ---------- S04 use-case 2x2 grid (14s) ----------
def s04(t):
    img = new_frame()
    d = ImageDraw.Draw(img)
    f_demo = font(16, False)
    f_cap = font(28)

    # grid frame appears
    if t >= 0.0:
        p = ease_out(min(t / 0.5, 1.0))
        # outer
        margin = 30
        gx0, gy0 = margin, 200
        gx1, gy1 = W - margin, H - 220
        d.line([(gx0, gy0), (gx0 + (gx1 - gx0) * p, gy0)], fill=DIM, width=1)
        d.line([(gx0, gy1), (gx0 + (gx1 - gx0) * p, gy1)], fill=DIM, width=1)
        d.line([(gx0, gy0), (gx0, gy0 + (gy1 - gy0) * p)], fill=DIM, width=1)
        d.line([(gx1, gy0), (gx1, gy0 + (gy1 - gy0) * p)], fill=DIM, width=1)

    margin = 30
    gx0, gy0 = margin, 200
    gx1, gy1 = W - margin, H - 220
    cw = (gx1 - gx0) // 2 - 8
    ch = (gy1 - gy0) // 2 - 8
    cards = [
        ("코드", gx0, gy0),
        ("리서치", gx0 + cw + 16, gy0),
        ("일정", gx0, gy0 + ch + 16),
        ("데이터", gx0 + cw + 16, gy0 + ch + 16),
    ]
    appear = [0.5, 0.9, 1.3, 1.7]

    for i, (lbl, x, y) in enumerate(cards):
        if t < appear[i]:
            continue
        # slide in from below
        p = ease_out(min((t - appear[i]) / 0.4, 1.0))
        oy = int(lerp(40, 0, p))
        _card(d, x, y + oy, cw, ch, lbl, YELLOW)

        # demos start after card lands
        d_t = t - appear[i] - 0.4
        if d_t < 0:
            continue
        cx, cy = x + cw // 2, y + oy + ch // 2

        if i == 0:  # 코드: terminal lines + ✓
            for k in range(3):
                if d_t > 0.3 + k * 0.4:
                    d.text((x + 14, y + oy + 38 + k * 18), f"$ run task {k+1}",
                           font=f_demo, fill=LIGHT)
            if d_t > 1.8:
                d.text((x + cw - 36, y + oy + ch - 28), "PR ✓",
                       font=f_demo, fill=YELLOW)
        elif i == 1:  # 리서치: 3 tabs → doc
            for k in range(3):
                if d_t > 0.2 + k * 0.3 and d_t < 2.4:
                    tx = x + 14 + k * 28
                    ty = y + oy + 40
                    d.rectangle([tx, ty, tx + 22, ty + 16], outline=LIGHT, width=1)
            if d_t > 2.4:
                d.text((x + cw // 2 - 14, y + oy + ch - 32), "PDF",
                       font=f_demo, fill=YELLOW)
        elif i == 2:  # 일정: cal grid + ✓
            # mini calendar
            for r in range(3):
                for c in range(4):
                    cx2 = x + 14 + c * 28
                    cy2 = y + oy + 40 + r * 24
                    d.rectangle([cx2, cy2, cx2 + 22, cy2 + 18], outline=DIM, width=1)
            if d_t > 1.0:
                d.rectangle([x + 14 + 56, y + oy + 40 + 24,
                             x + 14 + 56 + 22, y + oy + 40 + 24 + 18],
                            outline=YELLOW, width=2, fill=(60, 50, 0))
                d.text((x + 14 + 60, y + oy + 40 + 24 + 2), "✓",
                       font=f_demo, fill=YELLOW)
        elif i == 3:  # 데이터: bars grow
            for k in range(4):
                if d_t > 0.3 + k * 0.25:
                    bp = ease_out(min((d_t - 0.3 - k * 0.25) / 0.6, 1.0))
                    bh = int(lerp(2, 50 + k * 6, bp))
                    bx = x + 18 + k * 22
                    by = y + oy + ch - 18
                    d.rectangle([bx, by - bh, bx + 14, by], fill=YELLOW)

    # 4 cards all appeared → connect lines + caption
    if t >= 9.5:
        a = min((t - 9.5) / 0.5, 1.0)
        c = tuple(int(YELLOW[i] * a) for i in range(3))
        draw_centered(d, "한 명의 에이전트가", H - 140, f_cap, c)

    return img


# ---------- S05 Gartner stat (12s) ----------
def s05(t):
    img = new_frame()
    d = ImageDraw.Draw(img)
    f_huge = font(180)
    f_cap = font(22)
    f_sm = font(16, False)
    f_year = font(20)

    # 0% → 33% counter (t 0.0–3.0)
    if t < 5.5:
        p = ease_out(min(t / 2.0, 1.0)) if t < 2.0 else 1.0
        val = int(lerp(0, 33, p))
        text = f"{val}%"
        # glow at end
        color = YELLOW
        draw_centered(d, text, 280, f_huge, color)

    # caption
    if t >= 2.5:
        a = min((t - 2.5) / 0.6, 1.0)
        col = tuple(int(LIGHT[i] * a) for i in range(3))
        draw_centered(d, "2028년까지 기업용 SW의 약 1/3이", 360, f_cap, col)
        draw_centered(d, "에이전틱 AI를 탑재", 395, f_cap, col)

    # bars 2024 vs 2028
    if t >= 5.5:
        # show "33%" smaller at top
        f_top = font(60)
        draw_centered(d, "33%", 240, f_top, YELLOW)
        # bar chart
        base_y = H - 220
        bx_left = 130
        bx_right = W - 130 - 70
        bw = 70
        # 2024 bar (~1%)
        p24 = ease_out(min((t - 5.7) / 0.8, 1.0))
        h24 = max(2, int(2 * p24))
        d.rectangle([bx_left, base_y - h24, bx_left + bw, base_y], fill=GRAY)
        d.text((bx_left + 6, base_y + 10), "2024", font=f_year, fill=GRAY)
        # 2028 bar (33%)
        p28 = ease_out(min((t - 6.0) / 1.6, 1.0))
        h28 = int(lerp(2, 280, p28))
        d.rectangle([bx_right, base_y - h28, bx_right + bw, base_y], fill=YELLOW)
        d.text((bx_right + 6, base_y + 10), "2028", font=f_year, fill=YELLOW)
        # axis
        d.line([(80, base_y), (W - 80, base_y)], fill=DIM, width=1)

    # bottom small caption
    if t >= 9.5:
        a = min((t - 9.5) / 0.6, 1.0)
        col = tuple(int(GRAY[i] * a) for i in range(3))
        draw_centered(d, "결정의 15%+ 자율화 (2028)", H - 90, f_sm, col)

    # source bottom-right
    if t >= 2.8:
        d.text((W - 200, H - 40), "Source: Gartner, 2024", font=f_sm, fill=DIM)

    return img


# ---------- S06 outro (6s) ----------
def s06(t):
    img = new_frame()
    d = ImageDraw.Draw(img)
    f_main = font(36)
    f_yel = font(72)
    f_tease = font(24)
    f_sub = font(18, False)

    if t < 4.0:
        if t >= 0.0:
            a = min(t / 0.6, 1.0)
            c = tuple(int(LIGHT[i] * a) for i in range(3))
            draw_centered(d, "이제 AI는 “쓰는” 게 아니라", 380, f_main, c)
        if t >= 1.5:
            a = min((t - 1.5) / 0.5, 1.0)
            c = tuple(int(YELLOW[i] * a) for i in range(3))
            draw_centered(d, "“맡기는” 것", 460, f_yel, c)
    else:
        # remain just keywords
        draw_centered(d, "“쓰는”  →  “맡기는”", 360, f_main, LIGHT)
        if t >= 4.0:
            a = min((t - 4.0) / 0.5, 1.0)
            c = tuple(int(LIGHT[i] * a) for i in range(3))
            draw_centered(d, "다음 편 — 직접 만들어보는 AI 에이전트",
                          540, f_tease, c)
        if t >= 5.0:
            pulse = 1.0 + 0.06 * math.sin((t - 5.0) * 8.0)
            sz = int(20 * pulse)
            f_cta = font(sz, False)
            draw_centered(d, "▶  구독 / 저장", H - 100, f_cta, YELLOW)

    return img
