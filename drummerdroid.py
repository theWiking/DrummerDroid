"""
This is main function of parser
use this to start program
"""
import argparse
from resource import __version__
from scripts.full.pattern_drum import Pattern

import os


def test_run(kwargs):
    pattern = Pattern(['kick', 'snare'])
    pattern.preper_test_run([os.path.abspath('') + '/data/audio/D.wav', os.path.abspath('') + '/data/audio/G.wav'],
                            os.path.abspath('') + '/data/audio/patt.wav')
    pattern.preper_midi(cymbals_bit=kwargs['metrum'], actents=kwargs["actens"])
    pattern.save_date(os.path.abspath('') + '/output2')


def patter_drum(kwargs):
    pattern = Pattern(['kick', 'snare'])
    pattern.prepere_data(sample_len=kwargs['time_samples'], patten_len=kwargs['length_pattern'])
    pattern.read_pattern()
    pattern.preper_midi(kwargs['metrum'], kwargs['actens'])
    pattern.save_date(kwargs['path_save_midi'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Drummer Droid: " + __version__)
    parser.add_argument('-ts', '--time-samples', type=int, default=10)
    parser.add_argument('-ps', '--path-save-midi')
    parser.add_argument('-lp', '--length-pattern', type=int, default=30)
    parser.add_argument('-m', '--metrum', default=4, type=int, choices=[0, 2, 4, 8, 16],
                        help='there is only options 0, 2, 4, 8, 16')
    parser.add_argument('-a', '--actens', default=False, action="store_true")
    parser.add_argument('--test', default=False, action="store_true")

    args = parser.parse_args()

    if vars(args)["test"]:
        test_run(vars(args))
    else:
        print(vars(args))
        patter_drum(vars(args))
