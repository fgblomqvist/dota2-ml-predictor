import os
import json
import numpy as np
from sklearn.model_selection import train_test_split

# regions
US = 0
EU = 1
RU = 2
AU = 3
AS = 4
SA = 5
ZA = 6

# cluster-to-region mappings
cluster_map = {
    111: US,
    112: US,
    114: US,
    121: US,
    122: US,
    123: US,
    124: US,
    131: EU,
    132: EU,
    133: EU,
    134: EU,
    135: EU,
    136: EU,
    137: EU,
    138: EU,
    142: AS,
    143: AS,
    144: AS,
    145: AS,
    151: AS,
    152: AS,
    153: AS,
    154: AS,
    155: AS,
    156: AS,
    161: AS,
    163: AS,
    171: AU,
    172: AU,
    181: RU,
    182: RU,
    183: RU,
    184: RU,
    185: EU,
    186: EU,
    187: EU,
    188: EU,
    191: RU,
    192: EU,
    193: EU,
    200: SA,
    201: SA,
    202: SA,
    204: SA,
    211: ZA,
    212: ZA,
    213: ZA,
    221: AS,
    222: AS,
    223: AS,
    224: AS,
    227: AS,
    225: AS,
    231: AS,
    232: AS,
    241: SA,
    242: SA,
    251: SA,
}

# column names of the data output
data_format = [
    'winning_team', 'game_duration',
    'region_us', 'region_eu', 'region_ru', 'region_au', 'region_as', 'region_sa', 'region_za',
    'rad_str', 'rad_agi', 'rad_int',
    'dir_str', 'dir_agi', 'dir_int',
] + [('hero_' + str(i)) for i in range(1, 115)]


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
                if match['lobby_type'] != 7 or match['duration'] < 10 * 60:
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

    train, test = train_test_split(samples, test_size=10000, random_state=42)

    write_data(train, train_output)
    write_data(test, test_output)


# Data output format #
# 0: Team that won. -1 for dire, 1 for radiant.
# 1: Game duration. -1 if shorter than 40 min, 1 if equal or longer.
# 2-8: Server region. In which region the game was played.
# 9-11: How many STR, AGI, INT heroes Radiance has.
# 12-14: How many STR, AGI, INT heroes Dire has.
# 15-128: Which heroes were picked. 1 for radiant and -1 dire.
# There are only 113 heroes in DOTA 2, but one ID is unused. To make usage simpler,
# the unused id is allocated but always left as 0, therefore not really impacting the results.
def parse_match_details(match):
    data = ['0'] * 129

    if match['radiant_win']:
        data[0] = '1'
    else:
        data[0] = '-1'

    if match['duration'] < (60 * 40):
        data[1] = '-1'
    else:
        data[1] = '1'

    region = [0] * 7
    region[cluster_map[match['cluster']]] = 1

    # 0 = str, 1 = agi, 2 = int
    rad = [0] * 3
    dire = [0] * 3

    for player in match['players']:

        hero_id = int(player['hero_id'])

        t = get_hero_type(hero_id)

        if int(player['player_slot']) + 2 ** 8 >> 7 & 1:
            team = '-1'
            dire[t] += 1
        else:
            team = '1'
            rad[t] += 1

        # the heroes have an ID from 1 and onwards
        data[14 + hero_id] = team

    data[2:9] = region
    data[9:12] = rad
    data[12:15] = dire

    return data


def write_data(data, file):
    with open(file, "w+") as output:
        output.write(','.join(data_format) + '\n')
        for entry in data:
            output.write(','.join(str(x) for x in entry) + '\n')


def get_hero_type(hero_id):
    strength = [2, 7, 8, 14, 16, 18, 19, 23, 28, 29, 38, 42, 49, 51, 54, 57, 59, 60, 69, 71, 73, 77, 78, 81, 83, 85,
                91, 96, 97, 98, 99, 100, 102, 103, 104, 107, 108, 110]
    agility = [4, 6, 9, 10, 11, 12, 15, 20, 32, 35, 40, 41, 44, 46, 47, 48, 56, 61, 62, 63, 67, 70, 72, 80, 82, 88,
               89, 93, 94, 95, 106, 109, 113, 114]
    intelligence = [1, 3, 5, 13, 17, 21, 22, 25, 26, 27, 30, 31, 33, 34, 36, 37, 39, 43, 45, 50, 52, 53, 55, 58, 64,
                    65, 66, 68, 74, 75, 76, 79, 84, 86, 87, 90, 92, 101, 105, 111, 112]

    if hero_id in strength:
        return 0
    elif hero_id in agility:
        return 1
    elif hero_id in intelligence:
        return 2
