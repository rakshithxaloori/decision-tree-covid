import sys
import csv
import math
import random


from decision_tree import Decision_Tree


def discretise_target(value):
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
    if len(sys.argv) != 4:
        sys.exit("Usage: python3 runner.py csv_file_path depth pruning")

    csv_path = sys.argv[1]
    depth = int(sys.argv[2])
    pruning_string = sys.argv[3]
    if pruning_string == "True":
        pruning = True
    elif pruning_string == "False":
        pruning = False
    else:
        sys.exit("Pruning is either True/False")

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
                discretise_target(row[4])
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

    decision_tree = Decision_Tree(tre, depth, pruning)
    print("DECISION TREE")
    print(decision_tree.tree)
    print("MAXIMUM DEPTH REACHED")
    print(decision_tree.depth_reached)
    print("ACCURACY OVER TESTING")
    print(decision_tree.test_accuracy(tee)*100, "%")
