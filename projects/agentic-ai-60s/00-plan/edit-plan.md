# Edit Plan — 에이전틱 AI, 60초 안에 이해하기

> 이 문서는 편집 단계의 정답지입니다. 편집 중 변경이 필요하면
> 먼저 이 문서를 갱신한 뒤 하이퍼프레임에 반영하세요.

## 트랙 레이아웃 (표준)

| 트랙 | 용도 |
|---|---|
| V4 | 자막 (캡션) — 9:16 하단 22% |
| V3 | 라벨/오버레이 텍스트, 출처 표기 |
| V2 | 메인 모션 비주얼 (`04-motion-assets/`) |
| V1 | 배경 (검정 #0A0A0A 정지) |
| A3 | SFX |
| A2 | BGM (-22 LUFS) |
| A1 | VO (-16 LUFS, 노이즈 제거 후) |

전 신 공통: V1 = `bg_black.png` 정지, A2 BGM = `bgm_minimal_loop.wav` 60초 풀 길이

---

## S01 — 00:00–00:04 — 후킹

- **V1** `bg_black.png`
- **V2** `04-motion-assets/S01-C01_hook-typewriter.mp4` 00:00.0–00:04.0
- **V3** —
- **V4 자막** 없음 (메인 타이포가 텍스트 역할)
- **A1 VO** `02-recordings/S01_takeXX.mp4` (실제 take 채택 후 갱신) — 컷: 발화 시작–00:03.7
- **A2 BGM** -22dB, 00:00.0부터 페이드 인 (8f)
- **A3 SFX**
  - `sfx_typewriter.wav` @ 00:00.4 (loop 1.0s, 게이트 -3dB)
  - `sfx_whoosh_drop.wav` @ 00:01.6
- **트랜지션 OUT** `WHIP:4f` → S02

## S02 — 00:04–00:14 — 기존 AI vs 에이전틱 AI

- **V1** `bg_black.png`
- **V2**
  - `04-motion-assets/S02-C01_split-line.mp4` 00:04.0–00:04.5 (분할선 등장)
  - `04-motion-assets/S02-C02_old-ai-bubble.mp4` 00:04.5–00:09.0 (좌측, 좌측 절반에만 마스크)
  - `04-motion-assets/S02-C03_agentic-checklist.mp4` 00:09.0–00:13.5 (우측, 우측 절반 마스크)
- **V3 오버레이**
  - 라벨 `기존 AI` (회색 #A0A0A0) — 좌상단 패널 안, 00:04.5–00:09.0
  - 라벨 `에이전틱 AI` (옐로우 #FFD000) — 우상단 패널 안, 00:09.0–00:13.5
  - 캡션 `→ 답을 준다` 좌하단, 00:08.0–00:09.0
  - 캡션 `→ 일을 끝낸다` 우하단, 00:12.5–00:13.5
- **V4 자막** 스크립트 자동 + 수동 보정
- **A1 VO** `02-recordings/S02_takeXX.mp4`
- **A2 BGM** continued
- **A3 SFX**
  - `sfx_slide_in.wav` @ 00:04.0
  - `sfx_pop_bubble.wav` @ 00:05.0, 00:06.5 (좌측 말풍선 2회)
  - `sfx_pop_bubble.wav` @ 00:09.5 (우측 사용자 ?)
  - `sfx_tick.wav` ×4 @ 00:10.5, 00:11.2, 00:11.9, 00:12.6 (체크리스트)
- **트랜지션 OUT** `DISS:8f`

## S03 — 00:14–00:28 — 에이전트 루프

- **V1** `bg_black.png`
- **V2** `04-motion-assets/S03-C01_agent-loop.mp4` 00:14.0–00:28.0 (단일 클립, 14초)
  - 내부 키프레임: 00:14.0 노드 4개 등장 / 00:15.5 화살표 회전 시작 / 00:21.0 한 바퀴 완성 / 00:23.0 도구 아이콘 궤도 등장
- **V3 오버레이**
  - 캡션 `Agentic AI Loop` 상단, 00:14.5–00:27.5 (시안 #00E0FF)
  - 한국어 노드 라벨: `생각`, `행동`, `확인`, `개선` — 각 노드 점등 타이밍에 0.3s 페이드 인
- **V4 자막** 스크립트
- **A1 VO** `02-recordings/S03_takeXX.mp4`
- **A2 BGM** continued
- **A3 SFX**
  - `sfx_node_pop.wav` ×4 @ 00:14.2, 00:14.4, 00:14.6, 00:14.8
  - `sfx_swoosh_loop.wav` @ 00:15.5–00:21.0 (라이트 게이트)
  - `sfx_chime_complete.wav` @ 00:21.0
- **트랜지션 OUT** `PUSH-L:6f`

## S04 — 00:28–00:42 — 사용 사례 2×2 그리드

- **V1** `bg_black.png`
- **V2**
  - `04-motion-assets/S04-C01_grid-frame.mp4` 00:28.0–00:28.5 (그리드 라인 등장)
  - `04-motion-assets/S04-C02_card-code.mp4` 00:28.5–00:38.0 (좌-위 카드)
  - `04-motion-assets/S04-C03_card-research.mp4` 00:28.9–00:38.0 (우-위 카드)
  - `04-motion-assets/S04-C04_card-calendar.mp4` 00:29.3–00:38.0 (좌-아래)
  - `04-motion-assets/S04-C05_card-data-viz.mp4` 00:29.7–00:38.0 (우-아래)
  - `04-motion-assets/S04-C06_grid-pulse-connect.mp4` 00:38.0–00:42.0 (4카드 연결+펄스)
- **V3 오버레이**
  - 카드 라벨: `코드`, `리서치`, `일정`, `데이터` — 각 카드 등장 +0.2s 후 페이드 인
  - 가운데 캡션 `한 명의 에이전트가` 00:40.0–00:42.0 페이드 (옐로우)
- **V4 자막** 스크립트
- **A1 VO** `02-recordings/S04_takeXX.mp4`
- **A2 BGM** continued
- **A3 SFX**
  - `sfx_card_slide.wav` @ 00:28.5, 00:28.9, 00:29.3, 00:29.7
  - `sfx_complete_chime.wav` @ 00:38.0
- **트랜지션 OUT** `DISS:8f`

## S05 — 00:42–00:54 — Gartner 33% 빅넘버

- **V1** `bg_black.png`
- **V2**
  - `04-motion-assets/S05-C01_counter-0-to-33.mp4` 00:42.0–00:45.0 (카운트업)
  - `04-motion-assets/S05-C02_caption-context.mp4` 00:45.0–00:47.5 (메인 캡션 페이드)
  - `04-motion-assets/S05-C03_bar-2024-vs-2028.mp4` 00:47.5–00:53.0 (막대 차트 성장)
- **V3 오버레이**
  - 메인 캡션 `2028년까지 기업용 SW의 약 1/3이 에이전틱 AI 탑재` 00:45.0–00:53.5
  - 보조 캡션 `일상 업무 결정의 15% 이상 자율화 (2028)` 00:51.5–00:53.5 (작게)
  - 출처 `Source: Gartner, 2024` 우하단 8pt 회색 00:45.0–00:54.0
- **V4 자막** 스크립트
- **A1 VO** `02-recordings/S05_takeXX.mp4`
- **A2 BGM** +2dB 강조 @ 00:42.0–00:53.0 (자동화 페이드)
- **A3 SFX**
  - `sfx_number_tick.wav` @ 00:43.0–00:44.5 (카운트업 동안 짧게 반복)
  - `sfx_bar_grow.wav` @ 00:48.0
- **트랜지션 OUT** `FADE-K:12f` (검은 화면 페이드)

## S06 — 00:54–01:00 — 결론 + CTA

- **V1** `bg_black.png`
- **V2** `04-motion-assets/S06-C01_outro-write-vs-delegate.mp4` 00:54.0–01:00.0
- **V3 오버레이**
  - `다음 편 — 직접 만들어보는 AI 에이전트` 00:58.0–00:59.5
  - 구독 아이콘 + `구독 / 저장` 우하단 펄스 00:59.0–01:00.0
- **V4 자막** 없음
- **A1 VO** `02-recordings/S06_takeXX.mp4`
- **A2 BGM** -3dB 페이드 아웃 @ 00:58.0–01:00.0
- **A3 SFX** `sfx_soft_chime.wav` @ 00:55.5
- **트랜지션 OUT** `FADE-K:24f` (엔드 페이드)

---

## 모션 에셋 체크리스트 (`04-motion-assets/`)

| 파일명 | 신/컷 | 길이 | 스타일 | 핵심 동작 |
|---|---|---|---|---|
| `S01-C01_hook-typewriter.mp4` | S01 | 4.0s | KT | 타이프라이터 + 옐로우 강조 단어 드롭 |
| `S02-C01_split-line.mp4` | S02 | 0.5s | AB | 시안 분할선 등장 |
| `S02-C02_old-ai-bubble.mp4` | S02 | 4.5s | AB | ?·! 챗 버블 왕복 |
| `S02-C03_agentic-checklist.mp4` | S02 | 4.5s | UI | 자동 체크 + 사이드 윈도우 팝 |
| `S03-C01_agent-loop.mp4` | S03 | 14.0s | AB | 4-노드 회전 + 도구 궤도 |
| `S04-C01_grid-frame.mp4` | S04 | 0.5s | AB | 4분할 그리드 라인 |
| `S04-C02_card-code.mp4` | S04 | 9.5s | UI | 터미널 + GH PR ✓ |
| `S04-C03_card-research.mp4` | S04 | 9.1s | UI | 탭 3개 → PDF |
| `S04-C04_card-calendar.mp4` | S04 | 8.7s | UI | 캘린더 슬롯 ✓ |
| `S04-C05_card-data-viz.mp4` | S04 | 8.3s | UI | 표 → 막대그래프 모핑 |
| `S04-C06_grid-pulse-connect.mp4` | S04 | 4.0s | AB | 카드 연결 + 펄스 |
| `S05-C01_counter-0-to-33.mp4` | S05 | 3.0s | KT | 0→33 카운트업 + 글로우 |
| `S05-C02_caption-context.mp4` | S05 | 2.5s | KT | 본문 캡션 페이드 |
| `S05-C03_bar-2024-vs-2028.mp4` | S05 | 5.5s | AB | 비교 막대 성장 |
| `S06-C01_outro-write-vs-delegate.mp4` | S06 | 6.0s | KT | "쓰는→맡기는" 키워드 잔류 |

## 렌더 설정

- 코덱: H.264, 12,000 kbps (Shorts 권장)
- 해상도: 1080×1920 (9:16), 30fps
- 음성 LUFS: VO -16, BGM -22, SFX -20 (피크 -3dB 미만)
- 자막: Pretendard Bold 64pt, 흰색 + 검정 외곽선 4px, 하단 22%
- 색공간: Rec.709
- 안전 영역: 위/아래 12% (UI 오버레이 회피)

## 변경 이력

| 날짜 | 변경 내용 | 이유 |
|---|---|---|
| 2026-04-28 | 초안 작성 | — |
