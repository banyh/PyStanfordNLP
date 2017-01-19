# A Python Wrapper of Stanford Chinese Segmenter

## Prerequisite

* Java 8


## Installation

```
pip install git+https://github.com/banyh/PyStanfordNLP
```


## Usage

```python
from stanford_segmenter import Segmenter
from stanford_postagger import Postagger

seg = Segmenter()  # the only supported language is 'zh'
pos = Postagger()  # supported language: 'zh', 'en', 'fr', 'de', 'es'

seg.segment('你昨天去電影院了嗎?')
# ['你', '昨天', '去', '電影院', '了', '嗎', '?']
pos.postag('你 昨天 去 電影院 了 嗎 ?')
# '你#PN 昨天#NT 去#VV 電影院#VV 了#AS 嗎#NN ？#PU '
```
