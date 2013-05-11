from itertools import groupby
import csv


class SectionWiseClustering(object):
    def __init__(self, c, PI_bundle_unigrams, PI_bundle_bigrams, PI_bundle_trigrams, PI_bundle_fourgrams, PI_bundle_fivegrams, section_bundle):

        self.c = c
        self.PI_bundle_unigrams = PI_bundle_unigrams
        self.PI_bundle_bigrams = PI_bundle_bigrams
        self.PI_bundle_trigrams = PI_bundle_trigrams
        self.PI_bundle_fourgrams = PI_bundle_fourgrams
        self.PI_bundle_fivegrams = PI_bundle_fivegrams

        self.section_bundle = section_bundle

        self.section_headers = {}
        self.section_headers_ranges = []

    # Scheme 1 - Scheme | Amber
    def key_scheme_1(self, item):
        """

        @param item: item of section_bundle list
        @return: grouper (pattern required to group section words into phrases)
        """
        # here grouper is a list of location indices (last 3 before last) + last 5 sig tags + len(location vector)
        grouper = [[int(x) for x in item[1].split()[:-1]], [x for x in item[2].split()[-5:]], [len(item[1])]]
        return grouper

    # Scheme 2 - Scheme with heading and normal rags | jidan
    def key_scheme_2(self, item):
        return [int(x) for x in item[1].split()[:3]]

    def findSectionHeaders(self):
        if not len(self.section_bundle) < 1:
            loc_ind = self.section_bundle[-1][1].split(' ')
            loc_sig = self.section_bundle[-1][2].split(' ')
            loc_ind = [int(ind) for ind in loc_ind]

            # check condition for Scheme 1 | inferred from spec_analyser.py

            for i, (ind, tag) in enumerate(zip(loc_ind, loc_sig)):
                if ind >= 0 and tag == 'Sect' and loc_ind[i + 1] == 0 and 'H' in loc_sig[i + 1] and loc_ind[i + 2] == 0 and loc_sig[i + 2] == 'statement' and loc_ind[i + 3] >= 0 and loc_sig[i + 3] == 'word':

                    for k, v in groupby(self.section_bundle, key=self.key_scheme_1):
                        self.section_headers[' '.join(x[0] for x in v)] = [k, v]

                    # no self.section_headers_range_pivots and self.section_headers_ranges here
                    self.clusterUnigramsBySectionScheme1()
                    self.clusterBigramsBySectionScheme1()
                    self.clusterTrigramsBySectionScheme1()
                    self.clusterFourgramsBySectionScheme1()
                    self.clusterFivegramsBySectionScheme1()

            # check condition for Scheme 2 | inferred from spec_analyser.py

            for i, tag in enumerate(loc_sig):
                if tag == 'Sect' and 'heading' in loc_sig[i + 1]:
                    for k, v in groupby(self.section_bundle, key=self.key_scheme_2):
                        self.section_headers[' '.join(str(x) for x in k)] = [' '.join(x[0] for x in v)]
                    self.section_headers_range_pivots = {}
                    for ind, section in self.section_headers.iteritems():
                        self.section_headers_range_pivots[int(ind.split(' ')[2])] = section[0]
                    for ind, section in sorted(self.section_headers_range_pivots.items()):
                        self.section_headers_ranges.append([ind, section])
                    self.clusterUnigramsBySectionScheme2()
                    self.clusterBigramsBySectionScheme2()
                    self.clusterTrigramsBySectionScheme2()
                    self.clusterFourgramsBySectionScheme2()
                    self.clusterFivegramsBySectionScheme2()
        else:
            self.noSectionUnigramsPISheet()

    def noSectionUnigramsPISheet(self):
        self.c.writerow(['Word', 'PI Score', 'Tf-Idf', 'Loc Ind', 'Loc Sig', 'Section'])
        for word, info in self.PI_bundle_unigrams.iteritems():
            self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], 'NA'])
        for bigram, info in self.PI_bundle_bigrams.iteritems():
            self.c.writerow([bigram, info[0], info[1][0], info[1][1], info[1][2], 'NA'])
        for trigram, info in self.PI_bundle_trigrams.iteritems():
            self.c.writerow([trigram, info[0], info[1][0], info[1][1], info[1][2], 'NA'])
        for fourgram, info in self.PI_bundle_fourgrams.iteritems():
            self.c.writerow([fourgram, info[0], info[1][0], info[1][1], info[1][2], 'NA'])
        for fivegram, info in self.PI_bundle_fivegrams.iteritems():
            self.c.writerow([fivegram, info[0], info[1][0], info[1][1], info[1][2], 'NA'])

    # ****************************** Scheme 1 ******************************
    def clusterUnigramsBySectionScheme1(self):
        self.c.writerow(['Word', 'PI Score', 'Tf-Idf', 'Loc Ind', 'Loc Sig', 'Section'])
        for section, ind in self.section_headers.iteritems():
            #print section, ind[0][0], ind[0][0][:-2]
            sec_ind = ' '.join(str(i) for i in ind[0][0][:-2])
            for word, info in self.PI_bundle_unigrams.iteritems():
                if sec_ind in info[1][1] and len(sec_ind.split(' ')) > 3:
                    if not info[1][2].split(' ')[len(sec_ind.split(' '))] == 'Sect':
                        #print word, info[1][1], info[1][2]
                        self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(section) + "'"])

    def clusterBigramsBySectionScheme1(self):
        for section, ind in self.section_headers.iteritems():
            sec_ind = ' '.join(str(i) for i in ind[0][0][:-2])
            for word, info in self.PI_bundle_bigrams.iteritems():
                if sec_ind in info[1][1].split('|')[0]:
                    if not info[1][2].split('|')[0].split(' ')[len(sec_ind.split(' '))] == 'Sect':
                        print word, info[1][1], info[1][2]
                        self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(section) + "'"])

    def clusterTrigramsBySectionScheme1(self):
        for section, ind in self.section_headers.iteritems():
            sec_ind = ' '.join(str(i) for i in ind[0][0][:-2])
            for word, info in self.PI_bundle_trigrams.iteritems():
                if sec_ind in info[1][1].split('|')[0]:
                    if not info[1][2].split('|')[0].split(' ')[len(sec_ind.split(' '))] == 'Sect':
                        self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(section) + "'"])

    def clusterFourgramsBySectionScheme1(self):
        for section, ind in self.section_headers.iteritems():
            sec_ind = ' '.join(str(i) for i in ind[0][0][:-2])
            for word, info in self.PI_bundle_fourgrams.iteritems():
                if sec_ind in info[1][1].split('|')[0]:
                    if not info[1][2].split('|')[0].split(' ')[len(sec_ind.split(' '))] == 'Sect':
                        self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(section) + "'"])

    def clusterFivegramsBySectionScheme1(self):
        for section, ind in self.section_headers.iteritems():
            sec_ind = ' '.join(str(i) for i in ind[0][0][:-2])
            for word, info in self.PI_bundle_fivegrams.iteritems():
                if sec_ind in info[1][1].split('|')[0]:
                    self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(section) + "'"])

    # ****************************** Scheme 2 ******************************
    def clusterUnigramsBySectionScheme2(self):
        self.c.writerow(['Word', 'PI Score', 'Tf-Idf', 'Loc Ind', 'Loc Sig', 'Section'])
        for i, sect in enumerate(self.section_headers_ranges):
            if not (i + 1) > len(self.section_headers_ranges) - 1:
                #print sect[1]
                for word, info in self.PI_bundle_unigrams.iteritems():
                    if sect[0] <= int(info[1][1].split(' ')[2]) < self.section_headers_ranges[i + 1][0]:
                        print word, info[0]
                        self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(sect[1]) + "'"])
                print

        print self.section_headers_ranges[-1][1]
        for word, info in self.PI_bundle_unigrams.iteritems():
            if int(info[1][1].split(' ')[2]) > self.section_headers_ranges[-1][0]:
                print word, info[0]
                self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(self.section_headers_ranges[-1][1]) + "'"])

    def clusterBigramsBySectionScheme2(self):
        for i, sect in enumerate(self.section_headers_ranges):
            if not (i + 1) > len(self.section_headers_ranges) - 1:
                #print sect[1]
                for word, info in self.PI_bundle_bigrams.iteritems():
                    print int((info[1][1].split('|')[0]).split(' ')[2])
                    if sect[0] <= int((info[1][1].split('|')[0]).split(' ')[2]) < self.section_headers_ranges[i + 1][0]:
                        print word, info[0]
                        self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(sect[1]) + "'"])
                print

        print self.section_headers_ranges[-1][1]
        for word, info in self.PI_bundle_unigrams.iteritems():
            if int((info[1][1].split('|')[0]).split(' ')[2]) > self.section_headers_ranges[-1][0]:
                print word, info[0]
                self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(self.section_headers_ranges[-1][1]) + "'"])

    def clusterTrigramsBySectionScheme2(self):
        for i, sect in enumerate(self.section_headers_ranges):
            if not (i + 1) > len(self.section_headers_ranges) - 1:
                #print sect[1]
                for word, info in self.PI_bundle_trigrams.iteritems():
                    if sect[0] <= int((info[1][1].split('|')[0]).split(' ')[2]) < self.section_headers_ranges[i + 1][0]:
                        print word, info[0]
                        self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(sect[1]) + "'"])
                print

        print self.section_headers_ranges[-1][1]
        for word, info in self.PI_bundle_trigrams.iteritems():
            if int((info[1][1].split('|')[0]).split(' ')[2]) > self.section_headers_ranges[-1][0]:
                print word, info[0]
                self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(self.section_headers_ranges[-1][1]) + "'"])

    def clusterFourgramsBySectionScheme2(self):
        for i, sect in enumerate(self.section_headers_ranges):
            if not (i + 1) > len(self.section_headers_ranges) - 1:
                #print sect[1]
                for word, info in self.PI_bundle_fourgrams.iteritems():
                    if sect[0] <= int((info[1][1].split('|')[0]).split(' ')[2]) < self.section_headers_ranges[i + 1][0]:
                        print word, info[0]
                        self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(sect[1]) + "'"])
                print

        print self.section_headers_ranges[-1][1]
        for word, info in self.PI_bundle_fourgrams.iteritems():
            if int((info[1][1].split('|')[0]).split(' ')[2]) > self.section_headers_ranges[-1][0]:
                print word, info[0]
                self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(self.section_headers_ranges[-1][1]) + "'"])

    def clusterFivegramsBySectionScheme2(self):
        for i, sect in enumerate(self.section_headers_ranges):
            if not (i + 1) > len(self.section_headers_ranges) - 1:
                #print sect[1]
                for word, info in self.PI_bundle_fivegrams.iteritems():
                    if sect[0] <= int((info[1][1].split('|')[0]).split(' ')[2]) < self.section_headers_ranges[i + 1][0]:
                        print word, info[0]
                        self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(sect[1]) + "'"])
                print

        print self.section_headers_ranges[-1][1]
        for word, info in self.PI_bundle_fivegrams.iteritems():
            if int((info[1][1].split('|')[0]).split(' ')[2]) > self.section_headers_ranges[-1][0]:
                print word, info[0]
                self.c.writerow([word, info[0], info[1][0], info[1][1], info[1][2], "'" + str(self.section_headers_ranges[-1][1]) + "'"])