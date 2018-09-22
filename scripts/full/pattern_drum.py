import numpy

from scripts.single.audio_helper import Audio
from scripts.single.midi_helper import MidiHelper


class Pattern:

    def __init__(self, dict_strings):
        self.__audios = []
        for i in range(len(dict_strings)):
            aud = Audio(name=dict_strings[i])
            self.__audios.append(aud)
        self.__pattern_audio = Audio(name="pattern")
        self.__midi_maker = MidiHelper()

    def __del__(self):
        pass

    def preper_test_run(self, path, pattern_path):
        for i in range(len(self.__audios)):
            print(self.__audios[i].get_name())
            self.__audios[i].open_audio(path[i])
            print(numpy.around(self.__audios[i].get_peaks(), 3))
            print(numpy.around(self.__audios[i].get_peaks_in_s(), 3))
            array = self.__audios[i].splits_audio_and_return_notes()
            print(array)
            stri = ''
            for a in array:
                stri = stri + a[0]
            self.most_frequent(stri)
        self.__pattern_audio.open_audio(pattern_path)
        print(self.__pattern_audio.detect_tempo())
        print(numpy.around(self.__pattern_audio.get_peaks(), 3))
        print(len(self.__pattern_audio.get_frames()))
        print(numpy.around(self.__pattern_audio.get_peaks_in_s(), 3))
        self.__pattern_audio.splits_audio_and_return_notes()
        self.__notes_and_timings = self.__pattern_audio.quantization_notes()

    @staticmethod
    def most_frequent(text):
        frequencies = [(c, text.count(c)) for c in set(text)]
        return max(frequencies, key=lambda x: x[1])[0]

    def prepere_date(self, sample_len=10, patten_len=30):

        for i in range(len(self.__audios)):
            print(self.__audios[i].get_name())
            self.__audios[i].record_sample(time_of_recording=sample_len)
            print(numpy.around(self.__audios[i].get_peaks(), 3))
            print(numpy.around(self.__audios[i].get_peaks_in_s(), 3))
            array = self.__audios[i].splits_audio_and_return_notes()
            print(array)
            stri = ''
            for a in array:
                stri = stri + a[0]
            print(self.most_frequent(stri))
        print("record pattern")
        self.__pattern_audio.record_sample(time_of_recording=patten_len)

    def record(self):
        print("start")
        self.__audios[1].record_sample(5)
        print(self.__audios[1].recoginize_freq(self.__audios[1].get_frames()))
        print(self.__audios[1].get_name_note(self.__audios[1].get_the_freq()))

    def read_pattern(self):
        print(self.__pattern_audio.detect_tempo())
        print(numpy.around(self.__pattern_audio.get_peaks(), 3))
        print(len(self.__pattern_audio.get_frames()))

        print(numpy.around(self.__pattern_audio.get_peaks_in_s(), 3))
        self.__pattern_audio.splits_audio_and_return_notes()
        self.__notes_and_timings = self.__pattern_audio.quantization_notes()
        pass

    def preper_midi(self, cymbals_bit, actents):
        self.__midi_maker.set_tempo(self.__pattern_audio.get_tempo())
        for name, value, time in self.__notes_and_timings:
            if name[0] == self.__audios[0].get_name_note()[0]:
                name = 'kick'
            elif name[0] == self.__audios[1].get_name_note()[0]:
                name = 'snare'
            self.__midi_maker.put_note(name_note=name, rest_time=0, length=value)
        self.__midi_maker.add_cymbals(cymbals_bit, actents)

    def save_date(self, path):
        self.__midi_maker.save_midi(path)

