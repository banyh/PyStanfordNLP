from __future__ import unicode_literals, print_function
from setuptools import setup
from setuptools.command.install import install
from os.path import join, dirname, isfile, isdir
from os import unlink
try:
    from urllib.request import urlretrieve
except:
    from urllib import urlretrieve
import sys
import time
import zipfile


def report(count, blockSize, totalSize):
    percent = float(count) * blockSize * 100 / totalSize
    print('downloaded {:f}%     '.format(percent), end='\r')


class Compile(install):
    def run(self):
        install.run(self)
        sys.path.reverse()
        # ----------- install segmenter ------------
        import stanford_segmenter
        pwd = stanford_segmenter.__path__[0]
        if not isdir(join(pwd, 'stanford-segmenter-2015-12-09')):
            print('Start downloading stanford-segmenter-2015-12-09.zip...')
            urlretrieve('http://nlp.stanford.edu/software/stanford-segmenter-2015-12-09.zip', 'seg.zip', report)
            with zipfile.ZipFile('seg.zip', 'r') as z:
                z.extractall(pwd)
            unlink('seg.zip')
        # ----------- install postagger ------------
        import stanford_postagger
        pwd = stanford_postagger.__path__[0]
        if not isdir(join(pwd, 'stanford-postagger-full-2015-12-09')):
            print('Start downloading stanford-postagger-full-2015-12-09.zip...')
            urlretrieve('http://nlp.stanford.edu/software/stanford-postagger-full-2015-12-09.zip', 'pos.zip', report)
            with zipfile.ZipFile('pos.zip', 'r') as z:
                z.extractall(pwd)
            unlink('pos.zip')


setup(name='stanford_wrapper',
      version='0.2.0',
      description='Wrapping Stanford NLP as Python Packages',
      url='https://github.com/banyh/PyStanfordNLP',
      author='Ping Chu Hung',
      author_email='banyhong@gliacloud.com',
      license='MIT',
      packages=['stanford_segmenter', 'stanford_postagger'],
      zip_safe=False,
      install_requires=[
          'numpy',
          'jpype1',
      ],
      cmdclass={
          'install': Compile,
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,)
