#!/bin/zsh
# Copy a self-contained skill; repeated installation never clobbers local edits.
set -euo pipefail

if (( $# > 1 )); then
  print -u2 'Usage: zsh scripts/install-skill.zsh [ABSOLUTE_SKILLS_DIRECTORY]'
  exit 2
fi
install_repo="${0:A:h:h}"
install_source="$install_repo/skills/init-new-computer"
install_parent="${1:-$HOME/.agents/skills}"
install_destination="$install_parent/init-new-computer"
[[ "$install_parent" == /* ]] || { print -u2 'Use an absolute skills directory.'; exit 2; }
[[ -f "$install_source/SKILL.md" ]] || { print -u2 'Source SKILL.md is missing.'; exit 2; }

if [[ -e "$install_destination" || -L "$install_destination" ]]; then
  if [[ ! -L "$install_destination" && -d "$install_destination" ]] &&
      /usr/bin/diff -rq "$install_source" "$install_destination" >/dev/null; then
    print -r -- "Already installed: $install_destination"
    exit 0
  fi
  print -u2 -r -- "Existing skill differs: $install_destination. Back it up and review the intended update first."
  exit 1
fi

mkdir -p "$install_parent"
install_stage=$(/usr/bin/mktemp -d "$install_parent/.init-new-computer.XXXXXX")
trap 'if [[ -n ${install_stage:-} && -d "$install_stage" ]]; then command rm -r -- "$install_stage"; fi' EXIT
cp -R "$install_source/." "$install_stage/"
mv "$install_stage" "$install_destination"
print -r -- "Installed: $install_destination"
print 'Invoke $init-new-computer in your AI tool; refresh/restart skill discovery if needed.'
