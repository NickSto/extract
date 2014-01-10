#!/usr/bin/env python
import os
import re
import sys
from optparse import OptionParser

OPT_DEFAULTS = {'start':'', 'end':'', 'include':False, 'literal':False,
  'nums':False}
USAGE = """USAGE: %prog [start pattern] [end pattern] [file name]
       cat file | %prog [start pattern] [end pattern]
       %prog -s [start pattern] [file name]
       %prog -e [start pattern] [file name]"""
DESCRIPTION = """Extract a section from a file or stdout, starting and/or ending
at a matching line. Essentially, this is a version of head and tail where you
can specify the line by a grep-like pattern instead of a number."""
EPILOG = """"""

def main():

  parser = OptionParser(usage=USAGE, description=DESCRIPTION, epilog=EPILOG)

  parser.add_option('-s', '--start', dest='start',
    default=OPT_DEFAULTS.get('str'),
    help='Start pattern. Supply with this option if not giving an end pattern.')
  parser.add_option('-e', '--end', dest='end',
    default=OPT_DEFAULTS.get('end'),
    help='End pattern. Supply with this option if not giving a start pattern.')
  parser.add_option('-n', '--nums', dest='nums', action='store_true',
    default=OPT_DEFAULTS.get('nums'),
    help='Use start and end as line numbers instead of a pattern.')
  parser.add_option('-l', '--literal', dest='literal', action='store_true',
    default=OPT_DEFAULTS.get('literal'),
    help='Use the pattern(s) as a literal string to find in the matching line, '
      +'not a regex.')
  parser.add_option('-i', '--include', dest='include', action='store_true',
    default=OPT_DEFAULTS.get('include'),
    help='Include the lines that match the start and/or end pattern.')

  (options, arguments) = parser.parse_args()

  if not arguments and not options.start and not options.end:
    parser.print_help()
    fail("\nPlease provide a start and/or end pattern.")

  args = len(arguments)

  if args == 2 and (options.start or options.end):
    parser.print_help()
    fail("\nError: if giving both a start and end pattern, please provide them "
      +"both as positional arguments, without -e and -s.")

  if args == 0 or args == 2:
    infile = sys.stdin
  elif args == 1 or args == 3:
    infile = open(arguments[-1], 'r')

  if args == 2 or args == 3:
    (start, end) = arguments[:2]
  elif args == 0 or args == 1:
    (start, end) = (options.start, options.end)

  if options.nums:
    if not start:
      start = 0
    if not end:
      end = sys.maxsize
    try:
      (start, end) = (int(start), int(end))
    except ValueError:
      parser.print_help()
      fail("\nError: selection by line number enabled, but the given start "
        +"and/or end are not integers: "+str(start)+", "+str(end))
  else:
    if not start:
      start = ''
    if not end:
      end = ''

  # if no start was given, start printing from the beginning
  if start:
    started = False
  else:
    started = True
  ended = False

  line_num = 0
  for line in infile:
    line_num += 1
    if options.nums:
      # don't print if we're before the starting line
      # (or if we're on it, and "include" is not enabled)
      if line_num < start or (line_num == start and not options.include):
        continue
      # don't print if we're past the ending line
      # (or if we're on it, and "include" is not enabled)
      if line_num > end or (line_num == end and not options.include):
        continue
    else:
      if not started and is_match(start, line, options):
        started = True
        if not options.include:
          continue
      if not started:
        continue
      if ended:
        continue
      elif end and is_match(end, line, options):
        ended = True
        if not options.include:
          continue
    sys.stdout.write(line)


  # Avoid closing sys.stdin, to be safe
  if isinstance(infile, file):
    infile.close()


def is_match(pattern, line, options):
  if options.literal:
    return pattern in line
  else:
    return re.search(pattern, line)


def fail(message):
  sys.stderr.write(message+"\n")
  sys.exit(1)

if __name__ == "__main__":
  main()