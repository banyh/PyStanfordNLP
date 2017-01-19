# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from jpype import startJVM, getDefaultJVMPath, shutdownJVM, java, JPackage, isJVMStarted
from os.path import join, dirname
from platform import system
import pickle
from .conv2cn import Conv2Cn as _Conv2Cn
from .conv2tw import Conv2Tw as _Conv2Tw

conv2cn = _Conv2Cn().conv
conv2tw = _Conv2Tw().conv


class Segmenter(object):
    def __init__(self, lang='zh'):
        if system() == 'Linux':
            sep = ':'
        else:
            sep = ';'  # Windows
        pwd = dirname(__file__)
        main_dir = join(pwd, 'seg')
        if not isJVMStarted():
            startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" +
                     sep.join([main_dir, join(main_dir, 'stanford-segmenter-3.6.0.jar'),
                     join(pwd, '..', 'stanford_postagger', 'pos'),
                     join(pwd, '..', 'stanford_postagger', 'pos', 'stanford-postagger.jar'),
                     join(main_dir, 'slf4j-api.jar'), join(main_dir, 'slf4j-simple.jar')]))
        # --------- for debugging -----------
        print('JVM classpath:')
        cl = java.lang.ClassLoader.getSystemClassLoader()
        for url in cl.getURLs():
            print(url.getFile())
        # --------- end debugging -----------
        prop = java.util.Properties()
        prop.setProperty('sighanCorporaDict', 'data')
        prop.setProperty('serDictionary', 'data/dict-chris6.ser.gz')
        prop.setProperty('inputEncoding', 'UTF-8')
        prop.setProperty('sighanPostProcessing', 'true')
        self.segmenter = JPackage('edu').stanford.nlp.ie.crf.CRFClassifier(prop)
        self.segmenter.loadClassifierNoExceptions("data/ctb.gz", prop)

        with open(join(dirname(__file__), 'dict.set'), 'rb') as f:
            self.dicset = pickle.load(f)

    def _ngram_in_dict(self, string, n):
        ngrams = set()
        for i in range(len(string) - n + 1):
            if string[i:(i+n)] in self.dicset:
                ngrams.add(string[i:(i+n)])
        return ngrams

    def _cn_segment(self, cn_text):
        return list(self.segmenter.segmentString(cn_text))

    def _tw_segment(self, tw_text):
        cn_text = conv2cn(tw_text)
        tw_text = tw_text.replace('\r', '').replace('\n', '').replace(' ', '').replace('　', '')
        seg = self._cn_segment(cn_text)
        if seg is None:
            return None
        tlen = map(len, seg)
        tw_seg = []
        i = 0
        for wl in tlen:
            tw_seg.append(tw_text[i:(i + wl)])
            i += wl
        return tw_seg

    def _combine_keyword(self, segmented):
        out = []
        i = 0
        while i < len(segmented) - 3:
            bigram = ''.join(segmented[i:(i+2)])
            trigram = ''.join(segmented[i:(i+3)])
            quadgram = ''.join(segmented[i:(i+4)])
            if quadgram in self.dicset:
                out.append(quadgram)
                i += 4
            elif trigram in self.dicset:
                out.append(trigram)
                i += 3
            elif bigram in self.dicset:
                out.append(bigram)
                i += 2
            else:
                out.append(segmented[i])
                i += 1
        out.extend(segmented[i:])
        return out

    def cn_segment(self, cn_text):
        original = cn_text
        segmented = ' '.join(self._cn_segment(cn_text))
        if segmented is None:
            return None
        err_word = []
        for length in range(7, 2, -1):
            ngram = self._ngram_in_dict(original, length)
            if not ngram:
                continue
            for w in ngram:
                if segmented.count(w) != original.count(w):
                    err_word.append(w)
        for w in err_word:
            original = original.replace(w, ' ' + w + ' ')
        seg = self._cn_segment(original)
        if seg is None:
            return None
        seg = self._combine_keyword(seg)
        return seg

    def tw_segment(self, tw_text):
        cn_text = conv2cn(tw_text)
        tw_text = tw_text.replace('\r', '').replace('\n', '').replace(' ', '')
        cn_seg = self.cn_segment(cn_text)
        if cn_seg is None:
            return None
        tlen = map(len, cn_seg)
        tw_seg = []
        i = 0
        for wl in tlen:
            tw_seg.append(tw_text[i:(i + wl)])
            i += wl
        return tw_seg
