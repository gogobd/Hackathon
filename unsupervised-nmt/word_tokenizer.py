#!/usr/bin/env python3

import re
import sys
from collections import Counter


if len(sys.argv) != 2:
    print('{0} <corpus>'.format(sys.argv[0]))
    print('Writes single word entities to stdout.')
    sys.exit()

linecount = 0
wordcount = Counter()
with open(sys.argv[1], 'rb') as infile:
    for line in infile:
        linecount += 1
        line = line.decode('utf-8')
        line = re.sub(r'(\W)', ' \\1 ', line)
        words = re.findall(r'\S+', line, re.UNICODE)
        wordcount.update(words)
        if linecount % 5000 == 0:
            sys.stderr.write(
                "{0} lines seen, {1} word entities found.\n".format(
                    linecount,
                    len(wordcount),
                    # wordcount.most_common(8),
                )
            )

l = [
    '<blank>',
    '<s>',
    '</s>',
]
l += [i[0].encode('utf-8').decode('utf-8') for i in wordcount.most_common()]

sys.stdout.buffer.write(
    '\n'.join(
        l
    ).encode('utf-8')
)
