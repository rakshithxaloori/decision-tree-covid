import copy
import math


class Decision_Tree:
    attr_value_dict = dict()
    target_values = list()
    tree = dict()
    depth_reached = 0

    def __init__(self, tre, depth, pruning_bool):
        self.tre = tre
        self.max_depth = depth
        self.pruning_bool = pruning_bool

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
        for eg in s:
            for value in self.attr_value_dict[attr]:
                if value not in split_lists.keys():
                    split_lists[value] = list()
                if eg[0][attr] == value:
                    # Pop the attr, not needed anymore
                    new_eg = copy.deepcopy(eg)
                    if pop:
                        new_eg[0].pop(attr)
                    split_lists[value].append(new_eg)

        return split_lists

    def id3(self):
        """ Given a set of examples, returns a decision tree. """
        # Create a root node.
        # Base case
        if (len(self.tre[0][0].keys()) == 0) or (self.max_depth == 0):
            # No attributes
            self.tree = self.most_freq(self.tre)
            return

        # Base case if all TEs are same
        same = True
        first_target_val = self.tre[0][1]
        for eg in self.tre:
            if eg[1] != first_target_val:
                same = False
                break

        if same:
            self.tree = first_target_val
            return

        # Build the tree
        node_attr = self.best_attr(self.tre)
        tree = dict()
        tree[node_attr] = list()

        # Split the set with values of the attr
        for key, value in self.split_node(self.tre, node_attr).items():
            tree[node_attr].append((key, self.id3_tree(value, 1)))

        self.tree = tree

    def id3_tree(self, s, current_depth):
        """ Return a decision tree. """
        # Keep track of depth reached
        if self.depth_reached < current_depth:
            self.depth_reached = current_depth

        # Base case
        if len(s[0][0].keys()) == 0 or ((current_depth == self.max_depth) and (self.max_depth != -1)):
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

        best_attr = self.best_attr(s)
        if self.pruning_bool and self.pruning(s, best_attr):
            return self.most_freq(s)

        # Recursive algorithm
        tree = dict()
        tree[best_attr] = list()
        for key, value in self.split_node(s, best_attr).items():
            if len(value) == 0:
                tree[best_attr].append((key, self.most_freq(s)))
            else:
                tree[best_attr].append(
                    (key, self.id3_tree(value, current_depth+1)))

        return tree

    def expected_value(self, attr, attr_val_list):
        """ Return the expected value of attr in s. """
        prob_dict = dict()
        for each_val_pos in self.attr_value_dict[attr]:
            prob_dict[each_val_pos] = 0

        for each_val in attr_val_list:
            prob_dict[each_val] += 1

        expected_value = 0
        for val, val_count in prob_dict.items():
            expected_value += (val_count/len(attr_val_list))*(val)

        return expected_value

    def pruning(self, s, attr):
        """ Return the best tree by performing statistical test pre-pruning. """
        # Performing a chi-square statistic
        # Create a list of values with attr in s
        attr_val_list = list()
        for eg in s:
            attr_val_list.append(eg[0][attr])

        expected_value = self.expected_value(attr, attr_val_list)
        chi_sqr = 0
        for each_val in attr_val_list:
            chi_sqr += (each_val - expected_value) * \
                (each_val - expected_value)/expected_value

        # When the chi-square value is low, return True(prune), else return False(don't prune)
        chi_square_threshold = 1.65
        return (chi_sqr > chi_square_threshold)

    def test_eg(self, eg):
        """ Test and return True/False if the eg matches and doesn't respectively. """
        tree = copy.deepcopy(self.tree)

        while (type(tree) == dict):
            # Iterate until leaf node is reached
            attr = list(tree.keys())[0]
            for pair in list(tree.values())[0]:
                if eg[0][attr] == pair[0]:
                    # If the attribute matches, proceed along that sub-tree
                    tree = pair[1]
                    break

        if tree == eg[1]:
            return True
        else:
            return False

    def test_accuracy(self, tee):
        """ Test the accuracy of the model with the tee set. """
        count_true = 0
        count_false = 0

        for eg in tee:
            if self.test_eg(eg) is True:
                count_true += 1
            else:
                count_false += 1

        accuracy = (float(count_true))/(count_true+count_false)
        return accuracy

    def sub_tree_str(self, tree, level, add_str):
        if type(tree) != dict:
            return "\t"*level+'( '+add_str+' )'+' '+'( target = '+repr(tree)+' )'+"\n"
        ret = "\t"*level+'( '+add_str+' )'+repr(list(tree.keys())[0])+"\n"
        for child in list(tree.values())[0]:
            ret += str(self.sub_tree_str(child[1], level+1,
                                         str(list(tree.keys())[0]) + ' = ' + str(child[0])))
        return ret

    def __str__(self, level=0):
        if self.max_depth == 0:
            return(str(self.tree))
        ret = "\t"*level+repr(list(self.tree.keys())[0])+"\n"
        for child in list(self.tree.values())[0]:
            ret += str(self.sub_tree_str(child[1], level+1, str(
                list(self.tree.keys())[0]) + ' = ' + str(child[0])))
        return ret

    def __repr__(self):
        return '<tree node representation>'
