#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=(
  "$HOME/.claude/skills"
  "$HOME/.agents/skills"
  "$HOME/.codex/skills"
  "$HOME/.config/opencode/skills"
)

names=()
srcs=()
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  names+=("$(basename "$src")")
  srcs+=("$src")
done < <(find "$REPO/skills" -name SKILL.md -not -path '*/node_modules/*' -not -path '*/deprecated/*' -print0 | sort -z)

for DEST in "${DESTS[@]}"; do
  if [ -L "$DEST" ]; then
    case "$(readlink "$DEST")" in
      */dotfiles/.config/opencode/skills)
        rm "$DEST"
        echo "replaced old dotfiles skills symlink: $DEST"
        ;;
      *)
        echo "skipped $DEST (it is a symlink not owned by this installer)"
        continue
        ;;
    esac
  fi

  mkdir -p "$DEST"

  for i in "${!names[@]}"; do
    name="${names[$i]}"
    src="${srcs[$i]}"
    target="$DEST/$name"

    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "skipped $target (exists and is not a symlink)"
      continue
    fi

    if [ -L "$target" ]; then
      rm "$target"
    fi

    ln -s "$src" "$target"
    echo "linked $name -> $src ($DEST)"
  done
done
