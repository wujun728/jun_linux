# -*- coding: utf-8 -*-
"""
http://www.nltk.org/
首页示例
"""
import nltk

# Tokenize and tag some text:
sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."
tokens = nltk.word_tokenize(sentence)
print tokens

tagged = nltk.pos_tag(tokens)
print tagged[0:6]

# Identify named entities:
entities = nltk.chunk.ne_chunk(tagged)
print entities

# Display a parse tree:
from nltk.corpus import treebank
t = treebank.parsed_sents('wsj_0001.mrg')[0]
t.draw()

# NLTK中文语料库 sinica_treebank
from nltk.corpus import sinica_treebank
sinica_text = nltk.Text(sinica_treebank.words())
print sinica_text

for (key, var) in sinica_treebank.tagged_words()[:8]:
    print '%s%s' % (key, var),

# NLTK中文句法树
sinica_treebank.parsed_sents()[15].draw()