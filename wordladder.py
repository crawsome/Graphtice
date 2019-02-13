from datetime import datetime
import sys
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

startTime = datetime.now()


def timestamp():
    return str(datetime.now() - startTime)


class Node(object):
    """your standard node structure"""

    def __init__(self, data=None, id=None):
        self.data = data
        self.id = id
        self.visited = False
        self.neighbors = dict()

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
        self.path = dict()
        self.graph_size = 0
        self.found = False

    def new_node(self, node_data):
        """addNode: Adds a unique new node to an undirected graph, increases graph size"""
        new_node = Node(data=node_data, id=self.graph_size)
        self.graph_size += 1
        return new_node

    def remove_node(self):
        """remove_node"""
        pass

    def wordladder(self, starting_node, ending_node, wordlist):
        """wordladder: creates a whole path of nodes between one word and another.
        This is not efficient, and I would love some input on making it work better
        """
        starting_word = str(starting_node.data)
        ending_word = str(ending_node.data)
        self.path[starting_node.id] = starting_node.data

        if starting_node.id == 0 and not self.found:
            starting_node.visited = False
        if self.found: return
        if (starting_word == ending_word):
            # print('\n[S] MOVING DOWN TO:')
            self.found = True
            # starting_node.visited = True
            ending_node.id = self.graph_size
            # ending_node.printnode()
        else:
            for word, used in zip(wordlist.keys(), wordlist.values()):
                word_end_delta = self.word_delta(word, ending_word)
                start_word_delta = self.word_delta(starting_word, word)
                if word_end_delta[0] >= 1 and start_word_delta[0] == 3 and not used and not self.found:
                    wordlist[word] = True
                    new_node = self.new_node(word)
                    new_node.id = starting_node.id + 1
                    starting_node.neighbors[word] = new_node
                    new_node.neighbors[starting_word] = starting_node
                    sys.setrecursionlimit(sys.getrecursionlimit() + 1)
                    # for debugging / demonstration of algorithm steps
                    # print('MOVING UP TO:')
                    # new_node.printnode()
                    self.wordladder(new_node, ending_node, wordlist)
                    # print('MOVING DOWN TO:')
                    starting_node.visited = True
                    # starting_node.printnode()

    def word_delta(self, word1, word2):
        """returns an integer of how different 2 words are. 4=the same"""
        likeness = 0
        swappable_letter_slot = 0
        for index, letter in enumerate(word1):
            if letter == word2[index]:
                likeness += 1
            else:
                swappable_letter_slot = index
        return likeness, swappable_letter_slot

    def make_graph_layout(self, layout_type):

        pass


# This test implements the word ladder problem
def main(*args):
    # TIMING TIME
    startTime = datetime.now()

    # DATA TIME
    ourdictpath = './words2.txt'
    wordlist = dict()
    word1 = args[0]
    word2 = args[1]
    starting_node = Node(word1)
    starting_node.id = 0
    last_node = Node(word2)
    g = Graph()
    with open(ourdictpath) as f:
        for line in f:
            line = line.strip('\n').lower()
            if len(word1) == len(line):
                wordlist[line] = False
    g.wordladder(starting_node, last_node, wordlist)
    print(str(datetime.now() - startTime))
    print('Total Nodes made:' + str(g.graph_size))
    print('Dictionary Size : ' + str(len(wordlist)) + ' Words Used = : ' + str(len(g.path)))

    # GRAPHING TIME
    # populate our edges for new graph we're about to make
    edges = []
    edgedata = list(g.path.values())
    for index, node in enumerate(edgedata):
        try:
            edges.append(tuple((edgedata[index], edgedata[index + 1])))
        except IndexError:
            # print(edges)
            continue

    # create the graph object, and add our edges to it.
    ourplot = nx.DiGraph()
    ourplot.add_edges_from(edges)

    # make start and finish nodes be green (representative of go) and red (representative of stop)
    distinguished_nodes = {word1: 'g', word2: 'r'}

    # create a color list, set color to all other nodes to yellow
    color_values = [distinguished_nodes.get(node, 'y') for node in ourplot.nodes()]
    green_edges = [edges[0], edges[-1]]

    our_pos = dict()
    our_scale = 2000
    nodecount = len(g.path.values())
    # not needed yet
    # originx = nodecount / 2
    originy = our_scale / 2

    # pos = nx.spring_layout(ourplot, scale=our_scale)
    # This loop replaces the line above ^ since nxgraphs needs more custom layouts!
    for x in range(0, our_scale):
        for y, word in enumerate(g.path.values()):
            # increment our x coordinates evenly
            x = int(x + (our_scale / nodecount))

            # an alternate graph, makes a beautiful helix shape! Make your own!
            # y = np.sin(np.sin(x)) + originy

            # The closest I could get to a pretty sine wave (a correction to a mistake in my flow control maybe?)
            y = np.sin(np.sqrt(x)) + originy

            # add to layout (numpy array) (This is all a layout is!)
            our_pos[word] = np.array([float(x), float(y)])

    nx.draw_networkx_labels(ourplot, our_pos, font_size=8)
    nx.draw_networkx_edges(ourplot, our_pos, edgelist=edges, edge_color='b', arrows=True)
    nx.draw_networkx_edges(ourplot, our_pos, edgelist=green_edges, edge_color='g', arrows=True)
    nx.draw_networkx_nodes(ourplot, our_pos, node_color=color_values, node_size=len(word1) * 75)


    plt.savefig('out.pdf',bbox_inches='tight')
    plt.savefig('out.png')
    plt.show()


if __name__ == '__main__':
    main('fool', 'sage')
