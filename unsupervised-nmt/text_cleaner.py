#!/usr/bin/env python3

import re
import sys
from collections import Counter


if len(sys.argv) != 2:
    print('{0} <textfile>'.format(sys.argv[0]))
    print('Writes cleaned textfile to stdout.')
    sys.exit()

linecount = 0
max_line_len = 0
with open(sys.argv[1], 'rb') as infile:
    for line in infile:
        linecount += 1
        line = line.decode('utf-8')
        line = re.sub(r'(\W)', ' \\1 ', line)
        words = re.findall(r'\S+', line, re.UNICODE)
        length_counter = Counter([len(w) for w in words])
        if length_counter[1] > 32:
            sys.stderr.write(
                str(length_counter[1]) +
                ' ' +
                # '<<< ' +
                ' '.join(words) + 
                '\n\n'
            )
            continue
        if len(words) > max_line_len:
            max_line_len = len(words)
            sys.stderr.write(
                ' '.join(words) + '\n'
            )
        sys.stdout.buffer.write(
            (' '.join(
                words
            ) + '\n').encode('utf-8')
        )
        if linecount % 5000 == 0:
            sys.stderr.write(
                "{0} lines seen, maximum length: {1}\n".format(
                    linecount,
                    max_line_len
                )
            )
