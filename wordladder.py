from datetime import datetime
import sys, subprocess
import networkx as nx
import matplotlib.pyplot as plt
startTime = datetime.now()

def timestamp():
    return str(datetime.now() - startTime)


class Node(object):
    def __init__(self, data=None, id=None):
        self.data = data
        self.id = id
        self.visited = False
        self.neighbors = dict()

    def printnode(self):
        print('\nPRINTING\nGraph Size:\t' + str(self.graph_size))
        for node in self.nodes:
            print(node)

    def printnode(self):
        print('data:' + '\t\t\t' + str(self.data))
        print('id:' + '\t\t\t\t' + str(self.id))
        print('visited:' + '\t\t' + str(self.visited))
        print('neighbors:' + '\t\t' + str([x for x in self.neighbors.keys()]) + '\n')
        timestamp()
        pass


class Graph(object):
    def __init__(self):
        self.path = []
        self.graph_size = 0
        self.found = False

    def newNode(self, node_data):
        """addNode: Adds a unique new node to an undirected graph, increases graph size"""
        newnode = Node(data=node_data, id=self.graph_size)
        self.graph_size += 1
        return newnode

    def wordladder(self, starting_node, ending_node, wordlist):
        """wordladder: creates a whole path of nodes between one word and another.
        """
        starting_word = str(starting_node.data)
        ending_word = str(ending_node.data)
        self.path.append((starting_node.id,starting_node.data))

        if starting_node.id == 0 and not self.found:
            starting_node.visited = False
        if self.found: return
        if (starting_word == ending_word):
            print('\n[S] MOVING DOWN TO:')
            self.found = True
            starting_node.visited = True
            ending_node.id = self.graph_size
            ending_node.printnode()
        else:
            for word, used in zip(wordlist.keys(), wordlist.values()):
                word_end_delta = self.word_delta(word, ending_word)
                start_word_delta = self.word_delta(starting_word, word)
                if word_end_delta[0] >=1 and start_word_delta[0] == 3 and not used and not self.found:
                    wordlist[word] = True
                    newnode = self.newNode(word)
                    newnode.id = starting_node.id + 1
                    starting_node.neighbors[word] = newnode
                    newnode.neighbors[starting_word] = starting_node
                    sys.setrecursionlimit(sys.getrecursionlimit() + 1)
                    print('MOVING UP TO:')
                    newnode.printnode()
                    self.wordladder(newnode, ending_node, wordlist)
                    print('MOVING DOWN TO:')
                    starting_node.visited = True
                    starting_node.printnode()

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


# This test implements the word ladder problem
def main():
    print()
    startTime = datetime.now()
    ourdictpath = './words2.txt'
    wordlist = dict()
    word1 = 'fool'
    word2 = 'sage'
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
    print('Dictionary Size / Words Used = ' + str(len(g.path)/len(wordlist)))
    print(g.path)

    ourplot = nx.Graph()
    ourplot = nx.circular_layout(g.path)
    ourplot.add_nodes_from(g.path)
    nx.draw_circular(ourplot)



if __name__ == '__main__':
    main()
