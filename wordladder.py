from datetime import datetime
import sys
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

startTime = datetime.now()

"""
Graphtice: A word graphing, plotting, charting program
Plots words as nodes, and will traverse nodes. 
Words between 

"""

def timestamp():
    return str(datetime.now() - startTime)


class Node(object):
    """your standard node structure"""

    def __init__(self, data=None, id=None):
        self.data = data
        self.id = id
        self.visited = False
        self.neighbors = []

    def printnode(self):
        """printNode: prints node's data"""
        print('data:' + '\t\t\t' + str(self.data))
        print('id:' + '\t\t\t\t' + str(self.id))
        print('visited:' + '\t\t' + str(self.visited))
        print('neighbors:' + '\t\t' + str([x for x in self.neighbors.keys()]) + '\n')
        timestamp()
        pass


class Graph(object):
    def __init__(self):
        # create the graph object, and add our edges to it.
        self.ourplot = nx.DiGraph()
        self.distinguished_nodes = dict()
        self.path = []
        self.graph = dict()
        self.graph_size = 0
        self.found = False

    def new_node(self, node_data):
        """addNode: Adds a unique new node to an undirected graph, increases graph size"""
        new_node = Node(data=node_data, id=self.graph_size)
        self.graph_size += 1
        return new_node

    def remove_node(self, node_data):
        """remove_node"""
        self.graph[node_data] = None
        self.graph_size -= 1

    def wordladder(self, start, end):
        """wordladder: Traverses our adjacency graph with O(n^2*m)
        """
        # start with our word in our graph
        first_node = self.graph[start]
        first_node.visited = True
        try:
            if start == self.path[0]:
                first_node.visited = False
                print('BACK TO FIRST NODE')
                return
            else:
                print('APPENDING ' + str(start))
                self.path.append(start)
        except IndexError:
            print('INDEXERROR, APPENDING FIRST')
            self.path.append(start)

        # if start is end, exit
        if start == end:
            self.found = True
            self.path.append(end)
            return

        # look for words that are up to
        likeness_dict4, likeness_dict3, likeness_dict2, likeness_dict1 = dict(), dict(), dict(), dict()
        for neighbor in first_node.neighbors:
            next_diff = self.word_likeness(end, neighbor)
            if next_diff == len(start) - 3:
                likeness_dict1[neighbor] = next_diff
            elif next_diff == len(start) - 2:
                likeness_dict2[neighbor] = next_diff
            elif next_diff == len(start) - 1:
                likeness_dict3[neighbor] = next_diff
            elif next_diff == len(start):
                likeness_dict4[neighbor] = next_diff

        for word in likeness_dict4:
            if not self.graph[word].visited and not self.found:
                sys.setrecursionlimit(sys.getrecursionlimit() + 1)
                print('WIN ' + str(len(start)) + ' ' + word)
                self.wordladder(word, end)
                if self.found:
                    return
                else:
                    print('removing ' + str(self.path.pop()))

        for word in likeness_dict3:
            if not self.graph[word].visited and not self.found:
                sys.setrecursionlimit(sys.getrecursionlimit() + 1)
                print('GOOD MATCH ' + str(len(start)) + ' ' + word)
                self.wordladder(word, end)
                if self.found:
                    return
                else:
                    print('removing ' + str(self.path.pop()))

        for word in likeness_dict2:
            if not self.graph[word].visited and not self.found:
                sys.setrecursionlimit(sys.getrecursionlimit() + 1)
                print('OK MATCH ' + str(len(start)) + ' ' + word)
                self.wordladder(word, end)
                if self.found:
                    return
                else:
                    print('removing ' + str(self.path.pop()))

        for word in likeness_dict1:
            if not self.graph[word].visited and not self.found:
                sys.setrecursionlimit(sys.getrecursionlimit() + 1)
                print('MEH MATCH ' + str(len(start)) + ' ' + word)
                self.wordladder(word, end)
                if self.found:
                    return
                else:
                    print('removing ' + str(self.path.pop()))

    def word_likeness(self, word1, word2):
        """returns an integer of how different 2 words are. 4=the same"""
        likeness = 0
        for index, letter in enumerate(word1):
            if letter == word2[index]:
                likeness += 1
        return likeness

    def word_adjacency_graph(self, wordlist):
        """word_adjacency_graph: makes an adjacency graph of every word, and all other words that are at least
        1-character likeness to it
        """
        for word in wordlist.keys():
            self.graph[word] = Node(self.new_node(word))
            self.graph[word].id = self.graph_size + 1
            for proposed_neighbor in wordlist.keys():
                word_likeness = self.word_likeness(word, proposed_neighbor)
                if word_likeness >= 3 and word != proposed_neighbor:
                    # print(word + ' : ' + proposed_neighbor)
                    self.graph[word].neighbors.append(proposed_neighbor)

    def plot_graph(self, graph_layout):
        pass

    def sin_x_layout(self):
        """
        sin_x_layout: creates a custom sin_x networkx graph layout

        :return:
        """
        # GRAPHING TIME
        # populate our edges for new graph we're about to make
        edges = []
        edgedata = list(self.path)
        for index, node in enumerate(edgedata):
            try:
                edges.append(tuple((edgedata[index], edgedata[index + 1])))
            except IndexError:
                # print(edges)
                continue
        self.ourplot.add_edges_from(edges)

        # create a color list, set color to all other nodes to yellow
        color_values = [self.distinguished_nodes.get(node, 'y') for node in self.ourplot.nodes()]
        green_edges = [edges[0], edges[-1]]

        our_pos = dict()
        our_scale = 2000
        nodecount = len(self.path)

        # not needed yet
        # originx = nodecount / 2
        originy = our_scale / 2

        # pos = nx.spring_layout(ourplot, scale=our_scale)
        # This loop replaces the line above ^ since nxgraphs needs more custom layouts!
        for x in range(0, our_scale):
            for y, word in enumerate(self.path):
                # increment our x coordinates evenly
                x = int(x + (our_scale / nodecount))

                # an alternate graph, makes a beautiful helix shape! Make your own!
                # y = np.sin(np.sin(x)) + originy

                # The closest I could get to a pretty sine wave (a correction to a mistake in my flow control maybe?)
                y = np.sin(np.sqrt(x)) + originy

                # add to layout (numpy array) (This is all a layout is!)
                our_pos[word] = np.array([float(x), float(y)])

        nx.draw_networkx_labels(self.ourplot, our_pos, font_size=8)
        nx.draw_networkx_edges(self.ourplot, our_pos, edgelist=edges, edge_color='b', arrows=True)
        nx.draw_networkx_edges(self.ourplot, our_pos, edgelist=green_edges, edge_color='g', arrows=True)
        nx.draw_networkx_nodes(self.ourplot, our_pos, node_color=color_values, node_size=len(self.path[0] * 75))


# This test implements the word ladder problem
def main(*args):
    # TIMING TIME
    startTime = datetime.now()

    # DATA TIME
    ourdictpath = './words2.txt'
    wordlist = dict()
    word1 = args[0]
    word2 = args[1]

    g = Graph()
    g.distinguished_nodes = {word1: 'g', word2: 'r'}
    with open(ourdictpath) as f:
        for line in f:
            line = line.strip('\n').lower()
            if len(word1) == len(line):
                wordlist[line] = False

    # Create our entire adjacency graph, plotted as node neighbors if 1 letter difference.
    g.word_adjacency_graph(wordlist)
    print('Adjacency graph built in time: ' + str(datetime.now() - startTime))
    print(g.graph)

    # Create our path of words from [word1, ... , word2]
    g.wordladder(word1, word2)
    print(g.path)
    print('Wordladder built in time: ' + str(datetime.now() - startTime))

    # Plot our data
    g.sin_x_layout()
    print('Total Nodes made:' + str(g.graph_size))
    print('Dictionary Size : ' + str(len(wordlist)) + ' Words Used = : ' + str(len(g.path)))

    # make start and finish nodes be green (representative of go) and red (representative of stop)
    plt.savefig('out.pdf', bbox_inches='tight')
    plt.savefig('out.png')
    plt.show()


if __name__ == '__main__':
    # will it do the classic word ladder?
    main('fool', 'sage')

    # will it gracefully exit when it finds no path?
    #main('dance', 'falls')

    # will it reliably go a single node? (warning, 3 min graph build on my 7770k
    #main('cancer', 'dancer')


    #main('art','apt')
