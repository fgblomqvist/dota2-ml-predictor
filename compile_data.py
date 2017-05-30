import os
import json
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split


def compile_data(directory, train_output, test_output):
    d = os.fsencode(directory)

    wanted = 110000
    gotten = 0

    samples = []
    done = False

    for file in os.listdir(d):
        filename = os.fsdecode(file)

        with open(os.path.join(directory, filename)) as json_file:
            data = json.load(json_file)

            for match in data['result']['matches']:
                if match['lobby_type'] != 7:
                    continue

                match_details = parse_match_details(match)
                samples.append(match_details)

                gotten += 1

                print('Got {}, parsing next file'.format(gotten))

                if gotten >= wanted:
                    done = True
                    break

            if done:
                break

    samples = np.array(samples, dtype=float)
    scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1))
    samples = scaler.fit_transform(samples)

    train, test = train_test_split(samples, test_size=10000, random_state=42)

    write_data(train, train_output)
    write_data(test, test_output)


# Data output format #
# 0: Team that won. -1 for dire, 1 for radiant.
# 1: Game duration. -1 if shorter than 40 min, 1 if equal or longer.
# 2: Server cluster. On which region-specific server the game was played.
# 3-116: Which heroes were picked. 1 for radiant and -1 dire.
# There are only 113 heroes in DOTA 2, but one ID is unused. To make usage simpler,
# the unused id is allocated but always left as 0, therefore not impacting the results.
def parse_match_details(match):
    data = ['0'] * 117

    if match['radiant_win']:
        data[0] = '1'
    else:
        data[0] = '-1'

    if match['duration'] < (60 * 40):
        data[1] = '-1'
    else:
        data[1] = '1'

    data[2] = match['cluster']

    for player in match['players']:

        if int(player['player_slot']) + 2 ** 8 >> 7 & 1:
            team = '-1'
        else:
            team = '1'

        # the heroes have an ID from 1 and onwards
        data[2 + int(player['hero_id'])] = team

    return data


def write_data(data, file):
    with open(file, "w+") as output:
        for entry in data:
            output.write(','.join(str(x) for x in entry) + '\n')
