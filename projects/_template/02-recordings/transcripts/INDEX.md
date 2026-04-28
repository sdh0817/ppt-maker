# Transcripts (Whisper Large v3)

`tools/transcribe.py` 가 생성한 전사 결과 모음.

## 명령

```bash
./tools/transcribe.py ../<녹음파일>.mp4 -o . -l ko
```

## 산출물

| 녹음 | 채택 take | txt | srt | json | 비고 |
|---|---|---|---|---|---|
| S01 | take02 | `S01_take02.txt` | `S01_take02.srt` | `S01_take02.json` | |

- `.txt` 스크립트와 비교용 (재녹음 필요 여부 판단)
- `.srt` 그대로 `06-output/`에 사용 가능
- `.json` `00-plan/edit-plan.md` 의 VO 컷 포인트 갱신에 사용
