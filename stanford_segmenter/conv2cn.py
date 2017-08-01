# -*- coding: utf-8 -*-
import re


class Conv2Cn(object):
    def __init__(self):
        from ._conv2cn_data import trad, simp, phrase_table
        self.one_char = dict((ord(t), ord(s)) for t, s in zip(trad, simp))

        num_char = max([len(t) for t, _ in phrase_table])
        phrases = [list() for i in range(num_char + 1)]
        for t, s in phrase_table:
            phrases[len(t)].append((t, s))

        patterns = []
        tables = []
        for ph in phrases:
            rep = dict((re.escape(trad), simp) for trad, simp in ph)
            tables.append(rep)
            patterns.append(re.compile("|".join(rep.keys())))

        self.patterns = []
        self.tables = []
        for i in range(len(tables)):
            if patterns[i].pattern != '':
                self.patterns.append(patterns[i])
                self.tables.append(tables[i])

    def conv(self, text):
        t = text.translate(self.one_char)
        for pattern, rep in zip(self.patterns[::-1], self.tables[::-1]):
            t = pattern.sub(lambda m: rep[re.escape(m.group(0))], t)
        return t
