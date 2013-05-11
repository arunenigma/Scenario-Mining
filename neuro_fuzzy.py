from __future__ import division

__author__ = 'arunprasathshankar'
import itertools
from operator import itemgetter


class NeuroFuzzySystem(object):
    PI_bundle_unigrams = {}
    PI_bundle_bigrams = {}
    PI_bundle_trigrams = {}
    PI_bundle_fourgrams = {}
    PI_bundle_fivegrams = {}

    def __init__(self):
        self.word_list = []
        self.cog_list = []
        self.word_info = {}

        self.bigram_list = []
        self.cog_list_bigrams = []
        self.bigram_info = {}

        self.trigram_list = []
        self.cog_list_trigrams = []
        self.trigram_info = {}

        self.fourgram_list = []
        self.cog_list_fourgrams = []
        self.fourgram_info = {}

        self.fivegram_list = []
        self.cog_list_fivegrams = []
        self.fivegram_info = {}

        self.PI_bundle_unigrams = {}
        self.PI_bundle_bigrams = {}
        self.PI_bundle_trigrams = {}
        self.PI_bundle_fourgrams = {}
        self.PI_bundle_fivegrams = {}

        self.mfs = []

    def neuroFuzzyModelling(self, tf_idf_list, u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, tf_idf_bigram_list,
                            b1, b2, b3, tf_idf_trigram_list, t1, t2, t3, tf_idf_fourgram_list, f1, tf_idf_fivegram_list,
                            p1):
        """
        @param tf_idf_list: list of unigrams with info like tf_idf, location index and location signature
        @param tf_idf_bigram_list:
        @param tf_idf_trigram_list:
        @param tf_idf_fourgram_list:
        @param tf_idf_fivegram_list:
        """

        print tf_idf_bigram_list
        print tf_idf_trigram_list
        print tf_idf_fourgram_list
        print tf_idf_fivegram_list
        out = open('out.txt', 'w')
        for item in u1:
            out.write(str(item[0]) + " " + str(item[1]) + '\n')
        out.close()

        u1 = {item[0]: item[1:] for item in u1}  # word bag - common english words
        u2 = {item[0]: item[1:] for item in u2}
        u3 = {item[0]: item[1:] for item in u3}
        u4 = {item[0]: item[1:] for item in u4}
        u5 = {item[0]: item[1:] for item in u5}
        u6 = {item[0]: item[1:] for item in u6}
        u7 = {item[0]: item[1:] for item in u7}
        u8 = {item[0]: item[1:] for item in u8}
        u9 = {item[0]: item[1:] for item in u9}
        u10 = {item[0]: item[1:] for item in u10}
        u11 = {item[0]: item[1:] for item in u11}
        u12 = {item[0]: item[1:] for item in u12}

        b1 = {item[0]: item[1:] for item in b1}
        b2 = {item[0]: item[1:] for item in b2}
        b3 = {item[0]: item[1:] for item in b3}

        t1 = {item[0]: item[1:] for item in t1}
        t2 = {item[0]: item[1:] for item in t2}
        t3 = {item[0]: item[1:] for item in t3}

        f1 = {item[0]: item[1:] for item in f1}

        p1 = {item[0]: item[1:] for item in p1}

        for info, word in tf_idf_list.iteritems():

            try:

                u1_nrn_info = u1.get(word, 0)
                u2_nrn_info = u2.get(word, 0)
                u3_nrn_info = u3.get(word, 0)
                u4_nrn_info = u4.get(word, 0)
                u5_nrn_info = u5.get(word, 0)
                u6_nrn_info = u6.get(word, 0)
                u7_nrn_info = u7.get(word, 0)
                u8_nrn_info = u8.get(word, 0)
                u9_nrn_info = u9.get(word, 0)
                u10_nrn_info = u10.get(word, 0)
                u11_nrn_info = u11.get(word, 0)
                u12_nrn_info = u12.get(word, 0)

            except KeyError:
                continue

            self.mfs = []  # membership functions
            self.wts = []  # weights

            if not u1_nrn_info == 0:
                u1_mf1 = u1_nrn_info[1] * u1_nrn_info[2] - 1
                u1_mf2 = u1_nrn_info[3] * u1_nrn_info[4] - 1
                self.mfs.append([u1_mf1, u1_mf2])
                self.wts.append(u1_nrn_info[2])
                self.wts.append(u1_nrn_info[4])

            if not u2_nrn_info == 0:
                u2_mf1 = u2_nrn_info[1] * u2_nrn_info[2] + 1  # +1 --> bias
                u2_mf2 = u2_nrn_info[3] * u2_nrn_info[4] + 1
                self.mfs.append([u2_mf1, u2_mf2])
                self.wts.append(u2_nrn_info[2])
                self.wts.append(u2_nrn_info[4])

            if not u3_nrn_info == 0:
                u3_mf1 = u3_nrn_info[1] * u3_nrn_info[2]
                u3_mf2 = u3_nrn_info[3] * u3_nrn_info[4]
                self.mfs.append([u3_mf1, u3_mf2])
                self.wts.append(u3_nrn_info[2])
                self.wts.append(u3_nrn_info[4])

            if not u4_nrn_info == 0:
                u4_mf1 = u4_nrn_info[1] * u4_nrn_info[2]
                u4_mf2 = u4_nrn_info[3] * u4_nrn_info[4]
                self.mfs.append([u4_mf1, u4_mf2])
                self.wts.append(u4_nrn_info[2])
                self.wts.append(u4_nrn_info[4])

            if not u5_nrn_info == 0:
                u5_mf1 = u5_nrn_info[1] * u5_nrn_info[2]
                u5_mf2 = u5_nrn_info[3] * u5_nrn_info[4]
                self.mfs.append([u5_mf1, u5_mf2])
                self.wts.append(u5_nrn_info[2])
                self.wts.append(u5_nrn_info[4])

            if not u6_nrn_info == 0:
                u6_mf1 = u6_nrn_info[1] * u6_nrn_info[2]
                u6_mf2 = u6_nrn_info[3] * u6_nrn_info[4]
                self.mfs.append([u6_mf1, u6_mf2])
                self.wts.append(u6_nrn_info[2])
                self.wts.append(u6_nrn_info[4])

            if not u7_nrn_info == 0:
                u7_mf1 = u7_nrn_info[1] * u7_nrn_info[2]
                u7_mf2 = u7_nrn_info[3] * u7_nrn_info[4]
                self.mfs.append([u7_mf1, u7_mf2])
                self.wts.append(u7_nrn_info[2])
                self.wts.append(u7_nrn_info[4])

            if not u8_nrn_info == 0:
                u8_mf1 = u8_nrn_info[1] * u8_nrn_info[2]
                u8_mf2 = u8_nrn_info[3] * u8_nrn_info[4]
                self.mfs.append([u8_mf1, u8_mf2])
                self.wts.append(u8_nrn_info[2])
                self.wts.append(u8_nrn_info[4])

            if not u9_nrn_info == 0:
                u9_mf1 = u9_nrn_info[1] * u9_nrn_info[2]
                u9_mf2 = u9_nrn_info[3] * u9_nrn_info[4]
                self.mfs.append([u9_mf1, u9_mf2])
                self.wts.append(u9_nrn_info[2])
                self.wts.append(u9_nrn_info[4])

            if not u10_nrn_info == 0:
                u10_mf1 = u10_nrn_info[1] * u10_nrn_info[2]
                u10_mf2 = u10_nrn_info[3] * u10_nrn_info[4]
                self.mfs.append([u10_mf1, u10_mf2])
                self.wts.append([u10_nrn_info[2], u10_nrn_info[4]])

            if not u11_nrn_info == 0:
                u11_mf1 = u11_nrn_info[1] * u11_nrn_info[2]
                u11_mf2 = u11_nrn_info[3] * u11_nrn_info[4]
                self.mfs.append([u11_mf1, u11_mf2])
                self.wts.append(u11_nrn_info[2])
                self.wts.append(u11_nrn_info[4])

            if not u12_nrn_info == 0:
                u12_mf1 = u12_nrn_info[1] * u12_nrn_info[2]
                u12_mf2 = u12_nrn_info[3] * u12_nrn_info[4]
                self.mfs.append([u12_mf1, u12_mf2])
                self.wts.append(u12_nrn_info[2])
                self.wts.append(u12_nrn_info[4])

            if len(self.mfs) > 0:
                weights = sum(self.wts)
                rule_inputs = list(itertools.product(*self.mfs))
                number_of_wordbags = len(self.mfs)
                number_of_rules = len(rule_inputs)
                number_of_weights = len(self.wts)
                weight_factor = (number_of_wordbags * number_of_rules) / number_of_weights
                weights *= weight_factor
                rule_inputs = sum([sum(r) for r in rule_inputs])
                self.defuzzifyUnigrams(word, rule_inputs, weights, info)
                
        # ****************** BIGRAMS *******************
        for info, bigram, in tf_idf_bigram_list.iteritems():
            try:
                b1_nrn_info = b1.get(bigram, 0)
                b2_nrn_info = b2.get(bigram, 0)
                b3_nrn_info = b3.get(bigram, 0)

            except KeyError:
                continue
                
            self.mfs = []  # membership functions
            self.wts = []  # weights

            if not b1_nrn_info == 0:
                b1_mf1 = b1_nrn_info[1] * b1_nrn_info[2]
                b1_mf2 = b1_nrn_info[3] * b1_nrn_info[4]
                self.mfs.append([b1_mf1, b1_mf2])
                self.wts.append(b1_nrn_info[2])
                self.wts.append(b1_nrn_info[4])

            if not b2_nrn_info == 0:
                b2_mf1 = b2_nrn_info[1] * b2_nrn_info[2]
                b2_mf2 = b2_nrn_info[3] * b2_nrn_info[4]
                self.mfs.append([b2_mf1, b2_mf2])
                self.wts.append(b2_nrn_info[2])
                self.wts.append(b2_nrn_info[4])

            if not b3_nrn_info == 0:
                b3_mf1 = b3_nrn_info[1] * b3_nrn_info[2]
                b3_mf2 = b3_nrn_info[3] * b3_nrn_info[4]
                self.mfs.append([b3_mf1, b3_mf2])
                self.wts.append(b3_nrn_info[2])
                self.wts.append(b3_nrn_info[4])

            if len(self.mfs) > 0:
                weights = sum(self.wts)
                rule_inputs = list(itertools.product(*self.mfs))
                number_of_wordbags = len(self.mfs)
                number_of_rules = len(rule_inputs)
                number_of_weights = len(self.wts)
                weight_factor = (number_of_wordbags * number_of_rules) / number_of_weights
                weights *= weight_factor
                rule_inputs = sum([sum(r) for r in rule_inputs])
                self.defuzzifyBigrams(bigram, rule_inputs, weights, info)

        # ****************** TRIGRAMS *******************
        for info, trigram, in tf_idf_trigram_list.iteritems():
            try:
                t1_nrn_info = t1.get(trigram, 0)
                t2_nrn_info = t2.get(trigram, 0)
                t3_nrn_info = t3.get(trigram, 0)

            except KeyError:
                continue

            self.mfs = []  # membership functions
            self.wts = []  # weights

            if not t1_nrn_info == 0:
                t1_mf1 = t1_nrn_info[1] * t1_nrn_info[2]
                t1_mf2 = t1_nrn_info[3] * t1_nrn_info[4]
                self.mfs.append([t1_mf1, t1_mf2])
                self.wts.append(t1_nrn_info[2])
                self.wts.append(t1_nrn_info[4])

            if not t2_nrn_info == 0:
                t2_mf1 = t2_nrn_info[1] * t2_nrn_info[2]
                t2_mf2 = t2_nrn_info[3] * t2_nrn_info[4]
                self.mfs.append([t2_mf1, t2_mf2])
                self.wts.append(t2_nrn_info[2])
                self.wts.append(t2_nrn_info[4])

            if not t3_nrn_info == 0:
                t3_mf1 = t3_nrn_info[1] * t3_nrn_info[2]
                t3_mf2 = t3_nrn_info[3] * t3_nrn_info[4]
                self.mfs.append([t3_mf1, t3_mf2])
                self.wts.append(t3_nrn_info[2])
                self.wts.append(t3_nrn_info[4])

            if len(self.mfs) > 0:
                weights = sum(self.wts)
                rule_inputs = list(itertools.product(*self.mfs))
                number_of_wordbags = len(self.mfs)
                number_of_rules = len(rule_inputs)
                number_of_weights = len(self.wts)
                weight_factor = (number_of_wordbags * number_of_rules) / number_of_weights
                weights *= weight_factor
                rule_inputs = sum([sum(r) for r in rule_inputs])
                self.defuzzifyTrigrams(trigram, rule_inputs, weights, info)

        # ****************** FOURGRAMS *******************
        for info, fourgram, in tf_idf_fourgram_list.iteritems():
            try:
                f1_nrn_info = f1.get(fourgram, 0)

            except KeyError:
                continue

            self.mfs = []  # membership functions
            self.wts = []  # weights

            if not f1_nrn_info == 0:
                f1_mf1 = f1_nrn_info[1] * f1_nrn_info[2]
                f1_mf2 = f1_nrn_info[3] * f1_nrn_info[4]
                self.mfs.append([f1_mf1, f1_mf2])
                self.wts.append(f1_nrn_info[2])
                self.wts.append(f1_nrn_info[4])

            if len(self.mfs) > 0:
                weights = sum(self.wts)
                rule_inputs = list(itertools.product(*self.mfs))
                number_of_wordbags = len(self.mfs)
                number_of_rules = len(rule_inputs)
                number_of_weights = len(self.wts)
                weight_factor = (number_of_wordbags * number_of_rules) / number_of_weights
                weights *= weight_factor
                rule_inputs = sum([sum(r) for r in rule_inputs])
                self.defuzzifyFourgrams(fourgram, rule_inputs, weights, info)

        # ****************** FIVEGRAMS *******************
        for info, fivegram, in tf_idf_fivegram_list.iteritems():
            try:
                p1_nrn_info = p1.get(fivegram, 0)

            except KeyError:
                continue

            self.mfs = []  # membership functions
            self.wts = []  # weights

            if not p1_nrn_info == 0:
                p1_mf1 = p1_nrn_info[1] * p1_nrn_info[2]
                p1_mf2 = p1_nrn_info[3] * p1_nrn_info[4]
                self.mfs.append([p1_mf1, p1_mf2])
                self.wts.append(p1_nrn_info[2])
                self.wts.append(p1_nrn_info[4])

            if len(self.mfs) > 0:
                weights = sum(self.wts)
                rule_inputs = list(itertools.product(*self.mfs))
                number_of_wordbags = len(self.mfs)
                number_of_rules = len(rule_inputs)
                number_of_weights = len(self.wts)
                weight_factor = (number_of_wordbags * number_of_rules) / number_of_weights
                weights *= weight_factor
                rule_inputs = sum([sum(r) for r in rule_inputs])
                self.defuzzifyFivegrams(fivegram, rule_inputs, weights, info)

    def defuzzifyUnigrams(self, word, rule_inputs, weights, info):
        cog = rule_inputs / weights
        self.word_list.append(word)
        self.cog_list.append(cog)
        self.word_info[info] = word

    def defuzzifyBigrams(self, bigram, rule_inputs, weights, info):
        cog = rule_inputs / weights
        #print bigram, tf_idf, cog
        self.bigram_list.append(bigram)
        self.cog_list_bigrams.append(cog)
        self.bigram_info[info] = bigram

    def defuzzifyTrigrams(self, trigram, rule_inputs, weights, info):
        cog = rule_inputs / weights
        self.trigram_list.append(trigram)
        self.cog_list_trigrams.append(cog)
        self.trigram_info[info] = trigram

    def defuzzifyFourgrams(self, fourgram, rule_inputs, weights, info):
        cog = rule_inputs / weights
        self.fourgram_list.append(fourgram)
        self.cog_list_fourgrams.append(cog)
        self.fourgram_info[info] = fourgram

    def defuzzifyFivegrams(self, fivegram, rule_inputs, weights, info):
        cog = rule_inputs / weights
        self.fivegram_list.append(fivegram)
        self.cog_list_fivegrams.append(cog)
        self.fivegram_info[info] = fivegram

    def normCOGUnigrams(self):
        for k, v in self.word_info.iteritems():
            print k, v

        if not len(self.cog_list) < 1:
            self.max_cog = max(self.cog_list)
            self.cog_list = [cog / self.max_cog for cog in self.cog_list]
            word_rank = dict(zip(self.word_list, self.cog_list))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** UNIGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                self.uni_gram_lv_list = []
                self.uni_gram_lv_list.append(item[1])  # item[1] --> PI score
                for info, word in self.word_info.iteritems():
                    if item[0] == word:
                        print info
                        self.uni_gram_lv_list.append(info)
                NeuroFuzzySystem.PI_bundle_unigrams[item[0]] = self.uni_gram_lv_list

        else:
            print '*********** UNIGRAMS ***********'
            print None

    def normCOGBigrams(self):
        if not len(self.cog_list_bigrams) < 1:
            print self.cog_list_bigrams
            max_cog = max(self.cog_list_bigrams)
            self.cog_list_bigrams = [cog / max_cog for cog in self.cog_list_bigrams]
            word_rank = dict(zip(self.bigram_list, self.cog_list_bigrams))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** BIGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                self.bi_gram_lv_list = []
                self.bi_gram_lv_list.append(item[1])
                for info, bigram in self.bigram_info.iteritems():
                    if item[0] == bigram:
                        print info
                        self.bi_gram_lv_list.append(info)
                NeuroFuzzySystem.PI_bundle_bigrams[item[0]] = self.bi_gram_lv_list
        else:
            print '*********** BIGRAMS ***********'
            print None

    def normCOGTrigrams(self):
        if not len(self.cog_list_trigrams) < 1:
            max_cog = max(self.cog_list_trigrams)
            self.cog_list_trigrams = [cog / max_cog for cog in self.cog_list_trigrams]
            word_rank = dict(zip(self.trigram_list, self.cog_list_trigrams))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** TRIGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                self.tri_gram_lv_list = []
                self.tri_gram_lv_list.append(item[1])
                for info, trigram in self.trigram_info.iteritems():
                    if item[0] == trigram:
                        print info
                        self.tri_gram_lv_list.append(info)
                NeuroFuzzySystem.PI_bundle_trigrams[item[0]] = self.tri_gram_lv_list
        else:
            print '*********** TRIGRAMS ***********'
            print None

    def normCOGFourgrams(self):
        if not len(self.cog_list_fourgrams) < 1:
            max_cog = max(self.cog_list_fourgrams)
            self.cog_list_fourgrams = [cog / max_cog for cog in self.cog_list_fourgrams]
            word_rank = dict(zip(self.fourgram_list, self.cog_list_fourgrams))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** FOURGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                self.four_gram_lv_list = []
                self.four_gram_lv_list.append(item[1])
                for info, fourgram in self.fourgram_info.iteritems():
                    if item[0] == fourgram:
                        print info
                        self.four_gram_lv_list.append(info)
                NeuroFuzzySystem.PI_bundle_fourgrams[item[0]] = self.four_gram_lv_list
        else:
            print '*********** FOURGRAMS ***********'
            print None

    def normCOGFivegrams(self):
        if not len(self.cog_list_fivegrams) < 1:
            max_cog = max(self.cog_list_fivegrams)
            self.cog_list_fivegrams = [cog / max_cog for cog in self.cog_list_fivegrams]
            word_rank = dict(zip(self.fivegram_list, self.cog_list_fivegrams))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** FIVEGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                self.five_gram_lv_list = []
                self.five_gram_lv_list.append(item[1])
                for info, fivegram in self.fivegram_info.iteritems():
                    if item[0] == fivegram:
                        print info
                        self.five_gram_lv_list.append(info)
                NeuroFuzzySystem.PI_bundle_fivegrams[item[0]] = self.four_gram_lv_list
        else:
            print '*********** FIVEGRAMS ***********'
            print None