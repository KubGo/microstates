import numpy.typing as npt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.typing as mplt
from matplotlib.patches import Patch
import os
from scipy.interpolate import griddata
import seaborn as sn

LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', "H", 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

FILE_NAME =  os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "cap2.csv")

def plot_gfp(
    data: npt.ArrayLike,
    frequency: int) -> plt.Figure:
    plt.close('all')
    t = np.arange(len(data)) / frequency
    fig = plt.figure()
    plt.plot(t, data, "-k", linewidth=1)
    plt.xlabel("time [s]", fontsize=24)
    plt.ylabel("potential energy [µV]", fontsize=24)
    plt.tight_layout()
    return fig

def plot_microstate(
    microstate_data: npt.ArrayLike) -> plt.Figure:
    cm = matplotlib.colormaps['seismic']
    plt.close('all')
    fig = plt.figure()
    plt.imshow(
        eeg_to_map(microstate_data),
        cmap=cm,
        origin='lower')
    plt.axis('off')
    return fig

def plot_transition_matrix(
    transition_matrix: npt.ArrayLike) -> plt.Figure:
    plt.close('all')
    fig = plt.figure(figsize=(10, 10))
    labels = LABELS[:len(transition_matrix[0])]
    sn.set(font_scale=3)
    heat_map = sn.heatmap(
        data=transition_matrix,
        annot=True,
        cmap='coolwarm',
        xticklabels=labels,
        yticklabels=labels
    )
    return heat_map.get_figure()

def plot_peaks_on_signal(
    data: npt.ArrayLike,
    microstates_chain: list[str],
    frequency: int) -> plt.Figure:
    plt.close('all')
    fig = plt.figure()
    colors = {
        0: "green",
        1: "blue",
        2: "red",
        3: "yellow",
        4: "orange",
        5: "brown",
        6: "purple",
        7: "black"
    }
    t  = np.arange(len(data)) / frequency
    last_microstate = microstates_chain[0]
    start_point = 0
    for point, microstate in enumerate(microstates_chain):
        if last_microstate != microstate:
            last_point = point
            plt.fill_between(
                x=t,
                y1=data,
                where=(t >= start_point / frequency) & (t <= last_point / frequency),
                color=colors[last_microstate],
                alpha=0.6)
            last_microstate = microstate
            start_point = last_point
    legend_patches = [Patch(color=color, label=label) for label, color in colors.items()]
    plt.legend(handles=legend_patches)
    plt.plot(t, data)
    return fig

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
