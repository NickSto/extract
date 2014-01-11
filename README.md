Have you ever been using head, but wanted to set the ending line by a grep pattern instead of a line number? Or been using tail and wanted to set the starting line by a line number instead of doing math to find out how far the line is from the end? Better yet, have you found yourself using head + tail to extract sections from the middle of a file, but got tired of doing the math to get the right lines?

extract.py satisfies all those desires by letting you select a section from a file (or stdin) by patterns or line numbers. And then heade.sh and taile.sh use extract.py to extend the capabilities of standard head and tail. They add those options you wish head and tail had, and use extract.py to execute them.

Just make sure extract.py is on your PATH and you're good to go.

Usages:
extract.py
```
Usage: extract.py [options] start_pattern end_pattern filename
       cat filename | extract.py [options] start_pattern end_pattern
       extract.py [options] -s start_pattern filename
       extract.py [options] -e end_pattern filename

Extract a section from a file or stdout, starting andgor ending at a matching
line. Essentially, this is a version of head and tail where you can specify
the line by a grep-like pattern instead of a number.

Options:
  -h, --help            show this help message and exit
  -s START, --start=START
                        Start pattern. Supply with this option if not giving
                        an end pattern.
  -e END, --end=END     End pattern. Supply with this option if not giving a
                        start pattern.
  -n, --nums            Use start and end as line numbers instead of a
                        pattern.
  -l, --literal         Use the pattern(s) as a literal string to find in the
                        matching line, not a regex.
  -E, --exclude         Exclude the lines that match the start andgor end
                        pattern.
```

heade.sh
```
Usage: heade [options] pattern|line_num filename
       cat filename | heade [options] pattern|line_num
Standard head with some new options.
Print all the lines up to (and including) the first one matching the given
pattern or line number. Patterns can be full (Python) regex. Standard head
options can be given instead and the built-in head will be invoked.
  -N: Required if using a line number.
  -l: Match the given pattern as a literal string, not a regex.
  -E: Exclude the matching line.
```

taile.sh
```
Usage: taile.sh [options] pattern|line_num filename
       cat filename | taile.sh [options] pattern|line_num
Standard tail with some new options.
Print all the lines after (and including) the first one matching the given
pattern or line number. Patterns can be full (Python) regex. Standard tail
options can be given instead and the built-in tail will be invoked.
  -N: Required if using a line number.
  -l: Match the given pattern as a literal string, not a regex.
  -E: Exclude the matching line.
```

