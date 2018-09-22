from midiutil import MIDIFile
import sys
from copy import deepcopy as dcp


class MidiHelper:
    __channel = 9
    __drum_dict = {'kick': 36, 'snare': 38, 'hi_close': 42, 'hi_open': 46}
    __len_dict = {'full': 4, 'half': 2, 'quarter': 1, 'eighth': 0.5, 'sixteenth': 0.25}
    __vel_dict = {'ppp': 16, 'pp': 33, 'p': 49, 'mp': 64, 'mf': 80, 'f': 96, 'ff': 112, 'fff': 127}
    __current_time = 0
    __duration_last_note = 0

    def __init__(self):
        self.__midi = MIDIFile(numTracks=1, file_format=1)
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

    def add_cymbals(self, cymbals_bit, actents):
        if cymbals_bit is not 0:
            full_len = dcp(self.__current_time)
            self.__current_time = 0
            full_len = full_len * cymbals_bit / 4
            if cymbals_bit == 4:
                key = 'quarter'
            elif cymbals_bit == 8:
                key = 'eighth'
            elif cymbals_bit == 16:
                key = 'sixteenth'
            elif cymbals_bit == 2:
                key = 'half'
            for a, note in enumerate(range(int(full_len))):
                if a % cymbals_bit == 0 and actents:
                    self.put_note(name_note='hi_open', rest_time=0, length=key, volume="ff")
                else:
                    self.put_note(name_note='hi_close', rest_time=0, length=key, volume='pp')
        else:
            pass

    def set_tempo(self, tempo):
        print(int(tempo))
        self.__midi.addTempo(time=0, track=0, tempo=int(tempo))

    def put_note(self, name_note, rest_time, length, volume='mf'):
        self.__duration_last_note = self.__len_dict[length]

        self.__midi.addNote(track=0,
                            channel=self.__channel,
                            pitch=self.__drum_dict[name_note],
                            time=self.__current_time + rest_time,
                            duration=self.__len_dict[length],
                            volume=self.__vel_dict[volume])
        self.__current_time = self.__current_time + self.__duration_last_note + rest_time

    def save_midi(self, name):

        with open(name + ".mid", 'wb') as output_file:
            print('save in ' + name)
            self.__midi.writeFile(output_file)
