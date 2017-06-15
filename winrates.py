import json

from bs4 import BeautifulSoup


def get_winrates():

    with open('data/dotabuff_winrates.html') as f:
        doc = BeautifulSoup(f, 'html.parser')

    heroes_elements = doc.find('div', class_='content-inner').find('table').find('tbody').find_all('tr')
    heroes = {}

    for elem in heroes_elements:
        name = elem.find_all('td')[0]['data-value']
        winrate = float(elem.find_all('td')[2]['data-value'])/100
        heroes[name] = winrate

    with open('data/winrates.json', 'w+') as f:
        json.dump(heroes, f)
