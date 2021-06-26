import pandas as pd
import numpy as np
import soundfile as sf
from scipy.io import wavfile

class CombFilter:

    def __init__(self,audio_file_path):
        self.original_audio,self.original_fs = sf.read(audio_file_path)
        self.filtered_audio = None
        self.filter_delay = None

    def feedForwardComb(self,filter_delay,alpha):

        self.filter_delay = filter_delay
        original_length = len(self.original_audio)
        final_length = original_length + self.filter_delay

        filtered_audio_list = []

        audio_iter = 0
        while(audio_iter < final_length):
            if(audio_iter < filter_delay):
                filtered_audio_list.append(self.original_audio[audio_iter])
            elif(audio_iter >= original_length):
                filtered_audio_list.append(alpha*self.original_audio[audio_iter - self.filter_delay])
            else:
                filtered_audio_list.append(self.original_audio[audio_iter] + alpha*self.original_audio[audio_iter - self.filter_delay])
            audio_iter += 1

        self.filtered_audio = np.array(filtered_audio_list)

    def feedbackComb(self,filter_delay,alpha):

        self.filter_delay = filter_delay
        original_length = len(self.original_audio)
        final_length = original_length + self.filter_delay

        filtered_audio_list = []

        audio_iter = 0
        while(audio_iter < final_length):
            if(audio_iter < filter_delay):
                filtered_audio_list.append(self.original_audio[audio_iter])
            elif(audio_iter >= original_length):
                filtered_audio_list.append(alpha*filtered_audio_list[audio_iter - self.filter_delay])
            else:
                filtered_audio_list.append(self.original_audio[audio_iter] + alpha*filtered_audio_list[audio_iter - self.filter_delay])
            audio_iter += 1

        self.filtered_audio = np.array(filtered_audio_list)

    def renderFilteredAudio(self,output_file_name):
        wavfile.write(output_file_name,self.original_fs,self.filtered_audio)

if __name__ == '__main__':

    audio_file_path = 'audio/run2.wav'
    output_file_path = 'audio/run2_comb.wav'
    delay = 50
    alpha = .5

    CF = CombFilter(audio_file_path)
    CF.feedbackComb(delay,alpha)
    CF.renderFilteredAudio(output_file_path)
