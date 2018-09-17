import math

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

    def __init__(self, name):
        self.__name = name
        self.__array_notes = None
        self.__audio = None
        self.__framerate = 44100
        self.__frames = None
        self.__time = None
        self.__npframe = None
        self.__freq = 0
        self.__metrum = (4, 4)
        self.__name_note = None
        self.__dict_freq = {'C': 32.7,
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

    def __del__(self):
        pass

    def get_name_note(self, freq=None):

        if freq == None:
            freq = self.__freq
        if freq != None:
            self.__name_note = librosa.hz_to_note(freq)
            return (''.join([i for i in self.__name_note if not i.isdigit()]))

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

    def get_framłes(self):
        return self.__frames

    def record_sample(self, time_of_recording=15):
        rate = 44100
        chunk = 1024
        channels = 1
        self.__framerate = rate
        format_audio = pyaudio.paInt16
        # instantiate the pyaudio
        audio = pyaudio.PyAudio()
        stream = audio.open(format=format_audio, channels=channels,
                            rate=rate, input=True, frames_per_buffer=chunk)
        # Start recording
        frames = []
        while True:
            data = stream.read(chunk)
            data_chunk = array('h', data)
            vol = max(data_chunk)

            if vol >= 250:
                print("start record")
                frames.append(data)
                for i in range(0, int(rate / chunk * time_of_recording)):
                    data = stream.read(chunk)
                    frames.append(data)
                break
        # end of recording
        stream.stop_stream()
        stream.close()
        self.__sampwidth = audio.get_sample_size(format_audio)
        self.__frames = b''.join(frames)

        self.__nframes = len(frames) / self.__sampwidth
        audio.terminate()
        return frames

    def get_the_freq(self):
        return self.__freq

    def remove_to_close(self, times, tempo, spaceModificer=20):
        arrayIndex = []
        for i in range(0, len(times) - 1):
            # tempo/20 precysion of slice ->20 bigger make more space
            if times[i + 1] - times[i] < (tempo / spaceModificer):
                arrayIndex.append(i + 1)
        return np.delete(times, arrayIndex)

    def bytes2int(self, str):
        return int(str.encode('hex'), 16)

    def get_peaks(self, frames=None):
        hop_length = 512
        if frames is not None:
            self.__frames = frames
        array = librosa.util.buf_to_float(self.__frames)
        self.__npframe = array
        audio_normalizte = librosa.util.normalize(array * 5)
        percusive = librosa.effects.percussive(audio_normalizte)
        onset_env = librosa.onset.onset_strength(percusive, self.__framerate, hop_length=hop_length,
                                                 aggregate=np.median)
        onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=self.__framerate)
        tempo, time_beats = librosa.beat.beat_track(percusive, self.__framerate, start_bpm=60)
        onset_frames = self.remove_to_close(onset_frames, tempo, int(math.log(tempo, 2)))
        self.__starts_stops = onset_frames * hop_length * 2
        return onset_frames * hop_length * 2

    def return_valuse_librosa_picks(self):
        hop_length = 512
        array = self.__starts_stops / (hop_length * 2)
        return array - array[0]

    def splits_audio_and_return_notes(self):
        array = np.frombuffer(self.__frames, dtype=np.uint8)
        self.__total_len_librosa = int(len(array) / 1024)
        notes_with_time = []
        times = self.return_valuse_librosa_picks()
        for i in range(0, (len(self.__starts_stops) - 1)):
            note_test = array[self.__starts_stops[i]:self.__starts_stops[i + 1]]
            note_name = self.get_name_note(self.recoginize_freq(b''.join(note_test), int(len(note_test) / 2)))
            notes_with_time.append([note_name, times[i]])
        self.__notes_with_time = notes_with_time
        return self.__notes_with_time

    def quantization_notes(self):
        array_of_len_notes = []
        len_dict = {'full': 4, 'half': 2, 'quarter': 1, 'eighth': 0.5, 'sixteenth': 0.25}

        for key, value in len_dict.items():
            array_of_len_notes.append([key, int((self.__tempo * value) / self.__metrum[0])])

        self.__notes_with_time.append(["last", self.__total_len_librosa])

        output = []

        for i in range(len(self.__notes_with_time) - 1):
            name = ''.join([a for a in self.__notes_with_time[i][0] if not a.isdigit()])
            timeline = self.__notes_with_time[i][1]
            duration = self.__notes_with_time[i + 1][1] - self.__notes_with_time[i][1]
            for q in range(len(array_of_len_notes) - 1):
                if array_of_len_notes[q][1] >= duration and array_of_len_notes[q + 1][1] < duration:
                    if ((array_of_len_notes[q][1] - array_of_len_notes[q + 1][1]) / 2) + array_of_len_notes[q + 1][
                        1] >= duration:
                        duration = array_of_len_notes[q + 1][0]
                        break
                    else:
                        duration = array_of_len_notes[q][0]
                        break
                elif array_of_len_notes[q][1] <= duration:
                    duration = array_of_len_notes[q][0]
                    break
            output.append([name, duration, timeline])
            duration = 0
        self.__notes_with_time.pop()
        return output

    def get_peaks_in_s(self, frames=None):
        hop_length = 512
        return librosa.frames_to_time(self.get_peaks(frames) / (hop_length * 2), self.__framerate)

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
        if self.__tempo is None:
            return -1
        else:
            return self.__tempo

    def recoginize_freq(self, frames=None, chunk=None):
        thefreq = 0
        if frames is not None:
            self.__frames = frames

        seconds = self.__nframes / self.__framerate
        if chunk == None:
            chunk = round(self.__framerate * seconds)
        # use a Blackman window
        window = np.blackman(chunk)
        # open stream
        p = pyaudio.PyAudio()
        data = self.__frames[0:chunk * self.__sampwidth]
        i = self.__sampwidth
        while len(data) == chunk * self.__sampwidth:
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
            data = self.__frames[chunk * (i - 1):chunk * (i)]
            i -= 1
            if i == 1:
                break
        p.terminate()
        print("freq: " + str(thefreq))
        self.__freq = thefreq
        return thefreq

    def recognize_freq_with_load(self, NAME="MonoD"):
        if (NAME[-4::] != ".wav"):
            NAME = NAME + ".wav"

        wf = wave.open(NAME, 'rb')
        swidth = wf.getsampwidth()
        RATE = wf.getframerate()
        thefreq = 0
        RECORDED_SECONDS = wf.getnframes() / RATE
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
        self.__freq = thefreq
        return thefreq
