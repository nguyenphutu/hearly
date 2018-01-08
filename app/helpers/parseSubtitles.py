import srt
import random
import re


def fill_word(line):
    return random.choice(re.findall("\w+\'?\w*", line))


def convert_srt(filename):
    file = open(filename, 'r')
    doc = file.read()
    subs = list(srt.parse(doc))
    data = []
    for i, sub in enumerate(subs):
        c = list()
        c.append(i)
        c.append(str(sub.start.total_seconds()) + '-' + str(sub.end.total_seconds()))
        c.append(str(sub.start)[2:7])
        c.append(fill_word(sub.content))
        blank = fill_word(sub.content)
        c.append(sub.content.replace(blank + ' ',
                                     ' <input type="text" maxlength="20" size="5" class="subfiller__blank autogrow" ' + 'data-answer="' + blank + '"> ',
                                     1))
        data.append(c)
    return data
