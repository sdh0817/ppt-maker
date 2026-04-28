# Output Versions

## 프리뷰 (애니매틱)

| 파일 | 길이 | 음성 | 용도 |
|---|---|---|---|
| `preview_v01.mp4` | 60.0s | 없음 | 1차 — 모션 타이밍 확인 |
| `preview_v02_voiced.mp4` | 60.0s | espeak-ng (placeholder, 로보틱) | 2차 — 보류 (음질 낮음) |
| **`preview_v03_voiced.mp4`** | 83.8s | 사용자 실음성 | **3차 — 사용자 페이스에 맞춰 영상 재렌더 + 실음성 muxing** |

> 풀 모션그래픽 퀄리티가 아닌 **애니매틱**입니다. 실제 영상은 하이퍼프레임으로 마감.

### 신 길이 (v03 기준 — 사용자 녹음 페이스)

| 신 | 시작 | 끝 | 길이 | 원래 기획 |
|---|---|---|---|---|
| S01 | 0.0  |  9.1  |  9.1s | 4s |
| S02 | 9.1  | 21.5  | 12.4s | 10s |
| S03 | 21.5 | 40.5  | 19.0s | 14s |
| S04 | 40.5 | 59.4  | 18.9s | 14s |
| S05 | 59.4 | 74.5  | 15.1s | 12s |
| S06 | 74.5 | 83.8  |  9.3s | 6s |

### 재생성

```bash
# 음성 없는 v01 (60s 원래 기획 기준)
python3 tools/previz/render.py projects/agentic-ai-60s/06-output

# 사용자 음성 + 페이스에 맞춘 v03
python3 tools/previz/render_with_audio.py projects/agentic-ai-60s/06-output \
    --audio "projects/agentic-ai-60s/02-recordings/녹음 (4).m4a"
```

## 최종 렌더 (하이퍼프레임 출력)

| 버전 | 파일명 | 렌더일 | 길이 | 비고 |
|---|---|---|---|---|
| v01 | `agentic-ai-60s_v01.mp4` | YYYY-MM-DD | 60s | 1차 컷 |

자막: `agentic-ai-60s_v01.srt`, 썸네일: `agentic-ai-60s_v01_thumb.png`
