import numpy

from scripts.single.audio_helper import Audio
from scripts.single import signatur_maker
import resource as res


class Pattern:


    def __init__(self, dict_strings):
        self.__audios = []
        for i in range(len(dict_strings)):
            #print(i)
            aud = Audio(name=dict_strings[i])
            self.__audios.append(aud)
            #print(self.__audios[i].get_name())
        self.__pattern_audio = Audio(name="pattern")

    def __del__(self):
        pass

    def load_date(self, path_to_save):
        rc = Audio()
        res.make_folder(path_to_save+"audio\\records\\from_top\\")
        res.make_folder(path_to_save+"audio\\records\\from_down\\")
        """
        print("on down")
        for i in range(0, 10):
            print("start ", i)
            rc.record_sample(path_to_save=path_to_save+"from_top\\"+str(i), time_of_recording=0.5)
            print("end")
        print("from down")
        for i in range(0, 10):
            print("start ", i)
            rc.record_sample(path_to_save=path_to_save+"from_down\\"+str(i), time_of_recording=0.5)
            print("end")
        pass
        """
        res.make_folder(path_to_save+"signatures\\records\\from_top\\")
        res.make_folder(path_to_save+"signatures\\records\\from_down\\")
        sm = signatur_maker.Signature()
        for i in range(0, 10):
            sm.load_audio(path_to_save+"audio\\records\\from_top\\"+str(i)+".wav")
            sm.fft_signature()
            sm.save_signature(path_to_save+"signatures\\records\\from_top\\"+str(i)+".jpg")

        for i in range(0, 10):
            sm.load_audio(path_to_save+"audio\\records\\from_down\\"+str(i)+".wav")
            sm.fft_signature()
            sm.save_signature(path_to_save+"signatures\\records\\from_down\\"+str(i) + ".jpg")

        print("start record fraze")
        #rc.record_sample(path_to_save+"audio\\records\\fraze", time_of_recording=4)

        sm.load_audio(path_to_save+"audio\\records\\fraze.wav")
        sm.fft_signature()
        sm.save_signature(path_to_save+"signatures\\records\\fraze.jpg")

    def prepere_date(self,is_save=None):

        # for i in range(len(self.__audios)):
        #     print(self.__audios[i].get_name())
        #     self.__audios[i].record_sample(time_of_recording=10)
        print(self.__audios[0].recognize_freq2("D:/Projekty/Python/DrummerDroid/date/audio/D.wav"))
        print("in memory***************************")
        self.__audios[0].open_audio("D:/Projekty/Python/DrummerDroid/date/audio/D.wav")
        print(self.__audios[0].recoginize_freq(self.__audios[0].get_frames()))
        print(self.__audios[0].get_name_note(self.__audios[0].get_the_freq()))
        #print(self.__audios[0].get_name_note(self.__audios[0].recognize_freq2("D:/Projekty/Python/DrummerDroid/date/audio/D.wav")))

        # check freq
        pass

    def record(self):
        print("start")
        self.__audios[1].record_sample(5)
        print(self.__audios[1].recoginize_freq(self.__audios[1].get_frames()))
        print(self.__audios[1].get_name_note(self.__audios[1].get_the_freq()))

    def read_pattern(self):

        # record pattern
        # read pattern
        self.__pattern_audio.open_audio("D:/Projekty/Python/DrummerDroid/date/audio/small_pattern.wav")
        # decetect tempo
        print(self.__pattern_audio.detect_tempo())
        # cout picks (print it) and print timings

        print(numpy.around(self.__pattern_audio.get_peaks(), 3))
        print(len(self.__pattern_audio.get_frames()))
        print(numpy.around(self.__pattern_audio.get_peaks_in_s(), 3))
        self.__pattern_audio.splits_audio_and_return_notes()
        # make array of this slices
        # check freq in all slices
        pass

    def save_date(self):
        pass
