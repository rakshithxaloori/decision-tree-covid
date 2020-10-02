import sys
import csv
import random


class Decision_Tree:
    # Training set
    tre = []
    # Validation set
    vae = []
    # Testing set
    tee = []

    def __init__(self, tre, vae, tee):
        self.tre = tre
        self.vae = vae
        self.tee = tee


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 decision-tree.py csv_file_path")

    csv_path = sys.argv[1]
    examples = []

    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            # Date,Confirmed,Recovered,Deaths,Increase rate
            examples.append({
                "date": row[0],
                "confirmed": row[1],
                "recovered": row[2],
                "deaths": row[3],
                "increase_rate": row[4]
            })

    # Shuffling for randomness
    random.shuffle(examples)
    tre = []
    vae = []
    tee = []

    # Split the data 80/20
    split_index = (int)((80 / 100) * len(examples))
    tre = examples[:split_index]
    tee = examples[split_index:]

    # Split to training, validation
    split_index = (int)((80 / 100) * len(tre))
    vae = tre[split_index:]
    tre = tre[:split_index]

    decision_tree = Decision_Tree(tre, vae, tee)
