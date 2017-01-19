from jpype import startJVM, getDefaultJVMPath, shutdownJVM, java, JPackage, isJVMStarted
from os.path import join, dirname
from platform import system


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

    def segment(self, text):
        return list(self.segmenter.segmentString(text))
