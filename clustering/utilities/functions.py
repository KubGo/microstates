import numpy as np
import pickle
import re
import os
import shutil
import matplotlib as mpl
import matplotlib.pyplot as plt

from math import log2
from scipy.interpolate import griddata
from datetime import datetime

FILE_NAME =  os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "cap2.csv")

MICROSTATE_A = np.array([
    -30,   -30,
    0,   -30, -30,
    30, 0, -30 ,-30, -30,
    30,   30, 30,   30,  0,  -30, -30,  -30,  -30,
    30, 30, 30,  0,  -30,
    30,  30, 0,
    30, 0, 
    30])
MICROSTATE_B = np.array([
    -30,   -30,
    -30,   -30, 0,
    -30, -30, -30 , 0, 30,
    -30, -30, -30,   -30,  0,  30, 30,  30,  30,
    -30, 0, 30,  30,  30,
    0,  30, 30,
    0, 30, 
    30])
MICROSTATE_C = np.array([
    -30,   -30,
    -30,   -30, -30,
    -30, -30, -30 , -30, -30,
    -30, -30, -30, -30, -30, -30, -30, -30,  -30,
    30, 30, 30,  30,  30,
    30, 30, 30,
    30, 30, 
    30])
MICROSTATE_D = np.array([
    -30,   -30,
    -30,   -30, -30,
    30, -30, -30 , -30, -30,
    30, 30, -30, -30, -30, -30, -30, -30,  30,
    30, -30, -30,  -30,  30,
    30, -30, 30,
    30, 30, 
    30])
REFERENCE_MICROSTATES = np.array([
    MICROSTATE_A,
    MICROSTATE_B,
    MICROSTATE_C,
    MICROSTATE_D
])

def eeg_to_map(data, n_grid=64):
    """
    Interpolate and normalize EEG topography
    Args:
        data:numpy array
        EEG data
        n_grid: int
        Number of point to interpolate to
        n_grid x n_grid, default=64
    Returns:
        topography_normalized:
            Normalized topography n_grid x n_grid
    """

    n_grid = 64
    topography = get_topography(data, n_grid)
    min = np.nanmin(topography)
    max = np.nanmax(topography)
    topography_normalized = (topography - min) / (max - min)
    return topography_normalized

def read_xyz(filename = FILE_NAME):
    """Reads locations of EEG electrodes in xyz format
    Args:
        filename: str
            Path to the '.xyz' file
    Returns:
        channel_names: list
            Channel names
        locations: numpy array n_channels x 3
            Locations of electrodes
    """

    channel_names = []
    locations = []

    with open(filename, 'r') as file:
        # Read header line
        line = file.readline()
        # Read locations
        while line:
            line = file.readline().strip().split("\t")
            if line != ['']:
                channel_names.append(line[0])
                locations.append([float(line[1]), float(line[2]), float(line[3])])
            else:
                line = None
    return channel_names, np.array(locations)


def get_topography(data: np.array,path_to_file, n_grid=64):
    """
    Interpolate EEG topograpth onto a regularly spaced grid
    Args:
        data: numpy array
            EEG data
        n_grid: integer
            Square grid size to interpolate
    Returns:
        Cubic interpolation of EEG topography n_grid x n_grid
    """
    channel_names, locations = read_xyz()
    n_channels = len(channel_names)

    locations /= np.linalg.norm(locations, 2, axis=1, keepdims=True)
    c = channel_names.index("Cz")
    w = np.linalg.norm(locations - locations[c], 2, 1)
    arclen = np.arcsin(w / 2. * np.sqrt(4. - w * w))
    phi_re = locations[:, 0] - locations[c][0]
    phi_im = locations[:, 1] - locations[c][1]
    tmp = phi_re + 1j * phi_im
    phi = np.angle(tmp)
    X = arclen * np.real(np.exp(1j * phi))
    Y = arclen * np.imag(np.exp(1j * phi))
    r = max([max(X), max(Y)])
    Xi = np.linspace(-r, r, n_grid)
    Yi = np.linspace(-r, r, n_grid)
    data_ip = griddata((X, Y), data, (Xi[None, :], Yi[:, None]), method='cubic')
    return data_ip



def entropy(probabilities: list):
    """
    Calculate
    Args:
        probabilities: list
        Probabilities of states

    Returns:
        h: entropy for given probabilities

    Notes:
        Herein logarithm with a base of 2 is used.
        However, in Frederic's the natural logarithm
        is used. I believe it is easier to understand it
        when it is presented in bits.
    """
    h = 0
    for p in probabilities:
        if (float(p) == 0 ):
            h += 0
            continue
        h += -p * log2(p)
    return h


def get_shuffled_copy(data: np.array):
    """
    Get shuffled copy of data
    Args:
        data: numpy array
            EEG microstates data
    Returns:
        shuffled_data: Shuffled copy of data
    """
    shuffled_data = data.copy()
    np.random.shuffle(shuffled_data)
    return shuffled_data


def load_model(path):
    """
    Load already developed model
    Args:
        path: String,
        Relative or absolute path to a model pickle file
    Returns:
        A child of AbstractModel class
    """
    if path:
        with open(path, "rb") as file:
            model = pickle.load(file)
            return model

def remove_pickles(folder, destination_folder):
    if not os.path.exists(folder):
        raise FileNotFoundError("There isn't such a path.")
    if not os.path.isdir(folder):
        raise NotADirectoryError("Given path is not for a directory")

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    files = os.listdir(folder)
    files_to_move = [f for f in files if not f.endswith(".pickle")]

    for file_name in files_to_move:
        print(f"file to move: {file_name}")
        source_file = os.path.join(folder, file_name)
        if os.path.isfile(source_file):
            destination_file = os.path.join(destination_folder, file_name)
            shutil.copy(source_file, destination_file)
            print(f"moved to {destination_file}")
        else:
            new_destination = os.path.join(destination_folder, file_name)
            remove_pickles(source_file, new_destination)
            
            
def match_data_folder(folder_name):
    """
    Check If folder matches to PXX where XX are digits
    Args:
        folder_name: name of the folder
    Returns:
        True, if matched else False
    """
    pattern = r'^P\d{2}'
    return re.match(pattern, folder_name)


def extract_date(filename):
    """
    Extracts date in datetime format from filename in
    convention like dd_mm_yy_filename.extension
    Args:
        filename: String, name of the file
    Returns:
        Datetime: Date from start of filename
    """
    parts = filename.split('_')
    date_str = '_'.join(parts[:3])
    return datetime.strptime(date_str, '%d_%m_%y')

def plot_microstate(microstate):
    cm = mpl.colormaps['seismic']
    plt.imshow(eeg_to_map(microstate), cmap=cm, origin='lower')
    plt.axis('off')
    plt.show()
    plt.clf()

def reorder_microstates(microstates: np.array, reference_microstates = None):
    reordered_microstates = np.ones(microstates.shape)
    # Get correlations between microstates and it's references
    microstates_normalized = microstates - np.mean(microstates, axis=1, keepdims=True) 
    microstates_normalized /= np.std(microstates, axis=1, keepdims=True)
    if not reference_microstates:
        reference_microstates = REFERENCE_MICROSTATES
    reference_microstates_normalized = reference_microstates - np.mean(reference_microstates, axis=1, keepdims=True)
    reference_microstates_normalized /= np.std(reference_microstates, axis=1, keepdims=True) 
    corr = np.dot(
        microstates_normalized, 
        reference_microstates_normalized.T) / len(microstates[0])
    corr = corr ** 2
    print(corr)
    print()
    # Pick the highest correlation and leave other for next iteration
    for _ in microstates:
        max_corr = np.max(corr, axis=1) # Max correlation in row
        max_positions = np.argmax(corr, axis=1) # row max position
        # Get position of microstate with maximal correlation value
        current_position = np.argmax(max_corr)
        new_position = max_positions[current_position]
        reordered_microstates[new_position] = microstates[current_position]
        # Remove this microstate correlation from next iterations
        corr[:, new_position] = -1
        corr[current_position, :] = -1
    return reordered_microstates
