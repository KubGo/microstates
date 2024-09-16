import numpy as np
import re
import os

from scipy.interpolate import griddata

FILE_NAME =  os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "cap2.csv")

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


