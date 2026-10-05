#!/bin/zsh
# Update only this skill's marked block; keep the user's surrounding content.
set -euo pipefail
setopt extendedglob
umask 077

if (( $# != 4 )); then
  print -u2 'Usage: zsh managed-block.zsh ABSOLUTE_TARGET BLOCK_ID CONTENT_FILE PRIVATE_BACKUP_DIR'
  exit 2
fi

config_target=$1
config_id=$2
config_content=$3
config_backup_dir=$4
[[ "$config_target" == /* && "$config_backup_dir" == /* ]] || {
  print -u2 'Target and backup directory must be absolute paths.'; exit 2
}
[[ "$config_id" == [a-zA-Z0-9_-]## && ${#config_id} -le 64 ]] || {
  print -u2 'Invalid block ID.'; exit 2
}
[[ -f "$config_content" ]] || { print -u2 'Content file is missing.'; exit 2; }
[[ -d "${config_target:h}" ]] || { print -u2 'Target parent is missing.'; exit 2; }
[[ ! -L "$config_target" ]] || {
  print -u2 'Target is a symlink; use the existing dotfiles management workflow.'; exit 2
}
[[ ! -e "$config_target" || -f "$config_target" ]] || {
  print -u2 'Target is not a regular file.'; exit 2
}

config_begin="# BEGIN init-new-computer:${config_id}"
config_end="# END init-new-computer:${config_id}"
config_input=/dev/null
config_mode=600
if [[ -f "$config_target" ]]; then
  config_input="$config_target"
  config_mode=$(/usr/bin/stat -f '%Lp' "$config_target")
fi
config_stage=$(/usr/bin/mktemp "${config_target}.init-new-computer.XXXXXX")
trap 'if [[ -n ${config_stage:-} && -f "$config_stage" ]]; then command rm -f -- "$config_stage"; fi' EXIT

if ! /usr/bin/awk -v marker_begin="$config_begin" -v marker_end="$config_end" '
  FILENAME == ARGV[1] {
    if ($0 == marker_begin || $0 == marker_end) { bad = 1 }
    content[++content_count] = $0
    next
  }
  $0 == marker_begin {
    if (inside || ++begins > 1) { bad = 1 }
    inside = 1
    print marker_begin
    for (i = 1; i <= content_count; i++) { print content[i] }
    print marker_end
    next
  }
  $0 == marker_end {
    if (!inside) { bad = 1 }
    ends++
    inside = 0
    next
  }
  !inside { print; output_count++ }
  END {
    if (bad || inside || begins != ends) { exit 1 }
    if (!begins) {
      if (output_count > 0) { print "" }
      print marker_begin
      for (i = 1; i <= content_count; i++) { print content[i] }
      print marker_end
    }
  }
' "$config_content" "$config_input" > "$config_stage"; then
  print -u2 'Malformed/duplicate block markers; target was not changed.'
  exit 1
fi

if [[ -f "$config_target" ]] && /usr/bin/cmp -s "$config_target" "$config_stage"; then
  print -r -- "Already configured: $config_target"
  exit 0
fi
mkdir -p "$config_backup_dir"
chmod 700 "$config_backup_dir"
config_backup=$(/usr/bin/mktemp "${config_backup_dir}/config.XXXXXX")
if [[ -f "$config_target" ]]; then
  cp -p "$config_target" "$config_backup"
else
  print -r -- "Previously absent: $config_target" > "$config_backup"
fi
chmod 600 "$config_backup"
chmod "$config_mode" "$config_stage"
mv "$config_stage" "$config_target"
print -r -- "Updated: $config_target; original recorded in $config_backup"
