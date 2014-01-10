#!/usr/bin/env bash
set -ue

USAGE="Usage: $(basename $0) [options] [file]
       cat [file] | $(basename $0) [options]
Standard head with some new options.
All the standard head options apply. If no new ones are used, vanilla head is
invoked.
  -p: Print all the lines until (and including) the first one that contains the
      given pattern. By default it is interpreted as a (proper Python) regex.
  -l: Match the given pattern as a literal string, not a regex.
  -N: End on this line number (or before it, if -E is used)
  -E: Exclude the matching line."

if which extract >/dev/null 2>/dev/null; then
  cmd="extract"
elif which extract.py >/dev/null 2>/dev/null; then
  cmd="extract.py"
else
  echo "Error: extract command not found in PATH." >&2
  exit 1
fi

vanilla="true"; pattern=""; linenum=""; literal=""; exclude=""
while getopts ":p:N:lEh" opt; do
  case "$opt" in
    p) pattern=${OPTARG}
       vanilla=""
      ;;
    N) linenum=${OPTARG}
       vanilla=""
      ;;
    l) literal="-l"
       vanilla=""
      ;;
    E) exclude="-E"
       vanilla=""
      ;;
    h) echo "$USAGE"
       exit
      ;;
  esac
done

if [[ "$vanilla" ]]; then
  exec head $@
fi

infile=${@:$OPTIND:1}

nums=""
if [[ "$pattern" ]] && [[ "$linenum" ]]; then
  echo "Error: Do not give both a -p pattern and a -N line number." >&2
  exit 1
elif [[ "$pattern" ]]; then
  end="$pattern"
elif [[ "$linenum" ]]; then
  end="$linenum"
  nums="-n"
fi

exec $cmd -e $end $nums $literal $exclude $infile

