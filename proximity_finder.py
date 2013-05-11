#!/usr/bin/env python
from math import fabs, log10
import numpy as np


class ProximityFinder(object):
    def __init__(self, f1, f2):
        """
        unlinked demo class
        trying to create modified PI sheet with linked features and modified PI scores
        matrix computations | algorithm to remove duplicate feature words
        N-gram subset words clash

        @param f1: PI sheet
        @param f2: Modified PI Sheet
        """
        self.f1 = f1
        self.f2 = f2
        self.f2.writerow(['Feature Word', 'Priority Index Old', 'Proximity Score', 'Neighbour', 'Section'])
        self.section_N_grams = []
        self.heads = []
        self.head_clusters = {}

    def readPISheet(self):
        self.f1.next()
        for row in self.f1:
            if len(row[0].split(' ')) == 1 and not '|' in row[3]:
                start_head = str(sum([int(i) for i in row[3].split(' ')[:-2]])) + ' | ' + str(
                    len([int(i) for i in row[3].split(' ')[:-2]]))
                start_tail = [int(i) for i in row[3].split(' ')[-2:]]
                self.section_N_grams.append([row[0], row[1], start_head, start_tail, row[5]])

            if len(row[0].split(' ')) == 2 and row[3].count('|') == 1:
                start_head = str(sum([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]])) + ' | ' + str(
                    len([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]]))
                start_tail = [int(i) for i in row[3].split(' | ')[0].split(' ')[-2:]]
                end_head = sum([int(i) for i in row[3].split(' | ')[1].split(' ')[:-2]])
                end_tail = [int(i) for i in row[3].split(' | ')[1].split(' ')[-2:]]
                self.section_N_grams.append([row[0], row[1], start_head, start_tail, end_head, end_tail, row[5]])

            if len(row[0].split(' ')) == 3 and row[3].count('|') == 2:
                start_head = str(sum([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]])) + ' | ' + str(
                    len([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]]))
                start_tail = [int(i) for i in row[3].split(' | ')[0].split(' ')[-2:]]
                end_head = sum([int(i) for i in row[3].split(' | ')[2].split(' ')[:-2]])
                end_tail = [int(i) for i in row[3].split(' | ')[2].split(' ')[-2:]]
                self.section_N_grams.append([row[0], row[1], start_head, start_tail, end_head, end_tail, row[5]])

            if len(row[0].split(' ')) == 4 and row[3].count('|') == 3:
                start_head = str(sum([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]])) + ' | ' + str(
                    len([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]]))
                start_tail = [int(i) for i in row[3].split(' | ')[0].split(' ')[-2:]]
                end_head = sum([int(i) for i in row[3].split(' | ')[3].split(' ')[:-2]])
                end_tail = [int(i) for i in row[3].split(' | ')[3].split(' ')[-2:]]
                self.section_N_grams.append([row[0], row[1], start_head, start_tail, end_head, end_tail, row[5]])

            if len(row[0].split(' ')) == 5 and row[3].count('|') == 4:
                start_head = str(sum([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]])) + ' | ' + str(
                    len([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]]))
                start_tail = [int(i) for i in row[3].split(' | ')[0].split(' ')[-2:]]
                end_head = sum([int(i) for i in row[3].split(' | ')[4].split(' ')[:-2]])
                end_tail = [int(i) for i in row[3].split(' | ')[4].split(' ')[-2:]]
                self.section_N_grams.append([row[0], row[1], start_head, start_tail, end_head, end_tail, row[5]])

    def subSectionClustering(self):
        for ngram in self.section_N_grams:
            self.heads.append(ngram[2])
        self.heads = list(set(self.heads))
        print self.heads

        for head in self.heads:
            head_cluster = []
            for ngram in self.section_N_grams:
                if head == ngram[2]:
                    head_cluster.append(ngram)
            self.head_clusters[head] = head_cluster

    def buildDistanceMatrix(self):
        print 'Building Distance Matrices ...'
        for head, ngrams in self.head_clusters.iteritems():
            word_indices = []
            stmt_indices = []
            priority_indices = []
            feature_words = []
            sections = []
            dm_w_rows = []
            dm_s_rows = []
            dm_p_rows = []

            for ngram in ngrams:
                word_indices.append(ngram[3][1])
                stmt_indices.append(ngram[3][0])
                priority_indices.append(ngram[1])
                feature_words.append(ngram[0])
                sections.append(ngram[-1])

            word_indices_clone = word_indices
            stmt_indices_clone = stmt_indices
            priority_indices_clone = priority_indices

            for word_index, stmt_index, priority_index in zip(word_indices, stmt_indices, priority_indices):
                dm_w_row = []
                dm_s_row = []
                dm_p_row = []

                for word_index_clone, stmt_index_clone, priority_index_clone in zip(word_indices_clone,
                                                                                    stmt_indices_clone,
                                                                                    priority_indices_clone):
                    dm_w_row.append(
                        fabs(((1 + word_index) * (1 + stmt_index)) - ((1 + word_index_clone) * (1 + stmt_index_clone))))
                    dm_s_row.append(fabs((1 + stmt_index) - (1 + stmt_index_clone)))
                    dm_p_row.append(fabs(float(priority_index) - float(priority_index_clone)))

                dm_w_rows.append(dm_w_row)
                dm_s_rows.append(dm_s_row)
                dm_p_rows.append(dm_p_row)

            dm_w = np.array(dm_w_rows)
            dm_s = np.array(dm_s_rows)
            dm_p = np.array(dm_p_rows)
            #print dm_w
            #print dm_s
            #print dm_p
            prox_mat = []

            for w_dist, s_dist, PI in zip(np.nditer(dm_w), np.nditer(dm_s), np.nditer(dm_p)):
                if PI == 0.0:
                    proximity_score = (
                        (w_dist + len(np.unique(dm_s) * s_dist)) / (dm_w.shape[0] * len(np.unique(dm_s))))
                    prox_mat.append(proximity_score)
                else:
                    proximity_score = ((w_dist + len(np.unique(dm_s) * s_dist)) / (
                        dm_w.shape[0] * len(np.unique(dm_s)))) * log10(10 * PI)
                    prox_mat.append(proximity_score)

            ps = np.array(prox_mat)
            ps = np.reshape(ps, dm_w.shape)
            #print ps

            for r, row in enumerate(ps):
                for i, ele in enumerate(row):
                    if ele == min(row):
                        self.f2.writerow(
                            [feature_words[r], priority_indices[r], 1 - np.min(row), feature_words[i], sections[r]])