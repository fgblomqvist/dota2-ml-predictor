import os
import json


def compile_data(directory, output_file):

    d = os.fsencode(directory)

    wanted = 110000
    gotten = 0

    with open(output_file, "w+") as output:

        for file in os.listdir(d):
            filename = os.fsdecode(file)

            with open(os.path.join(directory, filename)) as json_file:
                data = json.load(json_file)

                for match in data['result']['matches']:
                    if match['lobby_type'] != 7:
                        continue

                    match_details = parse_match_details(match)
                    output.write(','.join(match_details) + '\n')
                    gotten += 1

                    if gotten >= wanted:
                        return

            print('Got {}, parsing next file'.format(gotten))


# Data output format #
# 0: Team that won. -1 for dire, 1 for radiant.
# 1: Game duration. -1 if shorter than 40 min, 1 if equal or longer.
# 2-115: Which heroes were picked. 1 for radiant and -1 dire.
# There are only 113 heroes in DOTA 2, but one ID is unused. To make usage simpler,
# the unused id is allocated but always left as 0, therefore not impacting the results.
def parse_match_details(match):
    data = ['0'] * 116

    if match['radiant_win']:
        data[0] = '1'
    else:
        data[0] = '-1'

    if match['duration'] < (60 * 40):
        data[1] = '-1'
    else:
        data[1] = '1'

    for player in match['players']:

        if int(player['player_slot']) + 2 ** 8 >> 7 & 1:
            team = '-1'
        else:
            team = '1'

        # the heroes have an ID from 1 and onwards
        data[1 + int(player['hero_id'])] = team

    return data
