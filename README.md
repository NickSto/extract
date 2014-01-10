Have you ever been using head, but wanted to set the ending line by a grep pattern instead of a line number? Or been using tail and wanted to set the starting line by a line number instead of doing math to find out how far the line is from the end? Better yet, have you found yourself using head + tail to extract sections from the middle of a file, but got tired of doing the math to get the right lines?

extract.py satisfies all those desires by letting you select a section from a file (or stdin) by patterns or line numbers. And then heade.sh and taile.sh use extract.py to extend the capabilities of standard head and tail. They add those options you wish head and tail had, and use extract.py to execute them.

Just make sure extract.py is on your PATH and you're good to go.

Usages:

`Usage: extract.py \[start pattern\] \[end pattern\] \[file name\]
       cat file | extract.py \[start pattern\] \[end pattern\]
       extract.py -s \[start pattern\] \[file name\]
       extract.py -e \[start pattern\] \[file name\]

Extract a section from a file or stdout, starting and/or ending at a matching
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
  -E, --exclude         Exclude the lines that match the start and/or end
                        pattern.
`

`Usage: heade.sh \[options\] \[file\]
       cat \[file\] | heade \[options\]
Standard head with some new options.
All the standard head options apply. If no new ones are used, vanilla head is
invoked.
  -p: Print all the lines until (and including) the first one that contains the
      given pattern. By default it is interpreted as a (proper Python) regex.
  -l: Match the given pattern as a literal string, not a regex.
  -N: End on this line number (or before it, if -E is used)
  -E: Exclude the matching line.
`

`Usage: taile.sh \[options\] \[file\]
       cat \[file\] | taile.sh \[options\]
Standard tail with some new options.
All the standard tail options apply. If no new ones are used, vanilla tail is
invoked.
  -p: Print all the lines after (and including) the first one that contains the
      given pattern. By default it is interpreted as a (proper, Python) regex.
  -l: Match the given pattern as a literal string, not a regex.
  -N: Start on this line number (or after it, if -E is used)
  -E: Exclude the matching line.
`

