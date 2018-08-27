import numpy as np
import librosa
import cv2 as cv
from scipy.misc import imsave
# from skimage.io import imsave
import resource


class Signature:
    __y = None
    __sr = None
    __fft_array = None

    def __init__(self, path_load=None):
        if path_load is not None:
            self.load_audio(path_load)
        pass

    def __del__(self):
        pass

    def load_audio(self, path_load):
        self.__y, self.__sr = librosa.load(path_load)
        pass

    def fft_signature(self, n_fft=2048, hoop=48):
        self.__fft_array = librosa.amplitude_to_db(librosa.core.stft(self.__y, n_fft, hoop), ref=np.max)
        return self.__fft_array
        pass

    def save_signature(self, name):
        imsave(name, self.__fft_array[:])
        pass

    def mix_signature(self, path_list_of_audio, path_save, is_array=False):

        pass
