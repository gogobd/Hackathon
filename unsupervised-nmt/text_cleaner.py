#!/usr/bin/env python3

import re
import sys
from collections import Counter


if len(sys.argv) != 2:
    print('{0} <textfile>'.format(sys.argv[0]))
    print('Writes cleaned textfile to stdout.')
    sys.exit()

linecount = 0
validlinecount = 0
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
                '<<< fragmentation <<<\n' +
                ' '.join(words) + 
                '\n\n'
            )
            continue
        if len(words) <= 1:
            sys.stderr.write(
                '<<< too short <<<\n\n'
            )
            continue
        if len(words) >= 256:
            sys.stderr.write(
                '<<< too long <<<\n' + 
                ' '.join(words) + 
                '\n\n'
            )
            continue
        if len(line) > 1024:
            sys.stderr.write(
                '<<< line {0} too long <<<\n\n'.format(linecount) +
                ' '.join(words) + 
                '\n\n'
            )
            continue            
        validlinecount += 1
        sys.stdout.buffer.write(
            (' '.join(
                words
            ) + '\n').encode('utf-8')
        )
        if linecount % 5000 == 0:
            sys.stderr.write(
                "{0} lines processed, {1} are valid...\n".format(
                    linecount,
                    validlinecount,
                )
            )
