import json

import re
import requests
import time

import sys

steam_api = 'https://api.steampowered.com/IEconDOTA2_570'

special_hero_names = {
    'nevermore': 'shadow_fiend',
    'vengefulspirit': 'vengeful_spirit',
    'windrunner': 'windranger',
    'zuus': 'zeus',
    'necrolyte': 'necrophos',
    'queenofpain': 'queen_of_pain',
    'skeleton_king': 'wraith_king',
    'rattletrap': 'clockwerk',
    'furion': 'natures_prophet',
    'life_stealer': 'lifestealer',
    'doom_bringer': 'doom',
    'obsidian_destroyer': 'outworld_devourer',
    'treant': 'treant_protector',
    'wisp': 'io',
    'centaur': 'centaur_warrunner',
    'magnataur': 'magnus',
    'shredder': 'timbersaw',
    'abyssal_underlord': 'abaddon',
}


def save_hero_data(output, api_key, winrates):
    r = requests.get(steam_api + '/GetHeroes/v1/', params={'key': api_key})

    # retry if key is busy
    if r.status_code == 429:
        print("API Key busy, retrying again in 10 seconds")
        time.sleep(10)
        return save_hero_data(output, api_key, winrates)

    result = json.loads(r.text)

    if result is None or result['result']['status'] != 200:
        print('Wrong status code: ' + result['status'])
        sys.exit(1)

    result = result['result']

    if winrates is None:
        with open(output, 'w+') as f:
            json.dump(result['heroes'], f)
        return

    # integrate winrates into the data
    with open(winrates) as f:
        winrates = json.load(f)

    winrates_sanitized = {}

    # sanitize hero names
    for hero, winrate in winrates.items():
        name = sanitize(hero)
        data = {
            'display_name': hero,
            'winrate': winrate,
        }

        winrates_sanitized[name] = data

    heroes = {}

    # match each hero with it's winrate
    for hero in result['heroes']:
        name = hero['name'].replace('npc_dota_hero_', '')

        if name in special_hero_names:
            name = special_hero_names[name]

        if name in winrates_sanitized:
            heroes[hero['id']] = winrates_sanitized[name]
            heroes[hero['id']]['name'] = name
        else:
            print("Unable to find match for " + name)

    with open(output, 'w+') as f:
        json.dump(heroes, f)


def sanitize(name):
    name = name.replace(' ', '_').lower()
    rx = re.compile('[\W-]+')
    return rx.sub('', name).strip()
