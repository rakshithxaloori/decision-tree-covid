import sys
import csv
import random
import math
import copy


class Decision_Tree:
    attr_value_dict = dict()
    target_values = list()
    tree = dict()
    depth_reached = 0

    def __init__(self, tre, depth):
        self.tre = tre
        self.depth = depth

        for attr in tre[0][0].keys():
            # The discrete values each attribute can take
            self.attr_value_dict[attr] = list()
            for eg in tre:
                if eg[0][attr] not in self.attr_value_dict[attr]:
                    self.attr_value_dict[attr].append(eg[0][attr])

                if eg[1] not in self.target_values:
                    self.target_values.append(eg[1])

        self.id3()

    def most_freq(self, s):
        """ Return the most frequent label in s. """
        count_dict = dict()
        for eg in s:
            if eg[1] not in count_dict.keys():
                count_dict[eg[1]] = 0
            count_dict[eg[1]] += 1

        return max(count_dict, key=count_dict.get)

    def entropy(self, s):
        """ Return the entropy of the set s. """
        target_count = dict()
        for val in self.target_values:
            target_count[val] = 0
        for eg in s:
            target_count[eg[1]] += 1

        entropy = 0
        for count in target_count.values():
            if count == 0:
                continue
            entropy += -(count/len(s))*(math.log2(count/len(s)))

        return entropy

    def entropy_gain(self, s, attr):
        """ Entropy gain if attr is chosen as node. """
        split_nodes = self.split_node(copy.deepcopy(s), attr, pop=False)
        entropy_gain = self.entropy(s)

        for each_value, each_set in split_nodes.items():
            entropy_gain -= ((len(each_set)/len(s))*self.entropy(each_set))

        return entropy_gain

    def best_attr(self, s):
        """ Return the best attribute for the set s. """
        entropy_gain_dict = dict()
        entropy_s = self.entropy(s)
        for each_attr in self.attr_value_dict.keys():
            if each_attr not in s[0][0].keys():
                continue
            entropy_gain_dict[each_attr] = self.entropy_gain(s, each_attr)

        return max(entropy_gain_dict, key=entropy_gain_dict.get)

    def split_node(self, s, attr, pop=True):
        """ Return a dict[value] = list, s split about a value of an attr """
        split_lists = dict()
        for eg in tre:
            for value in self.attr_value_dict[attr]:
                if attr not in eg[0].keys():
                    continue
                if value not in split_lists.keys():
                    split_lists[value] = list()
                if eg[0][attr] == value:
                    # Pop the attr, not needed anymore
                    if pop:
                        eg[0].pop(attr)
                    split_lists[value].append(eg)
                    break

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
        if len(s[0][0].keys()) == 0 or (current_depth == self.depth and self.depth != -1):
            return self.most_freq(s)

        # If all target values are same
        initial_target_value = s[0][1]
        same = True
        for data in s:
            if data[1] != initial_target_value:
                same = False
                break

        if same:
            return initial_target_value

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
        # TODO if accuracy is not good, properly discretise and then do
        pass


def discretise(value):
    # Convert to float
    if len(value) == 0:
        return 1

    value = float(value)

    if value < 2:
        return 1
    elif value < 5:
        return 2
    elif value < 10:
        return 3
    elif value < 15:
        return 4
    else:
        return 5


if __name__ == "__main__":
    if len(sys.argv) != 3:
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
                },
                discretise(row[4])
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
    print(decision_tree.tree)
    print("---------------------------------------")
    print(decision_tree.depth_reached)
