import enchant
from nltk.corpus import stopwords
from nltk.tag import pos_tag


class PronounMapping(object):
    txt_with_linked_pronouns = []

    def __init__(self, tokens, trigrams):
        self.tokens = tokens
        self.trigrams = trigrams

    def properNounGroups(self):
        self.NNP_multi_grams = []
        for trigram_list in self.trigrams:
            for trigram in trigram_list:
                if pos_tag([trigram[0]])[0][1] == 'NNP' and pos_tag([trigram[1]])[0][1] == 'CC' and pos_tag([trigram[2]])[0][1] == 'NNP':
                    self.NNP_multi_grams.append(list(trigram))

    def mapPronouns(self):
        self.zone_start_points = []
        self.zone_end_points = []
        self.tokens_modified = []

        for token in self.tokens:
            lv = [int(t.strip()) for t in token[0].split(',')]
            if not token[1] in [',', '.', ':', ';', '\"', '\'', ' ']:
                self.tokens_modified.append([token[1], lv])

        for i, token in enumerate(self.tokens_modified):
            if pos_tag([token[0]])[0][1] == 'NNP' and not pos_tag([token[0]])[0][0].lower() in stopwords.words(
                    'english') and not (enchant.Dict("en_US")).check(pos_tag([token[0]])[0][0].lower()):
                self.zone_start_points.append(token)
                if not (i - 1) < 0:
                    self.zone_end_points.append(
                        self.tokens_modified[i - 1])  # adding last element as end pivot of last zone
        self.zone_end_points.append(self.tokens_modified[-1])

    def multiGramCheck(self):
        self.group_pronouns = []
        for i, token in enumerate(self.tokens_modified):
            for n_gram in self.NNP_multi_grams:
                # checking for n-gram entity conflict
                if len(n_gram) == 3 and not ((i + 2) > len(self.tokens_modified)):
                    if token[0] == n_gram[0] and self.tokens_modified[i + 1][0] == n_gram[1] and self.tokens_modified[i + 2][0] == n_gram[2]:
                        self.group_pronouns.append([token, self.tokens_modified[i + 1], self.tokens_modified[i + 2]])
        print self.group_pronouns

    def changeZoneStartPoints(self):
        """
            example specific | works only for fight.txt
            has to written for more generic cases

        """
        changed_start_point = []
        for group_NNP in self.group_pronouns:
            self.zone_start_points.remove(group_NNP[0])
            self.zone_end_points.remove(group_NNP[1])
            self.zone_start_points.remove(group_NNP[2])
            changed_start_point.append([group_NNP[0][0] + '_' + group_NNP[2][0], group_NNP[0][1]])
        if len(changed_start_point) > 0:
            self.zone_start_points.append(changed_start_point[0])

    def markZones(self):
        self.zones = []
        for start, end in zip(self.zone_start_points, self.zone_end_points):
            self.zones.append([start[0], start[1], end[1], end[0]])

    def replacePronouns(self):
        self.linked_pronouns = []
        for zone in self.zones:
            z_start = zone[1][0] + (10 * zone[1][1])
            z_end = zone[2][0] + (10 * zone[2][1])
            for token in self.tokens_modified:
                token_ind = token[1][0] + (10 * token[1][1])
                if z_start <= token_ind <= z_end:
                    if pos_tag([token[0]])[0][1] == 'PRP':
                        self.linked_pronouns.append([zone[0], token[1]])

        for linked_pronoun in self.linked_pronouns:
            for i, token in enumerate(self.tokens_modified):
                if linked_pronoun[1] == token[1]:
                    token[0] = linked_pronoun[0]

        # success !! text with replaced pronouns
        print self.tokens_modified
        PronounMapping.txt_with_linked_pronouns = self.tokens_modified



