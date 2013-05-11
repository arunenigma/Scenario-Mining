class ConceptSkeleton(object):
    def __init__(self, pi_dict, ps_dict, f1, f2, f3, skeletons, inference_paths):
        self.pi_dict = pi_dict
        self.ps_dict = ps_dict
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3

        self.skeletons = skeletons
        self.inference_paths = inference_paths
        self.concepts = {}

    def extractConcepts(self):
        for skeleton, paths in zip(self.skeletons, self.inference_paths):
            if not len(paths) == 0:
                self.concepts[tuple(skeleton)] = paths
            else:
                self.concepts[tuple(skeleton)] = [skeleton]

    def writeOutputsToCsvFiles(self):
        #print self.concepts
        for skeleton, inference_paths in self.concepts.iteritems():
            #print skeleton, inference_paths
            self.f1.writerow([skeleton, inference_paths])
        for node, pi in self.pi_dict.iteritems():
            self.f2.writerow([node, pi])
        for pair, ps_sect in self.ps_dict.iteritems():
            self.f3.writerow([pair[0], pair[1], ps_sect[0], ps_sect[1]])