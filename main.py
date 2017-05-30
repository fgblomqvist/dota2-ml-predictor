import os
import sys
from fetch import fetch
from compile_data import compile_data
from train import train

steam_api = 'https://api.steampowered.com/IDOTA2Match_570'


def main():

    if sys.argv[1] == 'fetch':

        if 'STEAM_API_KEY' not in os.environ:
            print("STEAM_API_KEY environment variable not set")
            return

        api_key = os.environ['STEAM_API_KEY']

        fetch('matches/', api_key)

    elif sys.argv[1] == 'compile':
        compile_data('matches/', 'dota2matches.csv')

    elif sys.argv[1] == 'train':
        train('train.csv', 'test.csv')


main()
