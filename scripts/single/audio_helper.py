import math

import pyaudio
import wave
from array import array
import pyaudio
import wave
import numpy as np
from scipy.stats import itemfreq
import copy
import librosa
import struct
from copy import deepcopy as dcp

class Sample:
    """
    Use for pattern small times.
    Create list of this
    """
    __audio = None
    __framerate = 44100
    __name = None
    __frames = None
    __time = None
    __freq = None
    __note = None
    __time_in_audio = None



class Audio:
    __audio = None
    __framerate = 44100
    __name = None
    __frames = None
    __time = None
    __npframe = None
    __dict_freq = {'C': 32.7,
                   'C#': 34.6,
                   'D': 36.7,
                   'D#': 38.9,
                   'E': 41.2,
                   'F': 43.7,
                   'F#': 46.2,
                   'G': 49.0,
                   'G#': 51.9,
                   'A': 55.0,
                   'A#': 58.3,
                   'B': 61.7}

    def __init__(self, name):
        self.__name = name

    def __del__(self):
        pass

    def get_name_note(self, freq):
        """
        note = dcp(self.__dict_freq)
        for key, value in note.items():
            note[key] =abs(freq-(freq / value)*note[key] - (freq % value))
        sorted_d = sorted((value, key) for (key, value) in note.items())
        print(sorted_d)
        """
        return librosa.hz_to_note(freq)

    def get_name(self):
        return self.__name

    def open_audio(self, path_of_audio):
        """
        :path_of_audio
        :returns audio as nparray, framerate
        """
        wf = wave.open(path_of_audio, 'rb')
        self.__sampwidth = wf.getsampwidth()
        self.__frames = wf.readframes(wf.getnframes())
        self.__nframes = wf.getnframes()
        self.__framerate = wf.getframerate()
        return self.__frames, self.__framerate

    def save_audio(self, frames, path_to_save="Record.wav", rate=44100, channels=1):
        print(path_to_save)
        format_audio = pyaudio.paInt16
        audio = pyaudio.PyAudio()
        wave_file = wave.open(path_to_save + ".wav", 'wb')
        wave_file.setnchannels(channels)
        wave_file.setsampwidth(audio.get_sample_size(format_audio))
        wave_file.setframerate(rate)
        wave_file.writeframes(b''.join(frames))  # append frames recorded to file
        wave_file.close()

    def get_frames(self):
        return self.__frames

    def record_sample(self, time_of_recording=15, rate=44100, chunk=1024, channels=1):

        self.__framerate = rate
        format_audio = pyaudio.paInt16
        # instantiate the pyaudio
        audio = pyaudio.PyAudio()
        stream = audio.open(format=format_audio, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
        # Start recording
        frames = []
        while True:
            data = stream.read(chunk)
            data_chunk = array('h', data)
            vol = max(data_chunk)

            if vol >= 250:
                print("start recprd")
                frames.append(data)
                for i in range(0, int(rate / chunk * time_of_recording)):
                    data = stream.read(chunk)
                    # data_chunk = array('h', data)
                    # vol = max(data_chunk)
                    frames.append(data)
                break
        # end of recording
        stream.stop_stream()
        stream.close()
        self.__sampwidth = audio.get_sample_size(format_audio)
        self.__frames = b''.join(frames)
        self.__nframes = len(frames)/self.__sampwidth
        audio.terminate()

        # writing to file
        return frames

    def simple_freq(self, frames=None):
        if frames is not None:
            self.__frames = frames

        return max(itemfreq(self.__frames))

    def get_the_freq(self):
        return self.__freq

    def remove_to_close(self, times, tempo, spaceModificer=20):
        arrayIndex = []
        for i in range(0, len(times) - 1):
            # tempo/20 precysion of slice ->20 bigger make more space
            if times[i + 1] - times[i] < (tempo / spaceModificer):
                arrayIndex.append(i + 1)
        return np.delete(times, arrayIndex)

    def bytes2int(self,str):
        return int(str.encode('hex'), 16)

    def get_peaks(self, frames=None):
        hop_length=512
        if frames is not None:
            self.__frames = frames
        array = librosa.util.buf_to_float(self.__frames)
        self.__npframe = array
        audioNormalizte = librosa.util.normalize(array*5)
        percusive = librosa.effects.percussive(audioNormalizte)
        onset_env = librosa.onset.onset_strength(percusive,self.__framerate,hop_length=hop_length,aggregate=np.median)
        onsetFrames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=self.__framerate)
        tempo, timeBeats = librosa.beat.beat_track(percusive, self.__framerate, start_bpm=60)
        onsetFrames = self.remove_to_close(onsetFrames, tempo, int(math.log(tempo,2)))
        self.__starts_stops=onsetFrames*hop_length*2
        return onsetFrames*hop_length*2

    def splits_audio_and_return_notes(self):
        info = [self.__frames[self.__starts_stops[i]:self.__starts_stops[i+1]]
                for i in range(0, (len(self.__starts_stops)-1))]
        print(info)
        print(len(info))
        for i in range(0, (len(self.__starts_stops)-1)):

            print(self.recoginize_freq(info[i]+info[i]+info[]i))

    def get_peaks_in_s(self, frames=None):
        hop_length=512
        return librosa.frames_to_time(self.get_peaks(frames)/(hop_length*2),self.__framerate)

    def detect_tempo(self, frames=None):
        """
        :param frames: in bytes
        :return: tempo
        """
        if frames is not None:
            self.__frames = frames
        array = librosa.util.buf_to_float(self.__frames)
        self.__npframe = array
        self.__tempo = librosa.beat.tempo(y=array, sr=self.__framerate)
        return self.__tempo

    def get_tempo(self):
        if self.__tempo is not None:
            return -1
        else:
            return self.__tempo

    def recoginize_freq(self, frames=None):
        thefreq = 0
        if frames is not None:
            self.__frames = frames

        seconds = self.__nframes/self.__framerate
        # Window of all sample

        chunk = round(self.__framerate * seconds)
        ####print(chunk)
        # use a Blackman window
        window = np.blackman(chunk)
        # open stream
        p = pyaudio.PyAudio()
        data=self.__frames[0:chunk*self.__sampwidth]
        i=self.__sampwidth
        print(frames)
        while len(data) == chunk*self.__sampwidth:
            #print(str(len(data)) + " == " + str(chunk * self.__sampwidth))
            # unpack the data and times by the hamming window
            indata = np.array(wave.struct.unpack("%dh" % (len(data) / self.__sampwidth), data)) * window
            # Take the fft and square each value
            fftData = abs(np.fft.rfft(indata)) ** 2
            # find the maximum
            which = fftData[1:].argmax() + 1
            # use quadratic interpolation around the max
            if which != len(fftData) - 1:
                y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
                x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                # find the frequency and output it
                thefreq = (which + x1) * self.__framerate / chunk
            else:
                thefreq = which * self.__framerate / chunk
            # read some more data
            data=self.__frames[chunk*(i-1):chunk*(i)]
            i-=1
            if i == 1:
                break
        p.terminate()
        # print("end")
       ### print("frex:"+str(thefreq))
        self.__freq = thefreq
        return thefreq


    def recognize_freq2(self, NAME="MonoD"):
        #print(NAME)
        if (NAME[-4::] != ".wav"):
            NAME = NAME + ".wav"

        wf = wave.open(NAME, 'rb')
        swidth = wf.getsampwidth()
        RATE = wf.getframerate()
        thefreq = 0
        RECORDED_SECONDS = wf.getnframes() / RATE
        #print("Length of audio: ", round(RECORDED_SECONDS))
        # Window of all sample
        print(wf.getnframes())
        chunk = round(RATE * RECORDED_SECONDS)
        print(chunk)
        # use a Blackman window
        window = np.blackman(chunk)
        # open stream
        p = pyaudio.PyAudio()
        # read some data

        data = wf.readframes(chunk)
        # find the frequency of each chunk

        while len(data) == chunk * swidth:
            print(str(len(data)) + " == " + str(chunk * swidth))
            #print(data)
            # unpack the data and times by the hamming window
            indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth), data)) * window
            # Take the fft and square each value
            fftData = abs(np.fft.rfft(indata)) ** 2
            # find the maximum
            which = fftData[1:].argmax() + 1
            # use quadratic interpolation around the max
            if which != len(fftData) - 1:
                y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
                x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                # find the frequency and output it
                thefreq = (which + x1) * RATE / chunk
                thefreq = thefreq
            else:
                thefreq = which * RATE / chunk
            # read some more data
            data = wf.readframes(chunk)
        p.terminate()
        # print("end")
        self.__freq = thefreq
        return thefreq
