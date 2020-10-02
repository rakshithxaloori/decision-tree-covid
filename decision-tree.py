import sys
import csv
import random
import math


class Decision_Tree:
    attr_value_dict = dict()
    tree = dict()
    depth_reached = 0

    def __init__(self, tre, depth):
        self.tre = tre
        self.depth = depth

        for attr in tre[0].keys():
            # The discrete values each attribute can take
            self.attr_value_dict[attr] = list()
            for eg[0] in tre:
                if eg[0][attr] not in self.attr_value_dict[attr]:
                    self.attr_value_dict[attr].append(eg[0][attr])

        self.id3()

    def most_freq(self, s):
        """ Return the most frequent label in s. """
        count_dict = dict()
        for eg in s:
            if eg[1] not in count_dict.keys():
                count_dict[eg[1]] = 0
            count_dict[eg[1]] += 1

        return max(count_dict, key=count_dict.get)

    def entropy_gain(self, s, attr):
        """ Entropy gain if attr is chosen as node. """
        # TODO
        pass

    def best_attr(self, s):
        """ Return the best attribute for the set s. """
        # TODO
        pass

    def split_node(self, s, attr):
        """ Return a dict[value] = list, s split about a value of an attr """
        split_lists = dict()
        for eg[0] in tre:
            for value in self.attr_value_dict[attr]:
                if value not in split_lists.keys():
                    split_lists[value] = list()
                if eg[0][attr] == value:
                    # Pop the attr, not needed anymore
                    eg[0].pop(attr)
                    split_lists[value].append(eg[0])

        return split_lists

    def id3(self):
        """ Given a set of examples, returns a decision tree. """
        # Create a root node.
        # TODO base case
        node_attr = self.best_attr(self.tre)
        tree = dict()
        tree[node_attr] = list()
        # Split the set with values of the attr
        for key, value in self.split_node(tre, node_attr).items():
            tree[node_attr].append((key, self.id3_tree(value, 0)))

        self.tree = tree

    def id3_tree(self, s, current_depth):
        """ Return a decision tree. """
        # Keep track of depth reached
        if self.depth_reached < current_depth:
            self.depth_reached = current_depth

        # Base case
        if len(s) == 0 or (current_depth == self.depth and self.depth != -1):
            return self.most_freq(s)

        # Recursive algorithm
        best_attr = self.best_attr(s)
        tree = dict()
        tree[best_attr] = list()
        for key, value in self.split_node(s, best_attr).items():
            if len(value) == 0:
                tree[best_attr].append((key, self.most_freq(s)))
            else:
                tree[best_attr].append(
                    (key, self.id3_tree(value, current_depth+1)))

        return tree

    def pruning(self):
        """ Return the best tree with best accuracy on validation set. """
        # TODO
        pass

    def test_accuracy(self, tee):
        """ Test the accuracy of the model with the tee set. """
        # TODO
        pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 decision-tree.py csv_file_path depth")

    csv_path = sys.argv[1]
    depth = sys.argv[2]
    examples = list()

    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        # Skipping the fields
        next(csv_reader)

        # Extracting the data
        for row in csv_reader:
            # Making the values discrete
            data = (
                {
                    # Choosing month of date
                    "date": row[0].split("/")[0],
                    # log10 of confirmed
                    "confirmed": int(math.log10(int(row[1]))),
                    # log10 of recovered
                    "recovered": int(math.log10(int(row[2]))),
                    # log10 of deaths
                    "deaths": int(math.log10(int(row[3]))),
                }
                # TODO make it discrete
                "increase_rate": (row[4])
            )
            examples.append(data)

    # Shuffling for randomness
    random.shuffle(examples)
    tre = list()
    tee = list()

    # Split the data 80/20
    split_index = (int)((80 / 100) * len(examples))
    tre = examples[:split_index]
    tee = examples[split_index:]

    decision_tree = Decision_Tree(tre, depth)
