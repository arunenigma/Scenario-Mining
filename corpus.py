# -*- coding: utf-8 -*-
__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from nltk import bigrams, trigrams, ngrams
from string import maketrans
from lxml import etree


class Corpus(object):
    def __init__(self, path, spec_words, bi_grams, tri_grams, four_grams, five_grams):
        self.path = path
        self.spec_words = spec_words
        self.bi_grams = bi_grams
        self.tri_grams = tri_grams
        self.four_grams = four_grams
        self.five_grams = five_grams

    def parseXML(self):
        #parser = etree.XMLParser(ns_clean=True, remove_pis=True, recover=True)
        parser = etree.XMLParser(recover=True)
        f = etree.parse(self.path, parser)
        print f
        fstring = etree.tostring(f, encoding=unicode, pretty_print=True)
        bookmarks = self.findBookmarks(fstring)
        bookmarks = '<Part>' + '\n' + bookmarks + '</Part>' + '\n'
        fstring = fstring.replace('<bookmark-tree>', bookmarks)
        fstring = fstring.replace('<Annot>', ' ')
        fstring = fstring.replace('</Annot>', ' ')
        fstring = fstring.replace('</bookmark-tree>', '')
        element = etree.fromstring(fstring)
        return element

    def findBookmarks(self, fstring):
        bookmarks = " "
        fragments = fstring.split('\n')
        symbols = ",[]();:<>+=&+%!@#~?{}|"
        whitespace = "                      "
        for fragment in fragments:
            if '<bookmark title' in fragment:
                fragment = fragment.replace('<bookmark title=', '')
                fragment = fragment.replace('">', '')
                replace = maketrans(symbols, whitespace)
                fragment = fragment.translate(replace)
                fragment = fragment.replace('"', '')
                fragment = fragment.lstrip()
                fragment = fragment.rstrip()

                fragment = '<P>' + '\n' + '<Link>' + fragment + '</Link>' + '\n' + '</P>'
                #fragment = '<P>' + '\n' + '<Link>' + fragment + '</Link>' + '\n' + '</P>'
                bookmarks += fragment + '\n'
        return bookmarks

    def generateLocationVector(self, branch, index):
        if branch.text is not None:
            branch.text = branch.text.encode('ascii', 'ignore')

            if not branch.getchildren():
                sentences = branch.text.split('. ')

                for sentence in range(0, len(sentences)):
                    #sentence_location = (("{0}[{1}]".format(index, sentence)), sentences[sentence])
                    words = sentences[sentence].split()

                    for word in range(0, len(words)):
                        word_location = (("{0}[{1}][{2}]".format(index, sentence, word)), words[word])
                        symbols = ",[]();:<>+=&+%!@#~?{}|"
                        whitespace = "                      "
                        replace = maketrans(symbols, whitespace)
                        spec_word = word_location[1].translate(replace)
                        spec_word = spec_word.lstrip()
                        spec_word = spec_word.rstrip()

                        if len(spec_word) > 1 and not len(spec_word) > 16:
                            self.spec_words.append(spec_word)

                    bi_grams = bigrams(words)
                    if not len(bi_grams) < 1:
                        for bi_gram in bi_grams:
                            bi_gram = ' '.join(bi_gram)
                            self.bi_grams.append(bi_gram)

                    tri_grams = trigrams(words)
                    if not len(tri_grams) < 1:
                        for tri_gram in tri_grams:
                            tri_gram = ' '.join(tri_gram)
                            self.tri_grams.append(tri_gram)

                    four_grams = ngrams(words, 4)
                    if not len(four_grams) < 1:
                        for four_gram in four_grams:
                            four_gram = ' '.join(four_gram)
                            self.four_grams.append(four_gram)

                    five_grams = ngrams(words, 5)
                    if not len(five_grams) < 1:
                        for five_gram in five_grams:
                            five_gram = ' '.join(five_gram)
                            self.five_grams.append(five_gram)                    

            else:
                for subtree in range(0, len(branch)):
                    Corpus.generateLocationVector(self, branch[subtree], ("{0}[{1}]".format(index, subtree)))
