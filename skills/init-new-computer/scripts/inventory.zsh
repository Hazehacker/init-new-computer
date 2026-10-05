#!/bin/zsh
# Read-only facts. Never prints private keys, config contents or serial numbers.
set -uo pipefail

if [[ "$(uname -s)" != Darwin ]]; then
  print -u2 'This inventory is for macOS. Use an OS-specific plan on this machine.'
  exit 2
fi

print 'System'
sw_vers
print -r -- "Architecture: $(uname -m)"
print -n 'Memory bytes: '
/usr/sbin/sysctl -n hw.memsize 2>/dev/null || print 'unavailable in this execution environment'
print -n 'Model: '
/usr/sbin/sysctl -n hw.model 2>/dev/null || print 'unavailable'
df -h /
print -n 'Command Line Tools: '
xcode-select -p 2>/dev/null || print 'not configured'

print '\nCommand locations (presence alone is not verification)'
for inventory_tool in git brew java javac mvn node npm docker code; do
  inventory_location=$(whence -p "$inventory_tool" 2>/dev/null) || inventory_location='not on PATH'
  print -r -- "${inventory_tool}: ${inventory_location}"
done
for inventory_file in /opt/homebrew/bin/brew /usr/local/bin/brew "$HOME/.sdkman/bin/sdkman-init.sh"; do
  [[ ! -f "$inventory_file" ]] || print -r -- "Found: $inventory_file"
done

print '\nApplications'
for inventory_app in /Applications/*.app(N) "$HOME"/Applications/*.app(N); do
  print -r -- "${inventory_app:t}"
done

print '\nConfiguration presence (contents withheld)'
for inventory_name in .zprofile .zshrc .gitconfig .ssh; do
  if [[ -e "$HOME/$inventory_name" || -L "$HOME/$inventory_name" ]]; then
    print -r -- "Present: $inventory_name"
  else
    print -r -- "Absent: $inventory_name"
  fi
done

print '\nBattery summary'
system_profiler SPPowerDataType 2>/dev/null | /usr/bin/awk '
  /Cycle Count:|Condition:|Maximum Capacity:/ { print }
'
