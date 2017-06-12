import pickle
from compile_data import data_format


# print out the model coeficients along with which data they are for
def coefs(model_file):
    with open(model_file, 'rb') as mf:
        clf = pickle.load(mf)

    for i, name in enumerate(data_format[1:]):
        print('{}: {}'.format(name, clf.coef_[0][i]))
