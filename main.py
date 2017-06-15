import os
import sys

from coefs import coefs
from fetch import fetch
from compile_data import compile_data
from heroes import save_hero_data
from predict import predict
from train import train
from winrates import get_winrates

steam_api = 'https://api.steampowered.com/IDOTA2Match_570'


def main():

    if 'STEAM_API_KEY' in os.environ:
        api_key = os.environ['STEAM_API_KEY']
    else:
        api_key = ''

    if sys.argv[1] == 'fetch':

        if 'STEAM_API_KEY' not in os.environ:
            print("STEAM_API_KEY environment variable not set")
            return

        fetch('matches/', api_key)

    elif sys.argv[1] == 'compile':
        compile_data('matches/', 'train.csv', 'test.csv')

    elif sys.argv[1] == 'train':
        iterations = [int(x) for x in sys.argv[2].split(',')]
        train('train.csv', 'test.csv', 'ml.model', iterations)

    elif sys.argv[1] == 'predict':
        predict(sys.argv[2])

    elif sys.argv[1] == 'coefs':
        coefs(sys.argv[2])

    elif sys.argv[1] == 'winrates':
        get_winrates()

    elif sys.argv[1] == 'heroes':
        save_hero_data('data/heroes.json', api_key, 'data/winrates.json')


main()
