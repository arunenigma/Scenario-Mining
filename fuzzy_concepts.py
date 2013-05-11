import pygraphviz as pgv
import networkx as nx
import itertools


class FuzzyConcept(object):
    def __init__(self, f1, f1_clone):
        self.f1 = f1
        self.f1_clone = f1_clone
        self.PI_dict = {}
        self.PS_dict = {}

    def normalizeProximityScores(self):
        ps = []
        pi = []
        self.header = self.f1.next()

        for row in self.f1:
            pi.append(float(row[1]))
            ps.append(float(row[2]))

        self.max_ps = max(ps)
        self.min_pi = min(pi)
        self.max_pi = max(pi)
        self.denum = self.max_pi - self.min_pi

    def writeFinalPISheet(self, f2):
        self.pi_dict = {}
        f2.writerow(self.header)
        self.f1_clone.next()
        for row in self.f1_clone:
            if not self.max_pi == self.min_pi:
                f2.writerow(
                    [row[0], (float(row[1]) - self.min_pi) / self.denum, float(row[2]) / self.max_ps, row[3], row[4]])
                self.pi_dict[row[0]] = (float(row[1]) - self.min_pi) / self.denum
            else:
                f2.writerow([row[0], (float(row[1])), float(row[2]) / self.max_ps, row[3], row[4]])
                self.pi_dict[row[0]] = (float(row[1]))


    def find_all_paths(self, graph, start, end):
        path = []
        paths = []
        queue = [(start, end, path)]
        while queue:
            start, end, path = queue.pop()
            #print path
            path = path + [start]
            if start == end:
                paths.append(path)
            for node in set(graph[start]).difference(path):
                queue.append((node, end, path))
        return paths[0]

    def drawConceptGraphs(self, f3, graph):
        f3.next()
        for row in f3:
            # converting all strings to lower case
            self.PI_dict[row[0].lower()] = row[1].lower()
            self.PS_dict[tuple([row[0].lower(), row[3].lower()])] = [row[2], row[4]]
            graph.add_node(row[0].lower(), color='goldenrod2', style='filled', shape='box',
                           xlabel=round(float(row[1]), 2),
                           fontname='calibri')
            graph.add_node(row[3].lower(), color='goldenrod2', style='filled', shape='box',
                           xlabel=round(self.pi_dict.get(row[3]), 2), fontname='calibri')
            graph.add_edge(row[0].lower(), row[3].lower(), color='sienna', style='filled', label=round(float(row[2]), 2),
                           fontname='calibri')

        self.edges = graph.edges()
        g1 = nx.Graph(self.edges)
        self.skeletons = nx.connected_components(g1)[:]
        all_pivots = []

        for skeleton in self.skeletons:
            skeleton_pivots = []
            for node in skeleton:
                if len(graph.predecessors(node)) == 0 and len(graph.successors(node)) == 1:
                    skeleton_pivots.append(node)
                if len(graph.predecessors(node)) == 1 and len(graph.successors(node)) == 0:
                    skeleton_pivots.append(node)
            all_pivots.append(skeleton_pivots)

        self.inference_paths = []

        for skeleton_pivots in all_pivots:
            paths = []
            pairs = list(itertools.combinations(skeleton_pivots, 2))
            for pair in pairs:
                paths.append(self.find_all_paths(graph, pair[0], pair[1]))
            self.inference_paths.append(paths)

        graph.write('graph.dot')
        img = pgv.AGraph(file='graph.dot')  # img = pgv.AGraph('graph.dot') doesn't work | bug in Pygraphviz
        img.layout(prog='dot')
        img.draw('concepts.pdf')
        img.close()