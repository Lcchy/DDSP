import torch
import os

from scipy.io.wavfile import read
from torch.utils.data import Dataset as ParentDataset

import numpy as np
import pandas as pd

from Parameters import *

#### Debug settings ####
PRINT_LEVEL = "INFO"  # Possible modes : DEBUG, INFO, RUN


class Dataset(ParentDataset):
    """ F0 and Loudness dataset."""

    def __init__(self):
        if not os.path.isdir(FRAGMENT_CACHE_PATH):
            compute_cache()

        self.nb_frags = len(os.listdir(FRAGMENT_CACHE_PATH))

    def __len__(self):
        return self.nb_frags

    def __getitem__(self, idx):
        if PRINT_LEVEL == "DEBUG":
            print("Getting item", idx)

        frag_path = os.path.join(FRAGMENT_CACHE_PATH, FRAGMENT_CACHE_PATTERN.format(idx))
        frag = torch.load(frag_path)
        return frag

def compute_cache():
    os.mkdir(FRAGMENT_CACHE_PATH)

    f0_filenames = sorted(os.listdir(F0_PATH))
    audio_filenames = sorted(os.listdir(AUDIO_PATH))

    item_i = 0
    for audio_filename, f0_filename in zip(audio_filenames, f0_filenames):
        if PRINT_LEVEL == "DEBUG":
            print("F0 file name :", f0_filename)
            print("Audio file name :", audio_filename)

        f0_full = read_f0(f0_filename)
        lo_full = read_lo(audio_filename)

        waveform_full = read_waveform(audio_filename)

        for frag_i in range(FRAGMENTS_PER_FILE):
            inputs, stfts = compute_fragment_cache(f0_full, lo_full, waveform_full, frag_i)
            frag_path = os.path.join(FRAGMENT_CACHE_PATH, FRAGMENT_CACHE_PATTERN.format(item_i))
            torch.save((inputs, stfts), frag_path)
            item_i += 1

def compute_fragment_cache(f0_full, lo_full, waveform_full, frag_i):
    f0_lo_stride = FRAME_SAMPLE_RATE * FRAGMENT_DURATION
    waveform_stride = FRAGMENT_DURATION * AUDIO_SAMPLE_RATE

    f0_lo_start_i = frag_i * f0_lo_stride
    f0_lo_end_i = (frag_i + 1) * f0_lo_stride

    f0 = f0_full[f0_lo_start_i:f0_lo_end_i]
    f0 = f0.reshape((f0.shape[0], 1))
    f0 = torch.tensor(f0)

    lo = lo_full[f0_lo_start_i:f0_lo_end_i]
    lo = lo.reshape((lo.shape[0], 1))
    lo = torch.tensor(lo)
    inputs = { "f0": f0, "lo": lo }

    waveform_start_i = frag_i * waveform_stride
    waveform_end_i = (frag_i + 1) * waveform_stride
    # throw away last frame
    waveform_end_i -= FRAME_LENGTH
    waveform = waveform_full[waveform_start_i:waveform_end_i]
    waveform = torch.tensor(waveform)#.unsqueeze(0)

    # # compute all stfts
    # stft = compute_stft(waveform, FFT_SIZES)
    # stft = {k:v.squeeze() for k,v in stft.items()}

    return inputs, waveform

def read_f0(file_name):
    file_path = os.path.join(F0_PATH, file_name)
    raw_data = pd.read_csv(file_path, header=0)
    raw_array = raw_data.to_numpy()
    f0 = raw_array[:-1, 1]
    f0 = f0.astype(np.float32)

    return f0


import scipy
import librosa as rosa

def read_lo(file_name):
    file_path = os.path.join(AUDIO_PATH, file_name)
    [fs, waveform] = scipy.io.wavfile.read(file_path)

    assert fs == AUDIO_SAMPLE_RATE

    # int to float
    dtype = waveform.dtype
    if np.issubdtype(dtype, np.integer):
        waveform = waveform.astype(np.float32) / np.iinfo(dtype).max

    lo = rosa.feature.rms(waveform, hop_length=FRAME_LENGTH, frame_length=FRAME_LENGTH)
    lo = lo.flatten()
    lo = lo.astype(np.float32)

    lo = np.log(lo + np.finfo(np.float32).eps)

    return lo

def read_waveform(file_name):
    file_path = os.path.join(AUDIO_PATH, file_name)
    [fs, waveform] = scipy.io.wavfile.read(file_path)

    assert fs == AUDIO_SAMPLE_RATE

    # int to float
    dtype = waveform.dtype
    if np.issubdtype(dtype, np.integer):
        waveform = waveform.astype(np.float32) / np.iinfo(dtype).max

    return waveform


if __name__ == "__main__":
    compute_cache()
