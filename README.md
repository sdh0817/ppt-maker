# ppt-maker

하이퍼프레임(HyperFrame) 기반 모션 애니메이션 영상 제작 워크스페이스.
얼굴 노출 없이, 사용자가 녹음한 음성을 기반으로 모션/타이포/일러스트 애니메이션
영상을 제작하기 위한 다중 프로젝트 관리 저장소입니다.

## 작업 흐름 (한 프로젝트 기준)

각 프로젝트는 다음 7단계를 순서대로 거칩니다. 폴더 번호는 단계와 1:1 매칭됩니다.

| 단계 | 폴더 | 담당 | 산출물 |
|---|---|---|---|
| 0. 기획 | `00-plan/` | Claude (지시받아) | `concept.md`, `storyboard.md`, `edit-plan.md` |
| 1. 스크립트 | `01-script/` | Claude | `script.md` (낭독용 본문 + 호흡 표시) |
| 2. 음성 녹음 | `02-recordings/` | 사용자 | `*.mp4` (낭독 녹음) + `INDEX.md` |
| 3. 원본 영상 | `03-source/` | 사용자 | `*.mp4` (참고/소스 영상) + `INDEX.md` |
| 4. 모션 에셋 | `04-motion-assets/` | Claude/툴 | 얼굴 없는 모션 애니메이션 클립, 일러스트 |
| 5. 편집 | `05-edit/` | 하이퍼프레임 | 하이퍼프레임 프로젝트 파일, 트랙 노트 |
| 6. 출력 | `06-output/` | 렌더 | 최종 `*.mp4`, 썸네일, 자막 |

> 기획(0)에서 **각 신이 어느 타임코드에 어떤 트랙으로 들어가는지** 까지
> 모두 명시한 뒤에 다음 단계로 넘어갑니다. 편집 단계에서 즉흥적으로
> 결정하지 않습니다.

## 폴더 구조

```
ppt-maker/
├── README.md                  # 본 문서
├── docs/
│   ├── workflow.md            # 단계별 상세 작업 절차
│   ├── hyperframe-conventions.md  # 트랙/네이밍 규칙
│   └── motion-style-guide.md  # 얼굴 없는 모션 스타일 가이드
├── projects/                  # 모든 개별 프로젝트
│   ├── _template/             # 새 프로젝트 시드(복사 원본)
│   └── <project-slug>/        # 실제 프로젝트들
├── shared/
│   ├── motion-presets/        # 재사용 모션/트랜지션 프리셋
│   └── brand/                 # 로고/폰트/컬러 등 공용 자산
└── tools/
    └── new-project.sh         # 새 프로젝트 부트스트랩
```

## 새 프로젝트 시작

```bash
./tools/new-project.sh "프로젝트-슬러그" "프로젝트 한국어 제목"
```

이 명령은 `projects/_template/`을 복사하여
`projects/프로젝트-슬러그/`를 만들고 `meta.yaml`에 제목/생성일을 기록합니다.

## 미디어 파일 정책

- `.mp4`, `.mov`, `.wav`, `.aif`, `.psd`, `.ai` 등 바이너리는 **git에 커밋하지 않습니다**.
- 대신 각 폴더의 `INDEX.md`에 파일명/길이/내용 요약을 기록합니다.
- 큰 파일은 외부 저장소(클라우드 드라이브 등) 링크를 `INDEX.md`에 함께 둡니다.

## 명명 규칙 요약

- 프로젝트 슬러그: 소문자 + 하이픈. 예) `intro-ai-agent`, `q2-recap`
- 신(scene) ID: `S01`, `S02`, ...
- 컷(cut) ID: `S01-C01`, `S01-C02`, ...
- 모션 에셋: `S01-C02_typing-cursor.mp4`
- 녹음: `S01_take01.mp4`

자세한 내용은 `docs/workflow.md`를 참고하세요.
