# -*- coding: utf-8 -*-
from __future__ import division

__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

# spec_analyser.py generates input data for fuzzification

from nltk import corpus as corpus, word_tokenize, pos_tag
from string import maketrans
from lxml import etree
from math import log10
from main import *
import enchant
import re
#import csv
#import sys


class LocationVector(object):
    def __init__(self, path, spec_words, bi_grams, tri_grams, four_grams, five_grams):
        self.path = path
        self.spec_words = spec_words
        self.bi_grams = bi_grams
        self.tri_grams = tri_grams
        self.four_grams = four_grams
        self.five_grams = five_grams

    def parseXML(self):
        parser = etree.XMLParser(recover=True)
        f = etree.parse(self.path, parser)
        fstring = etree.tostring(f, pretty_print=True)
        bookmarks = self.findBookmarks(fstring)
        bookmarks = '<Part>' + '\n' + bookmarks + '</Part>' + '\n'
        fstring = fstring.replace('<bookmark-tree>', bookmarks)
        fstring = fstring.replace('<Annot>', ' ')
        fstring = fstring.replace('</Annot>', ' ')
        fstring = fstring.replace('</bookmark-tree>', '')
        # deleting <Figure> and </Figure> tags
        fstring = fstring.replace('<Figure>', '')
        fstring = fstring.replace('</Figure>', '')
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
                        # any change in line below should be replicated in method generateLocationVector of 
                        # class LocationVector of this file and corpus.py file also
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
                    LocationVector.generateLocationVector(self, branch[subtree], ("{0}[{1}]".format(index, subtree)))


class HelperFunctions(object):
    def isNumber(self, s):
        m = re.findall(r"(^[0-9]*[0-9., ]*$)", s)
        return m

    def allLowerCase(self, s):
        m = re.search("[a-z]", s)
        return m

    def percentage(self, a, b):
        return 100 * float(a / b)


class WordTagger(HelperFunctions):
    """
        parse xml and generate location vector
    """
    spell_checker_US = enchant.Dict('en_US')
    spell_checker_GB = enchant.Dict('en_GB')
    spell_checker_AU = enchant.Dict('en_AU')
    negation_words_data = []
    negation_adverbs_data = []

    def __init__(self, spec_ID, path, output_write, output_bigrams_write, output_trigrams_write, output_fourgrams_write,
                 output_fivegrams_write, candidates_write, spec_words, bi_grams, tri_grams, four_grams, five_grams,
                 statement_facts_data, corpus, corpus_bigrams, corpus_trigrams, corpus_fourgrams, corpus_fivegrams,
                 spec_count, spec_word_count_list, spec_bi_gram_count_list, spec_tri_gram_count_list,
                 spec_four_gram_count_list, spec_five_gram_count_list):
        super(WordTagger, self).__init__()
        self.word_location = []
        self.spec_ID = spec_ID
        self.path = path
        self.output = output_write
        self.output_bigrams_write = output_bigrams_write
        self.output_trigrams_write = output_trigrams_write
        self.output_fourgrams_write = output_fourgrams_write
        self.output_fivegrams_write = output_fivegrams_write
        self.candidates = candidates_write

        self.spec_words = spec_words
        self.bi_grams = bi_grams
        self.tri_grams = tri_grams
        self.four_grams = four_grams
        self.five_grams = five_grams

        self.corpus = corpus
        self.corpus_bigrams = corpus_bigrams
        self.corpus_trigrams = corpus_trigrams
        self.corpus_fourgrams = corpus_fourgrams
        self.corpus_fivegrams = corpus_fivegrams

        self.spec_count = spec_count
        self.spec_word_count_list = spec_word_count_list
        self.spec_bi_gram_count_list = spec_bi_gram_count_list
        self.spec_tri_gram_count_list = spec_tri_gram_count_list
        self.spec_four_gram_count_list = spec_four_gram_count_list
        self.spec_five_gram_count_list = spec_five_gram_count_list
        self.statement_facts_data = statement_facts_data
        self.word_facts_data = []

        self.sections = []

        self.tf_idf_list = {}
        self.tf_idf_bigram_list = {}
        self.tf_idf_trigram_list = {}
        self.tf_idf_fourgram_list = {}
        self.tf_idf_fivegram_list = {}

        self.spec_domain_dict_match = []
        self.potential_candidates = []

        self.common_eng_words = {}
        self.common_eng_words_UPPER = {}
        self.abbreviation_cluster = {}

        self.nouns_unigrams = {}
        self.verbs_unigrams = {}

        self.bigram_NNP_NNP = {}
        self.bigram_NNP_NN = {}
        self.bigram_NN_NN = {}

        self.trigram_NNP_NNP_NNP = {}
        self.trigram_NNP_NNP_NN = {}
        self.trigram_NNP_NN_NN = {}
        self.trigram_NN_NN_NN = {}

        self.fourgram_NNP_NNP_NNP_NNP = {}

        self.fivegram_NNP_NNP_NNP_NNP_NNP = {}

        self.loc_sig_link_unigrams = {}
        self.loc_sig_TD_unigrams = {}
        self.loc_sig_LI_Title_unigrams = {}
        self.loc_sig_TH_unigrams = {}
        self.loc_sig_H1_unigrams = {}
        self.loc_sig_H2_unigrams = {}
        self.loc_sig_H3_unigrams = {}
        self.loc_sig_H4_unigrams = {}
        self.loc_sig_H5_unigrams = {}
        self.loc_sig_H6_unigrams = {}

        self.spec_english_dict_match_count = 0
        self.number_match_count = 0
        self.abbreviation_match_count = 0
        self.symbol_match_count = 0
        self.repetitive_word_count = 0

        self.index = 1
        self.index_bigram = 1
        self.index_trigram = 1
        self.index_fourgram = 1
        self.index_fivegram = 1
        self.candidate_index = 1

        self.potential_tags = ['Link', 'TD', 'LI_Title', 'TH', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6']

    def parseXML(self):
        #parser = etree.XMLParser(ns_clean=True, remove_pis=True, recover=True)
        parser = etree.XMLParser(recover=True)
        f = etree.parse(self.path, parser)
        fstring = etree.tostring(f, pretty_print=True)
        bookmarks = self.findBookmarks(fstring)
        bookmarks = '<Part>' + '\n' + bookmarks + '</Part>' + '\n'
        fstring = fstring.replace('<bookmark-tree>', bookmarks)
        fstring = fstring.replace('<Annot>', ' ')
        fstring = fstring.replace('</Annot>', ' ')
        fstring = fstring.replace('</bookmark-tree>', '')
        fstring = fstring.replace('<Annot>', ' ')
        fstring = fstring.replace('</Annot>', ' ')
        # deleting <Figure> and </Figure> tags
        fstring = fstring.replace('<Figure>', '')
        fstring = fstring.replace('</Figure>', '')
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
        """
            generating location vector for every data in spec
        """
        signature_map = []
        #statement_signature_map = []

        signature = branch.tag
        #print branch.getchildren()
        parent = branch.getparent()

        while True:
            if not parent is None:
                signature_map.append(parent.tag)
                parent = parent.getparent()
                continue
            break

        signature_map.append(signature)
        last = signature_map[-1]
        signature_map = signature_map[-2::-1]
        signature_map.append(last)

        if branch.text is not None:
            branch.text = branch.text.encode('ascii', 'ignore')

            if not branch.getchildren():
                statements = branch.text.split('. ')
                signature_map.append('statement')
                self.statement_signature_map = signature_map
                signature_map.append('word')

                for statement in range(0, len(statements)):
                    statement_location = (("{0}[{1}]".format(index, statement)), statements[statement])
                    self.statement_facts_data.append(
                        [statement_location[1], statement_location[0],
                         self.statement_signature_map])  # CLIPS facts data
                    words = statements[statement].split()
                    self.statement_loc_vec = statement_location[0]
                    for word in range(0, len(words)):
                        self.word_location = (("{0}[{1}][{2}]".format(index, statement, word)), words[word])
                        # any change in line below should be replicated in method generateLocationVector of 
                        # class LocationVector of this file and corpus.py file also
                        symbols = ",[]();:<>+=&+%!@#~?{}|"
                        whitespace = "                      "
                        replace = maketrans(symbols, whitespace)
                        spec_word = self.word_location[1].translate(replace)
                        spec_word = spec_word.lstrip()
                        spec_word = spec_word.rstrip()

                        if len(spec_word) > 1 and not len(spec_word) > 16:
                            self.spec_word = spec_word
                            self.spec_word_lower_case = spec_word.lower()
                            self.word_location_index = self.word_location[0].replace('][', ' ')
                            self.word_location_index = self.word_location_index.replace('[', '')
                            self.word_location_index = self.word_location_index.replace(']', '')
                            self.signature_map = signature_map
                            #print self.spec_word, self.word_location_index, self.signature_map
                            WordTagger.wordMatcher(self)

                    bi_grams = bigrams(words)
                    if not len(bi_grams) < 1:
                        for i, bi_gram in enumerate(bi_grams):
                            self.bi_gram = ' '.join(bi_gram)
                            self.statement_loc_vec = self.statement_loc_vec.replace('][', ' ')
                            self.statement_loc_vec = self.statement_loc_vec.replace('[', '')
                            self.statement_loc_vec = self.statement_loc_vec.replace(']', '')
                            self.bi_gram_index = self.statement_loc_vec + ' ' + str(
                                i) + ' | ' + self.statement_loc_vec + ' ' + str(i + 1)
                            #print self.bi_gram, self.bi_gram_index
                            WordTagger.wordMatcherBigram(self, self.bi_gram)

                    tri_grams = trigrams(words)
                    if not len(tri_grams) < 1:
                        for i, tri_gram in enumerate(tri_grams):
                            self.tri_gram = ' '.join(tri_gram)
                            self.statement_loc_vec = self.statement_loc_vec.replace('][', ' ')
                            self.statement_loc_vec = self.statement_loc_vec.replace('[', '')
                            self.statement_loc_vec = self.statement_loc_vec.replace(']', '')
                            self.tri_gram_index = self.statement_loc_vec + ' ' + str(
                                i) + ' | ' + self.statement_loc_vec + ' ' + str(
                                i + 1) + ' | ' + self.statement_loc_vec + ' ' + str(i + 2)
                            #print self.tri_gram, self.tri_gram_index
                            WordTagger.wordMatcherTrigram(self, self.tri_gram)

                    four_grams = ngrams(words, 4)
                    if not len(four_grams) < 1:
                        for i, four_gram in enumerate(four_grams):
                            self.four_gram = ' '.join(four_gram)
                            self.statement_loc_vec = self.statement_loc_vec.replace('][', ' ')
                            self.statement_loc_vec = self.statement_loc_vec.replace('[', '')
                            self.statement_loc_vec = self.statement_loc_vec.replace(']', '')
                            self.four_gram_index = self.statement_loc_vec + ' ' + str(
                                i) + ' | ' + self.statement_loc_vec + ' ' + str(
                                i + 1) + ' | ' + self.statement_loc_vec + ' ' + str(
                                i + 2) + ' | ' + self.statement_loc_vec + ' ' + str(i + 3)
                            #print self.four_gram, self.four_gram_index
                            WordTagger.wordMatcherFourgram(self, self.four_gram)

                    five_grams = ngrams(words, 5)
                    if not len(five_grams) < 1:
                        for five_gram in five_grams:
                            self.five_gram = ' '.join(five_gram)
                            self.statement_loc_vec = self.statement_loc_vec.replace('][', ' ')
                            self.statement_loc_vec = self.statement_loc_vec.replace('[', '')
                            self.statement_loc_vec = self.statement_loc_vec.replace(']', '')
                            self.five_gram_index = self.statement_loc_vec + ' ' + str(
                                i) + ' | ' + self.statement_loc_vec + ' ' + str(
                                i + 1) + ' | ' + self.statement_loc_vec + ' ' + str(
                                i + 2) + ' | ' + self.statement_loc_vec + ' ' + str(
                                i + 3) + ' | ' + self.statement_loc_vec + ' ' + str(i + 4)
                            #print self.five_gram, self.five_gram_index
                            WordTagger.wordMatcherFivegram(self, self.five_gram)

            else:
                for subtree in range(0, len(branch)):
                    WordTagger.generateLocationVector(self, branch[subtree], ("{0}[{1}]".format(index, subtree)))

    def wordMatcher(self):
        WordTagger.tf(self)
        WordTagger.idf(self)
        WordTagger.tf_idf(self)
        WordTagger.wordFactsData(self)
        WordTagger.englishDictMatch(self)
        WordTagger.numberMatch(self)
        WordTagger.abbreviationMatch(self)
        WordTagger.symbolMatch(self)
        WordTagger.repetitiveWords(self)
        WordTagger.posTaggingUnigrams(self)
        WordTagger.wordSignatureWeight(self)
        WordTagger.csvTableData(self)
        WordTagger.potentialCandidates(self)

    def wordMatcherBigram(self, bi_gram):
        WordTagger.tf_bigram(self)
        WordTagger.idf_bigram(self)
        WordTagger.tf_idf_bigram(self)
        WordTagger.firstLetterOfEveryWordCapitalized(self, bi_gram)
        WordTagger.statementSignatureWeight(self)
        WordTagger.posTagging(self, bi_gram)
        WordTagger.csvTableDataBigrams(self)

    def wordMatcherTrigram(self, tri_gram):
        WordTagger.tf_trigram(self)
        WordTagger.idf_trigram(self)
        WordTagger.tf_idf_trigram(self)
        WordTagger.firstLetterOfEveryWordCapitalized(self, tri_gram)
        WordTagger.statementSignatureWeight(self)
        WordTagger.posTagging(self, tri_gram)
        WordTagger.csvTableDataTrigrams(self)

    def wordMatcherFourgram(self, four_gram):
        WordTagger.tf_fourgram(self)
        WordTagger.idf_fourgram(self)
        WordTagger.tf_idf_fourgram(self)
        WordTagger.firstLetterOfEveryWordCapitalized(self, four_gram)
        WordTagger.statementSignatureWeight(self)
        WordTagger.posTagging(self, four_gram)
        WordTagger.csvTableDataFourgrams(self)

    def wordMatcherFivegram(self, five_gram):
        WordTagger.tf_fivegram(self)
        WordTagger.idf_fivegram(self)
        WordTagger.tf_idf_fivegram(self)
        WordTagger.firstLetterOfEveryWordCapitalized(self, five_gram)
        WordTagger.statementSignatureWeight(self)
        WordTagger.posTagging(self, five_gram)
        WordTagger.csvTableDataFivegrams(self)

    def tf(self):
        word_count = self.spec_words.count(self.spec_word)
        self.tf = word_count / float(len(self.spec_words))

    def tf_bigram(self):
        bigram_count = self.bi_grams.count(self.bi_gram)
        self.tf_bigram = bigram_count / float(len(self.bi_grams))

    def tf_trigram(self):
        trigram_count = self.tri_grams.count(self.tri_gram)
        self.tf_trigram = trigram_count / float(len(self.tri_grams))

    def tf_fourgram(self):
        fourgram_count = self.four_grams.count(self.four_gram)
        self.tf_fourgram = fourgram_count / float(len(self.four_grams))

    def tf_fivegram(self):
        fivegram_count = self.five_grams.count(self.five_gram)
        self.tf_fivegram = fivegram_count / float(len(self.five_grams))

    def idf(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.spec_word_count_list)):
            end += self.spec_word_count_list[i]
            if self.spec_word in self.corpus[start:end]:
                word_occurrence += 1
                start = end + 1
            start = end + 1
        self.idf = log10(float(self.spec_count + 1) / (word_occurrence + 1))

    def idf_bigram(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.spec_bi_gram_count_list)):
            end += self.spec_bi_gram_count_list[i]
            if self.bi_gram in self.corpus_bigrams[start:end]:
                word_occurrence += 1
                start = end + 1
            start = end + 1
        self.idf_bigram = log10(float(self.spec_count + 1) / (word_occurrence + 1))

    def idf_trigram(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.spec_tri_gram_count_list)):
            end += self.spec_tri_gram_count_list[i]
            if self.tri_gram in self.corpus_trigrams[start:end]:
                word_occurrence += 1
                start = end + 1
            start = end + 1
        self.idf_trigram = log10(float(self.spec_count + 1) / (word_occurrence + 1))

    def idf_fourgram(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.spec_four_gram_count_list)):
            end += self.spec_four_gram_count_list[i]
            if self.four_gram in self.corpus_fourgrams[start:end]:
                word_occurrence += 1
                start = end + 1
            start = end + 1
        self.idf_fourgram = log10(float(self.spec_count + 1) / (word_occurrence + 1))

    def idf_fivegram(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.spec_five_gram_count_list)):
            end += self.spec_five_gram_count_list[i]
            if self.five_gram in self.corpus_fivegrams[start:end]:
                word_occurrence += 1
                start = end + 1
            start = end + 1
        self.idf_fivegram = log10(float(self.spec_count + 1) / (word_occurrence + 1))

    def tf_idf(self):
        self.tf_idf = self.tf * self.idf
        # clever way to create dict with dup keys is to make values the keys | values here is a list of info
        self.signature_map = ' '.join(str(sig) for sig in self.signature_map)
        #print self.word_location_index
        self.tf_idf_list[self.tf_idf, self.word_location_index, self.signature_map] = self.spec_word

        loc_ind = self.word_location_index.split(' ')
        loc_sig = self.signature_map.split(' ')

        # ************ grouping all sections in the document ************
        #print self.spec_word, loc_ind, loc_sig

        # xml Scheme 1 | eg. amber
        loc_ind = [int(ind) for ind in loc_ind]
        for i, (ind, tag) in enumerate(zip(loc_ind, loc_sig)):
            if ind >= 0 and tag == 'Sect' and loc_ind[i + 1] == 0 and 'H' in loc_sig[i + 1] and loc_ind[i + 2] == 0 and loc_sig[i + 2] == 'statement' and loc_ind[i + 3] >= 0 and loc_sig[i + 3] == 'word':
                print self.spec_word
                self.sections.append([self.spec_word, self.word_location_index, self.signature_map])

        # xml Scheme 2 | eg. jidan doc
        for i, tag in enumerate(loc_sig):
            if tag == 'Sect' and 'heading' in loc_sig[i + 1]:
                self.sections.append([self.spec_word, self.word_location_index, self.signature_map])

    def tf_idf_bigram(self):
        self.tfidf_bigram = self.tf_bigram * self.idf_bigram
        self.tf_idf_bigram_list[self.tfidf_bigram, self.bi_gram_index, self.signature_map] = self.bi_gram
        #print self.bi_gram, self.bi_gram_index, self.signature_map

    def tf_idf_trigram(self):
        self.tfidf_trigram = self.tf_trigram * self.idf_trigram
        self.tf_idf_trigram_list[self.tfidf_trigram, self.tri_gram_index, self.signature_map] = self.tri_gram
        #print self.tri_gram, self.tri_gram_index, self.signature_map

    def tf_idf_fourgram(self):
        self.tfidf_fourgram = self.tf_fourgram * self.idf_fourgram
        self.tf_idf_fourgram_list[self.tfidf_fourgram, self.four_gram_index, self.signature_map] = self.four_gram

    def tf_idf_fivegram(self):
        self.tfidf_fivegram = self.tf_fivegram * self.idf_fivegram
        self.tf_idf_fivegram_list[self.tfidf_fivegram, self.five_gram_index, self.signature_map] = self.five_gram

    def wordFactsData(self):
        self.word_facts_data.append([self.spec_word, self.spec_ID, self.path, self.word_location_index,
                                     self.signature_map])  # CLIPS facts data (Spec Words)

    def englishDictMatch(self):
        """
            matching spec word to English dictionaries
        """
        self.spell_checker_US = enchant.Dict('en_US')
        self.spell_checker_GB = enchant.Dict('en_GB')
        self.spell_checker_AU = enchant.Dict('en_AU')

        if self.spec_word_lower_case in (corpus.stopwords.words('english')):
            self.spec_english_dict_match = 'Yes (NTLK Stopword)'
            self.spec_english_dict_match_count += 1

        elif self.spell_checker_US.check(self.spec_word_lower_case) is True and not self.spell_checker_GB.check(
                self.spec_word_lower_case) is True and not self.spell_checker_AU.check(
                self.spec_word_lower_case) is True:
            self.spec_english_dict_match = 'Yes (en_US)'
            self.spec_english_dict_match_count += 1

        elif self.spell_checker_GB.check(self.spec_word_lower_case) is True and not self.spell_checker_US.check(
                self.spec_word_lower_case) is True and not self.spell_checker_AU.check(
                self.spec_word_lower_case) is True:
            self.spec_english_dict_match = 'Yes (en_GB)'
            self.spec_english_dict_match_count += 1

        elif self.spell_checker_AU.check(self.spec_word_lower_case) is True and not self.spell_checker_US.check(
                self.spec_word_lower_case) is True and not self.spell_checker_GB.check(
                self.spec_word_lower_case) is True:
            self.spec_english_dict_match = 'Yes (en_AU)'
            self.spec_english_dict_match_count += 1

        elif self.spell_checker_US.check(self.spec_word_lower_case) is True and self.spell_checker_GB.check(
                self.spec_word_lower_case) is True and not self.spell_checker_AU.check(
                self.spec_word_lower_case) is True:
            self.spec_english_dict_match = 'Yes (en_US, en_GB)'

        elif self.spell_checker_US.check(self.spec_word_lower_case) is True and self.spell_checker_AU.check(
                self.spec_word_lower_case) is True and not self.spell_checker_GB.check(
                self.spec_word_lower_case) is True:
            self.spec_english_dict_match = 'Yes (en_US, en_AU)'

        elif self.spell_checker_GB.check(self.spec_word_lower_case) is True and self.spell_checker_AU.check(
                self.spec_word_lower_case) is True and not self.spell_checker_US.check(
                self.spec_word_lower_case) is True:
            self.spec_english_dict_match = 'Yes (en_GB, en_AU)'

        elif self.spell_checker_US.check(self.spec_word_lower_case) is True and self.spell_checker_GB.check(
                self.spec_word_lower_case) is True and self.spell_checker_US.check(self.spec_word_lower_case) is True:
            self.spec_english_dict_match = 'Yes (en_US, en_GB, en_AU)'

        else:
            self.spec_english_dict_match = 'No'

    def numberMatch(self):
        if HelperFunctions.isNumber(self, self.spec_word):
            self.number_match = 'Yes'
            self.number_match_count += 1

        else:
            self.number_match = 'No'

    def abbreviationMatch(self):
        if HelperFunctions.allLowerCase(self, self.spec_word) is None and self.spell_checker_US.check(
                self.spec_word) is False:
            self.abbreviation_match = 'Yes'
            self.abbreviation_match_count += 1

        else:
            self.abbreviation_match = 'No'

    def symbolMatch(self):
        if '_' in self.spec_word or '/' in self.spec_word:
            self.symbol_match = 'Yes'
            self.symbol_match_count += 1
        else:
            self.symbol_match = 'No'

    def repetitiveWords(self):
        if self.idf == 0.0:
            self.repetitive_word = 'Yes'
            self.repetitive_word_count += 1
        else:
            self.repetitive_word = 'No'

    def posTaggingUnigrams(self):
        self.pos = pos_tag([self.spec_word])
        # NN or NNP --> Nouns (Priority Level = 1)
        if not self.spec_word_lower_case in (corpus.stopwords.words('english')) and not self.idf == 1.0 and \
                (self.pos[0][1] == 'NN' or self.pos[0][1] == 'NNP'):
            self.nouns_unigrams[self.spec_word] = self.tf_idf
        if not self.spec_word_lower_case in (corpus.stopwords.words('english')) and not self.idf == 1.0 and \
                        self.pos[0][1] == 'VB':
            self.verbs_unigrams[self.spec_word] = self.tf_idf

    def wordSignatureWeight(self):
        """
            Creating words bags for Location Attributes !!
        """
        self.potential_tags = ['Link', 'TD', 'LI_Title', 'TH', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6']
        if set(self.potential_tags) & set(self.signature_map):
            self.potential_tags_found = list(set(self.potential_tags) & set(self.signature_map))
            if not self.spec_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'Link' in self.potential_tags_found:
                self.loc_sig_link_unigrams[self.spec_word] = self.tf_idf
            if not self.spec_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'TD' in self.potential_tags_found:
                self.loc_sig_TD_unigrams[self.spec_word] = self.tf_idf
            if not self.spec_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'LI_Title' in self.potential_tags_found:
                self.loc_sig_LI_Title_unigrams[self.spec_word] = self.tf_idf
            if not self.spec_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'TH' in self.potential_tags_found:
                self.loc_sig_TH_unigrams[self.spec_word] = self.tf_idf
            if not self.spec_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'H1' in self.potential_tags_found:
                self.loc_sig_H1_unigrams[self.spec_word] = self.tf_idf
            if not self.spec_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'H2' in self.potential_tags_found:
                self.loc_sig_H2_unigrams[self.spec_word] = self.tf_idf
            if not self.spec_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'H3' in self.potential_tags_found:
                self.loc_sig_H3_unigrams[self.spec_word] = self.tf_idf
            if not self.spec_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'H4' in self.potential_tags_found:
                self.loc_sig_H4_unigrams[self.spec_word] = self.tf_idf
            if not self.spec_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'H5' in self.potential_tags_found:
                self.loc_sig_H5_unigrams[self.spec_word] = self.tf_idf
            if not self.spec_word_lower_case in (
                corpus.stopwords.words('english')) and not self.idf == 1.0 and 'H6' in self.potential_tags_found:
                self.loc_sig_H6_unigrams[self.spec_word] = self.tf_idf

        else:
            self.potential_tags_found = {}

    def statementSignatureWeight(self):
        if set(self.potential_tags) & set(self.statement_signature_map):
            self.potential_tags_found = list(set(self.potential_tags) & set(self.statement_signature_map))
        else:
            self.potential_tags_found = {}

    def firstLetterOfEveryWordCapitalized(self, string):
        cap_count = 0
        words = string.split()
        for word in words:
            if word[0].isupper():
                cap_count += 1
        if cap_count == len(words):
            self.first_letter_cap = "Yes"
        else:
            self.first_letter_cap = "No"

    def posTagging(self, string):
        """

        POS Tagger for bigrams | trigrams | 4-grams | 5-grams
        """
        words = word_tokenize(string)
        self.pos = pos_tag(words)
        self.pos = [x[1] for x in self.pos]

        # POS word bags for bigrams
        if len(self.pos) == 2 and self.pos[0] == 'NNP' and self.pos[1] == 'NNP':
            self.bigram_NNP_NNP[string] = self.tfidf_bigram

        if len(self.pos) == 2 and self.pos[0] == 'NNP' and self.pos[1] == 'NN':
            self.bigram_NNP_NN[string] = self.tfidf_bigram

        if len(self.pos) == 2 and self.pos[0] == 'NN' and self.pos[1] == 'NN':
            self.bigram_NN_NN[string] = self.tfidf_bigram

        # POS word bags for trigrams
        if len(self.pos) == 3 and self.pos[0] == 'NNP' and self.pos[1] == 'NNP' and self.pos[2] == 'NNP':
            self.trigram_NNP_NNP_NNP[string] = self.tfidf_trigram

        if len(self.pos) == 3 and self.pos[0] == 'NNP' and self.pos[1] == 'NNP' and self.pos[2] == 'NN':
            self.trigram_NNP_NNP_NN[string] = self.tfidf_trigram

        if len(self.pos) == 3 and self.pos[0] == 'NNP' and self.pos[1] == 'NN' and self.pos[2] == 'NN':
            self.trigram_NNP_NN_NN[string] = self.tfidf_trigram

        if len(self.pos) == 3 and self.pos[0] == 'NN' and self.pos[1] == 'NN' and self.pos[2] == 'NN':
            self.trigram_NN_NN_NN[string] = self.tfidf_trigram

        # POS word bags for 4-grams
        if len(self.pos) == 4 and self.pos[0] == 'NNP' and self.pos[1] == 'NNP' and self.pos[2] == 'NNP' and self.pos[
            3] == 'NNP':
            self.fourgram_NNP_NNP_NNP_NNP[string] = self.tfidf_fourgram

        # POS word bags for 5-grams
        if len(self.pos) == 5 and self.pos[0] == 'NNP' and self.pos[1] == 'NNP' and self.pos[2] == 'NNP' and self.pos[
            3] == 'NNP' and self.pos[4] == 'NNP':
            self.fivegram_NNP_NNP_NNP_NNP_NNP[string] = self.tfidf_fivegram

    def csvTableData(self):
        """
            writing results to Fuzzy table (see output_table.html)
        """
        self.output.writerow(
            [self.index, self.spec_word, self.word_location_index, self.signature_map, self.potential_tags_found,
             self.tf, self.idf, self.tf_idf, self.spec_english_dict_match, self.number_match, self.abbreviation_match,
             self.symbol_match, self.repetitive_word])
        self.index += 1

    def csvTableDataBigrams(self):
        self.output_bigrams_write.writerow(
            [self.index_bigram, self.bi_gram, self.statement_loc_vec, self.statement_signature_map,
             self.potential_tags_found, self.tf_bigram, self.idf_bigram, self.tfidf_bigram, self.first_letter_cap,
             self.pos])
        self.index_bigram += 1

    def csvTableDataTrigrams(self):
        self.output_trigrams_write.writerow(
            [self.index_trigram, self.tri_gram, self.statement_loc_vec, self.statement_signature_map,
             self.potential_tags_found, self.tf_trigram, self.idf_trigram, self.tfidf_trigram, self.first_letter_cap,
             self.pos])
        self.index_trigram += 1

    def csvTableDataFourgrams(self):
        self.output_fourgrams_write.writerow(
            [self.index_fourgram, self.four_gram, self.statement_loc_vec, self.statement_signature_map,
             self.potential_tags_found, self.tf_fourgram, self.idf_fourgram, self.tfidf_fourgram, self.first_letter_cap,
             self.pos])
        self.index_fourgram += 1

    def csvTableDataFivegrams(self):
        self.output_fivegrams_write.writerow(
            [self.index_fivegram, self.five_gram, self.statement_loc_vec, self.statement_signature_map,
             self.potential_tags_found, self.tf_fivegram, self.idf_fivegram, self.tfidf_fivegram, self.first_letter_cap,
             self.pos])
        self.index_fivegram += 1

    def potentialCandidates(self):
        # common English dictionary words
        if not self.spec_word_lower_case in (
            corpus.stopwords.words('english')) and not self.idf == 1.0 and self.spell_checker_US.check(
                self.spec_word_lower_case) is True:
            self.common_eng_words[self.spec_word] = self.tf_idf

        # common English words that are all upper case
        if not self.spec_word_lower_case in (
            corpus.stopwords.words('english')) and not self.idf == 1.0 and self.spell_checker_US.check(
                self.spec_word_lower_case) is True and HelperFunctions.allLowerCase(self, self.spec_word) is None:
            self.common_eng_words_UPPER[self.spec_word] = self.tf_idf

        # ABBREVIATION cluster
        if not self.spec_word_lower_case in (corpus.stopwords.words('english')) and not self.idf == 1.0 and \
                        self.abbreviation_match == 'yes':
            self.abbreviation_cluster[self.spec_word] = self.tf_idf

        if self.number_match == 'No' and self.abbreviation_match == 'No' and self.symbol_match == 'No' and \
                        self.repetitive_word == 'No':
            self.candidates.writerow(
                [self.candidate_index, self.spec_word, self.word_location_index, self.tf, self.idf, self.tf_idf])
            self.potential_candidates.append(self.spec_word.lower())
            self.candidate_index += 1

    def printPercentageMatch(self):
        print '\nTotal number of words in Spec = %d' % (self.index - 1)
        print 'Out of %d spec_words, %d words matched with English dictionaries, which is %4f percent of spec_words' % (
            self.index - 1, self.spec_english_dict_match_count,
            HelperFunctions.percentage(self, self.spec_english_dict_match_count, (self.index - 1)))
        print 'Out of %d spec_words, %d words are numbers, which is %4f percent of spec_words' % (
            self.index - 1, self.number_match_count,
            HelperFunctions.percentage(self, self.number_match_count, (self.index - 1)))
        print 'Out of %d spec_words, %d words are abbreviations, which is %4f percent of spec_words' % (
            self.index - 1, self.abbreviation_match_count,
            HelperFunctions.percentage(self, self.abbreviation_match_count, (self.index - 1)))
        print 'Out of %d spec_words, %d words are symbols, which is %4f percent of spec_words' % (
            self.index - 1, self.symbol_match_count,
            HelperFunctions.percentage(self, self.symbol_match_count, (self.index - 1)))
        print 'Out of %d spec_words, %d words are repetitive, which is %4f percent of spec_words' % (
            self.index - 1, self.repetitive_word_count,
            HelperFunctions.percentage(self, self.repetitive_word_count, (self.index - 1)))
        print 'Out of %d spec_words, %d words are unmatched words, which is %4f percent of spec_words' % (
            self.index - 1, self.candidate_index,
            HelperFunctions.percentage(self, self.candidate_index, (self.index - 1)))
        print

    def accuracy(self):
        identified = []
        self.spec_domain_dict_match = list(set(self.spec_domain_dict_match))
        for candidate in self.potential_candidates:
            if candidate in self.spec_domain_dict_match:
                identified.append(candidate)
        identified = list(set(identified))
        accuracy = float(len(identified) / len(self.spec_domain_dict_match)) * 100
        print accuracy
        print
        print "Identified Features!"
        print len(identified), identified
        print
