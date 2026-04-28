#!/usr/bin/env bash
# 새 프로젝트를 _template 에서 복제하여 생성합니다.
#
# 사용법:
#   ./tools/new-project.sh <slug> "<한국어 제목>"
#
# 예:
#   ./tools/new-project.sh intro-ai-agent "AI 에이전트가 뭔가요?"

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <slug> \"<title>\"" >&2
  echo "  slug: 소문자 + 하이픈 (예: intro-ai-agent)" >&2
  exit 1
fi

SLUG="$1"
TITLE="$2"

if [[ ! "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "ERROR: slug must be lowercase letters/digits with hyphens (got: $SLUG)" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="$ROOT_DIR/projects/_template"
TARGET_DIR="$ROOT_DIR/projects/$SLUG"

if [[ -e "$TARGET_DIR" ]]; then
  echo "ERROR: $TARGET_DIR already exists" >&2
  exit 1
fi

cp -R "$TEMPLATE_DIR" "$TARGET_DIR"

TODAY="$(date +%Y-%m-%d)"

# meta.yaml 채우기 (sed 인플레이스, BSD/GNU 호환을 위해 임시파일 사용)
META="$TARGET_DIR/meta.yaml"
TMP="$(mktemp)"
sed -e "s/^slug: TEMPLATE$/slug: $SLUG/" \
    -e "s/^title: \"프로젝트 한국어 제목\"$/title: \"$TITLE\"/" \
    -e "s/^created: YYYY-MM-DD$/created: $TODAY/" \
    "$META" > "$TMP"
mv "$TMP" "$META"

# README.md 제목 치환
sed -i.bak "s/<프로젝트 제목>/$TITLE/" "$TARGET_DIR/README.md" 2>/dev/null || \
  { TMP="$(mktemp)"; sed "s/<프로젝트 제목>/$TITLE/" "$TARGET_DIR/README.md" > "$TMP" && mv "$TMP" "$TARGET_DIR/README.md"; }
rm -f "$TARGET_DIR/README.md.bak"

echo "Created: $TARGET_DIR"
echo "  slug : $SLUG"
echo "  title: $TITLE"
echo
echo "다음 단계: $TARGET_DIR/00-plan/concept.md 부터 작성하세요."
