#### PARAMETERS FILE ####

import os
import torch

## FOLDER PARAMETERS ##
INSTRUMENT = "MyViolin"
AUDIO_PATH = os.path.join("Inputs", INSTRUMENT, "Audio")
F0_PATH = os.path.join("Inputs", INSTRUMENT, "F0")
FRAGMENT_CACHE_PATH = os.path.join("Cache", INSTRUMENT)
FRAGMENT_CACHE_PATTERN = "{:d}.pth"


## MODELS ##
PATH_SAVED_MODELS = os.path.join("Models")
MODEL_NAME = "Model_" + INSTRUMENT
MODEL_CHECKPOINT = MODEL_NAME + "_checkpt"
PATH_TO_CHECKPOINT = os.path.join(PATH_SAVED_MODELS, MODEL_CHECKPOINT + ".pth")
PATH_TO_MODEL = os.path.join(PATH_SAVED_MODELS, MODEL_NAME + ".pth")


## TRAIN PARAMETERS ##
SHUFFLE_DATALOADER = True
BATCH_SIZE = 6
FFT_SIZES = [2048, 1024, 512, 256, 128, 64]
NUMBER_EPOCHS = 1000
LEARNING_RATE = 0.001

GPU_ON = True
CUDA_ON = torch.cuda.is_available()
DEVICE = torch.device("cuda:0" if CUDA_ON and GPU_ON else "cpu")


## DATA PARAMETERS ##
AUDIO_SAMPLE_RATE = 16000
FRAME_SAMPLE_RATE = 100  # Hertz
FRAME_LENGTH = AUDIO_SAMPLE_RATE // FRAME_SAMPLE_RATE
AUDIOFILE_DURATION = 60  # Seconds
FRAGMENT_DURATION = 2  # Seconds
FRAGMENTS_PER_FILE = int(AUDIOFILE_DURATION / FRAGMENT_DURATION)
SAMPLES_PER_FRAGMENT = FRAGMENT_DURATION * FRAME_SAMPLE_RATE


## NET PARAMETERS ##
LINEAR_OUT_DIM = 512
HIDDEN_DIM = 512
NUMBER_HARMONICS = 64
OUTPUT_DIM = 1 + NUMBER_HARMONICS
USE_SIGMOID = False


## SYNTHESIS PARAMETERS ##
SYNTHESIS_DURATION = 2  # Seconds
SYNTHESIS_SAMPLING_RATE = 16000  # Hertz


## STFT PARAMETERS ##
STFT_SIZE = 512


## NUMBER PARAMETERS ##
SIGMOID_EXP = 1
