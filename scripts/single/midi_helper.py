from midiutil import MIDIFile
import sys
from copy import deepcopy as dcp

import mido

class MidiPlayer:

    def __init__(self):
        pass

    def load_file_midi(self, path):
        self.__name=path
        #mido.get_output_names()

        pass

    def load_samples(self, name_note, path):
        pass

    def play(self):
        pass




class MidiHelper:
    # drum channel
    __channel = 9
    __drum_dict = {'kick': 36, 'snare': 38, 'hi_close': 42, 'hi_open': 46}
    # __note_dict =
    __len_dict = {'full': 4, 'half': 2, 'quarter': 1, 'eighth': 0.5, 'sixteenth': 0.25}
    __vel_dict = {'ppp': 16, 'pp': 33, 'p': 49, 'mp': 64, 'mf': 80, 'f': 96, 'ff': 112, 'fff': 127}
    __current_time = 0
    __duration_last_note = 0

    def __init__(self):
        self.__midi = MIDIFile(numTracks=1, adjust_origin=False, file_format=0, deinterleave=True)
        # self.__midi.addChannelPressure(tracknum=0, channel=self.__channel, time=0)
        self.__midi.addProgramChange(tracknum=0, channel=self.__channel, program=115, time=0)
        pass

    def load_sample(self):
        pass

    def get_current_time(self):
        return self.__current_time

    def get_duration_last_note(self):
        return self.__duration_last_note

    def get_dict_duration(self):
        return self.__len_dict

    def add_cymbals(self,metrum,actents):
        full_len = dcp(self.__current_time)
        print(full_len)

    def make_midi(self):
        pass

    def set_tempo(self,tempo):
        #self.__midi.addTempo(time=0, track=0, tempo=int(tempo))
        pass

    def put_note(self, name_note, rest_time, length, volume='mf'):
        self.__duration_last_note = self.__len_dict[length]

        self.__midi.addNote(track=0,
                            channel=self.__channel,
                            pitch=self.__drum_dict[name_note],
                            time=self.__current_time + rest_time,
                            duration=self.__len_dict[length],
                            volume=self.__vel_dict[volume])
        self.__current_time = self.__current_time + self.__duration_last_note + rest_time
        pass

    def save_midi(self, name):
        print('save')
        with open(name + ".mid", 'wb') as output_file:
            self.__midi.writeFile(output_file)
        pass
