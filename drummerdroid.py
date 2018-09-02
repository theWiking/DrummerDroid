"""
This is main function of parser
use this to start program
"""
import argparse
from resource import __version__
from scripts.full.pattern_drum import Pattern


def patter_drum(kwargs):
    pattern = Pattern(['kick', 'snare'])
    pattern.prepere_date(sample_len=kwargs['time_samples'], patten_len=kwargs['length_pattern'])
    pattern.read_pattern()
    pattern.preper_midi(1,1)
    pattern.save_date(kwargs['path_save_midi'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Drummer Droid: " + __version__)
    parser.add_argument('-ts', '--time-samples', type=int, default=10)
    parser.add_argument('-ps', '--path-save-midi')
    parser.add_argument('-lp', '--length-pattern', type=int, default=30)
    parser.add_argument('-m', '--metrum', default=4, type=int, choices=[3, 4, 6, 8],
                        help='there is only options 3,4,6,8')
    parser.add_argument('-a','--actens',type=bool)

    args = parser.parse_args()
    print(vars(args))
    patter_drum(vars(args))
