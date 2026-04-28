# Output Versions

## 프리뷰 (음성 없음, 모션그래픽 애니매틱)

| 파일 | 길이 | 해상도 | 용도 |
|---|---|---|---|
| `preview_v01.mp4` | 60.0s | 540×960 | 신 타이밍/문구/기본 모션 확인용 |
| `preview_clips/SXX.mp4` | per-scene | 540×960 | 신별 디버깅 |
| `preview_thumbs/t_XXs.jpg` | — | 540×960 | 신별 정지 캡처 |

> 풀 모션그래픽 퀄리티가 아닌 **애니매틱**입니다 — 타이밍/배치/문구를
> 검증하는 용도. 실제 영상은 녹음 후 하이퍼프레임으로 마감합니다.

재생성:
```bash
python3 tools/previz/render.py projects/agentic-ai-60s/06-output
```

## 최종 렌더

| 버전 | 파일명 | 렌더일 | 길이 | 비고 |
|---|---|---|---|---|
| v01 | `agentic-ai-60s_v01.mp4` | YYYY-MM-DD | 60s | 1차 컷 |

자막: `agentic-ai-60s_v01.srt`, 썸네일: `agentic-ai-60s_v01_thumb.png`
