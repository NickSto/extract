#!/usr/bin/env bash
set -ue

USAGE="Usage: $(basename $0) [options] pattern|line_num filename
       cat filename | $(basename $0) [options] pattern|line_num
Standard tail with some new options.
Print all the lines after (and including) the first one matching the given
pattern or line number. Patterns can be full (Python) regex. Standard tail
options can be given instead and the built-in tail will be invoked.
  -N: Required if using a line number.
  -l: Match the given pattern as a literal string, not a regex.
  -E: Exclude the matching line."

if which extract >/dev/null 2>/dev/null; then
  cmd="extract"
elif which extract.py >/dev/null 2>/dev/null; then
  cmd="extract.py"
else
  echo "Error: extract command not found in PATH." >&2
  exit 1
fi

vanilla="true"; nums=""; literal=""; exclude=""
while getopts ":NlEh" opt; do
  case "$opt" in
    N) nums="-n"
       vanilla="";;
    l) literal="-l"
       vanilla="";;
    E) exclude="-E"
       vanilla="";;
    h) echo "$USAGE"
       exit;;
  esac
done


if [[ $OPTIND -le $# ]]; then
  # positional arguments present
  vanilla=""
  infile=""
  start=${@:$OPTIND:1}
  if [[ ${@:$OPTIND+1:1} ]]; then
    infile=${@:$OPTIND+1:1}
  fi
fi

if [[ "$vanilla" ]]; then
  exec tail $@
fi

if [[ ${infile:0:1} == '-' ]] || [[ ${start:0:1} == '-' ]]; then
  echo -e "Error: must give options before positional arguments.\n" >&2
  echo "$USAGE"
  exit 1
fi

exec $cmd -s $start $nums $literal $exclude $infile

