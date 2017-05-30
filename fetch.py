import os
import time
import requests
from ratelimit import rate_limited

steam_api = 'https://api.steampowered.com/IDOTA2Match_570'


def fetch(directory, api_key):

    next_match = "2787914098"

    while True:
        last_saved = save_matches(directory, next_match, api_key)
        next_match = str(int(last_saved) + 1)

        print('Last match was #{}'.format(last_saved))


def save_matches(directory, start_num, api_key):
    params = {
        'start_at_match_seq_num': start_num,
        'key': api_key
    }

    r = call_api('/GetMatchHistoryBySequenceNum/V001/', params)

    if r.json()['result']['status'] != 1:
        print('API returned status code ' + r.json()['result']['status'])
        exit(1)

    file = os.path.join(directory, '{}-TBA.json'.format(start_num))
    # save the json to a file
    with open(file, "a") as output:
        output.write(r.text)

    # get the last match id
    last_saved = r.json()['result']['matches'][-1]['match_seq_num']

    # rename the file to include the last match id
    os.rename(file, os.path.join(directory, '{}-{}.json'.format(start_num, last_saved)))

    return last_saved


@rate_limited(1, 1.5)
def call_api(path, params):
    r = requests.get(steam_api + path, params=params)

    # make sure we're not processing the requests too fast
    if r.status_code == 429:
        # take a break
        print("Sent too many requests, taking a break for 10 seconds")
        time.sleep(10)
        return call_api(path, params)

    return r