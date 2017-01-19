from jpype import startJVM, getDefaultJVMPath, shutdownJVM, java, JPackage, isJVMStarted
from os.path import join, dirname
from platform import system


class Postagger(object):
    def __init__(self, lang='zh'):
        if system() == 'Linux':
            sep = ':'
        else:
            sep = ';'  # Windows
        pwd = dirname(__file__)
        main_dir = join(pwd, 'pos')
        if not isJVMStarted():
            startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" +
                     sep.join([main_dir, join(main_dir, 'stanford-postagger.jar'),
                     join(pwd, '..', 'stanford_segmenter', 'seg'),
                     join(pwd, '..', 'stanford_segmenter', 'seg', 'stanford-segmenter-3.6.0.jar'),
                     join(main_dir, 'lib', 'slf4j-api.jar'), join(main_dir, 'lib', 'slf4j-simple.jar')]))
        # --------- for debugging -----------
        print('JVM classpath:')
        cl = java.lang.ClassLoader.getSystemClassLoader()
        for url in cl.getURLs():
            print(url.getFile())
        # --------- end debugging -----------
        maxent = JPackage('edu').stanford.nlp.tagger.maxent
        if lang == 'zh':
            self.postagger = maxent.MaxentTagger('models/chinese-distsim.tagger')
        elif lang == 'en':
            self.postagger = maxent.MaxentTagger('models/english-bidirectional-distsim.tagger')
        elif lang == 'fr':
            self.postagger = maxent.MaxentTagger('models/french.tagger')
        elif lang == 'de':
            self.postagger = maxent.MaxentTagger('models/german-dewac.tagger')
        elif lang == 'es':
            self.postagger = maxent.MaxentTagger('models/spanish-distsim.tagger')
        else:
            raise ValueError('Not Support Language: {}'.format(lang))

    def postag(self, segmented_sent):
        return self.postagger.tagTokenizedString(segmented_sent)
