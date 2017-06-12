import pickle

from compile_data import get_hero_type


def predict(model_file):
    with open(model_file, 'rb') as mf:
        clf = pickle.load(mf)

    while True:
        region = input("Region: ")
        rad_heroes = input("Radiance Hero IDs: ").split(' ')
        dir_heroes = input("Dire Hero IDs: ").split(' ')

        rad_heroes = [int(x) for x in rad_heroes]
        dir_heroes = [int(x) for x in dir_heroes]

        data = [0] * 128

        data[0] = -1
        data[1:8] = [1, 0, 0, 0, 0, 0, 0]  #int(region)

        # 0 = str, 1 = agi, 2 = int
        rad = [0] * 3
        dir = [0] * 3

        for hero in rad_heroes:
            t = get_hero_type(hero)
            rad[t] += 1

            # the heroes have an ID from 1 and onwards
            data[13 + hero] = 1

        for hero in dir_heroes:

            t = get_hero_type(hero)
            dir[t] += 1

            # the heroes have an ID from 1 and onwards
            data[7 + hero] = -1

        data[8:11] = rad
        data[11:14] = dir

        print("Before 40 min: ", clf.predict([data]))

        data[0] = 1
        print("After 40 min: ", clf.predict([data]))
