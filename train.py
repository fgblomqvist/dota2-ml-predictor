from sklearn.linear_model import SGDClassifier
import numpy as np


def train(train_file, test_file):
    x, y = load_data(train_file)
    x_test, y_test = load_data(test_file)

    print('Iterations,Train,Test')
    for it in [1, 5, 10, 20, 50, 100, 250, 500, 1000]:
        clf = SGDClassifier(loss='log', penalty='l2', n_iter=it)
        clf.fit(x, y)

        train_score = clf.score(x, y)
        test_score = clf.score(x_test, y_test)

        print('{},{},{}'.format(it, 1.0 - train_score, 1.0 - test_score))


def load_data(data_file):
    y = []
    x = []

    # put into matrices
    with open(data_file) as f:
        lines = [line.rstrip('\n') for line in f]

        for line in lines[1:]:
            line = line.split(",")
            line = [float(i) for i in line]

            y.append(line[0])
            x.append(line[1:])

    x = np.array(x)
    y = np.array(y)

    return x, y
