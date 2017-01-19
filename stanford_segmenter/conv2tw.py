# -*- coding: utf-8 -*-
import re


class Conv2Tw(object):
    def __init__(self):
        from ._conv2tw_data import simp, trad, phrase_table
        self.one_char = dict((ord(s), ord(t)) for s, t in zip(simp, trad))

        num_char = max([len(simp) for simp, trad in phrase_table])
        phrases = [list() for i in range(num_char + 1)]
        for simp, trad in phrase_table:
            phrases[len(simp)].append((simp, trad))

        patterns = []
        tables = []
        for ph in phrases:
            rep = dict((re.escape(simp), trad) for simp, trad in ph)
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
