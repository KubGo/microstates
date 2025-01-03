import os
import datetime
import pickle
import time
import sys
from decimal import Decimal

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import ArtistAnimation
from matplotlib.patches import Patch
import seaborn as sn
from jinja2 import Environment, FileSystemLoader

from . utilities import eeg_to_map, match_data_folder
from reporting import save_report, generate_comparison_report



def generate_average_results(path_to_results_folder, destination_path, activity, method, subfolder=""):
    """
    Generates averaged results for activity and method for all results
    Prototype method - for later discuss if this approach is correct,
    but there might be a need for some kind of need to reorder microstates
    Args:
        path_to_results_folder: String, path,
            Path to a folder with results for sportsmen
        destination_path: String, path,
            Destination path to save results
        activity: String,
            Activity to use for averaging
        method: String,
            Algorithm name to use
        subfolder: String,
            Used to get for example all listening data to use for averaging
    Returns:
        Saves averaged microstates and transition matrix in destination path
    """

    if not os.path.exists(path_to_results_folder):
        raise FileNotFoundError("There isn't such a path.")
    if not os.path.isdir(path_to_results_folder):
        raise NotADirectoryError("Given path is not for a directory")

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    files = os.listdir(path_to_results_folder)
    files = [os.path.join(path_to_results_folder, f) for f in files if match_data_folder(f)]
    for file in files:
        print(file)
    num_of_microstates_concated = 0
    microstates = np.zeros((4, 30))
    transition_matrix = np.zeros((4, 4))
    for file in files:
        path_to_results = os.path.join(file, activity, method, subfolder, "results")
        pickles = [os.path.join(path_to_results, f) for f in os.listdir(path_to_results) if f.endswith(".pickle")]
        if pickles:
            num_of_microstates_concated += 1
            print(f"Concatenated microstates {num_of_microstates_concated}")
            # latest_pickle = sorted(pickles, key=extract_date, reverse=True)[0]

            path_to_pickle = pickles[0]

            results = results_factory(path_to_pickle)
            for i in range(4):
                microstates += results.cluster_centers
            transition_matrix += results.transition_matrix

    microstates /= num_of_microstates_concated
    transition_matrix /= num_of_microstates_concated
    print(transition_matrix)
    print("#" * 50)
    print(microstates[0])
    result = Results(method)
    result.transition_matrix = transition_matrix
    result.cluster_centers = microstates
    results_path = os.path.join(destination_path, activity)
    result.save_results(results_path)
    result.save_microstates_images(results_path)
    result.save_transition_matrix(results_path)



class Results:
    cluster_centers = None
    clusters_chain = []
    empirical_p = []
    total_time = None
    time_occurrences = None
    transition_matrix = None
    h_max = h = h_mc = None
    p_markov_test_0 = p_markov_test_1 = p_markov_test_2 = None
    p_symmetry_test = p_conditional_homogenity = None
    maxima = None
    n_channels = None
    n_data_points = None
    alpha_wave = []
    gev = None
    fs = None
    data_for_gif = []
    alpha = None
    activity = None
    stats = None


    def __init__(self,  method: str):
        self.method = method
        self.id= ''
        self.activity = ''
        self.pickle_path = ''
        self.group = ''

    def set_id_and_activity(self, id: str, activity:str):
        self.id = id
        self.activity = activity
        
    def get_name(self) -> str:
        if self.group:
            return f"{self.id}-{self.group}-{self.activity}"
        return f"{self.id}-{self.activity}"

    def save_results(self, path):
        """
        Save results to destination path as dd_mm_yy_model.pickle
        Args:
            path: String, path,
                Path to a folder where pickled results should be saved
        """
        if not os.path.exists(path):
            os.makedirs(path)
        destination_path = os.path.join(path, datetime.datetime.now().strftime("%d_%m_%y") + "_model.pickle")
        with open(destination_path, "wb") as file:
            pickle.dump(self, file, protocol=pickle.HIGHEST_PROTOCOL)
        return destination_path

    def save_alpha_wave(self, path):
        """
        Save alpha wave image in folder specified by path
        Args:
            path: String, path,
                Path to a folder
        """
        data = self.alpha_wave
        if data is None:
            print("There is no alpha wave to plot")
            return
        t = np.arange(len(data)) / self.fs
        fig = plt.figure(1, figsize=(20, 5))
        plt.plot(t, data, "-k", linewidth=1)
        plt.xlabel("time [s]", fontsize=24)
        plt.ylabel("potential energy [$\mu$V]", fontsize=24)
        plt.tight_layout()
        destination_path = os.path.join(path, "pca_alpha_wave.jpg")
        plt.savefig(destination_path)
        plt.clf()
        return destination_path

    def save_each_microstate_image(self, path, xyz_file_path=""):
        """
        Save microstate single images to given path folder
        Args:
            path: String,
                Path to a folder
        """
        if not os.path.exists(path):
            print("Path doesn't exist")
            return
        microstates = self.cluster_centers
        if microstates is None:
            print("There are no microstates to plot")
            return
        cm = mpl.colormaps['seismic']
        for i, microstate in enumerate(microstates):
            path_for_microstate = os.path.join(path, f"microstate_{i}.png")
            plt.imshow(eeg_to_map(microstate), cmap=cm, origin='lower')
            plt.axis('off')
            plt.savefig(path_for_microstate, bbox_inches='tight')
            plt.clf()

    def save_microstates_images(self, path):
        """
        Save microstate images in folder specified by path
        Args:
            path: String, path,
                Path to a folder
        """
        if not os.path.exists(path):
            print("Path doesn't exist")
            return
        microstates = self.cluster_centers
        if microstates is None:
            print("There are no microstates to plot")
            return
        n_clusters = len(microstates)
        cm = mpl.colormaps['seismic']
        fig, ax = plt.subplots(1, n_clusters, figsize=(20, 5))
        microstates_labels = ['A', 'B', 'C', 'D']
        for imap in range(n_clusters):
            ax[imap].imshow(eeg_to_map(microstates[imap]), cmap=cm, origin='lower')
            ax[imap].set_xticks([])
            ax[imap].set_xticklabels([])
            ax[imap].set_yticks([])
            ax[imap].set_yticklabels([])
            ax[imap].set_title(f"{microstates_labels[imap]}", loc='center', fontsize=16)
        title = f"Microstates map ({self.method.upper()})"
        fig.suptitle(title, fontsize=16, fontweight='bold')
        # axbox = plt.axes([0.1, 0.05, 0.1, 0.1])
        # text_box = TextBox(axbox, "Ordering: ", initial="[0, 1, 2, 3]")
        destination_path = os.path.join(path, "microstates.jpg")
        plt.savefig(destination_path)
        plt.clf()
        return destination_path

    def save_gif(self, data, path):
        """
        Save gif to folder specified by path
        Args:
            data: numpy array,
                EEG data
            path: String, path,
                Path to a folder to save gif
        """
        microstates = self.cluster_centers
        microstate_chain = self.clusters_chain
        n = len(data)
        # if not microstates[0]:
        #     print("There are no microstates clusters available")
        #     return
        # if not microstate_chain[0]:
        #     print("There is no microstates chain available")
        #     return
        frames = []
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        ax[1].set_title("Microstate")
        ax[0].set_title("original")
        cm = mpl.colormaps['seismic']
        font = {
            'family': 'serif',
            "color": 'black',
            'weight': 'bold',
            'size': 16
        }
        print("Preparing gif")
        for i in range(n):
            original = ax[0].imshow(eeg_to_map(data[i]), cmap=cm, origin='lower')
            cluster = microstate_chain[i]
            fit = ax[1].imshow(eeg_to_map(microstates[cluster]), cmap=cm, origin='lower')
            ax[0].axis('off')
            ax[1].axis('off')
            frames.append([original, fit])
            progress(i, n)
        print("")

        animation = ArtistAnimation(fig, frames, interval=100)
        destination_path = os.path.join(path, "microstates.gif")
        print("Saving gif")
        time.sleep(0.5)
        animation.save(destination_path, writer='pillow',
                       progress_callback=lambda e, r: progress(e, n))
        plt.clf()
        print()
        return destination_path

    def save_transition_matrix(self, path):
        """
        Save transition matrix as csv in folder specified by path
        Args:
            path: String, path,
                Path to a folder to save csv
        """
        fig = plt.figure(1, figsize=(10, 10))
        transition_matrix = self.transition_matrix
        if transition_matrix is None:
            print("There is no transition matrix available")
            return
        destination_path = os.path.join(path, "transition_matrix.jpg")
        sn.set(font_scale=3)
        microstates_labels = ['A', 'B', 'C', 'D']
        hm = sn.heatmap(transition_matrix,
                        annot=True,
                        cmap="coolwarm",
                        xticklabels=microstates_labels,
                        yticklabels=microstates_labels)

        fig.savefig(destination_path)
        fig.clf()
        sn.reset_orig()
        return destination_path

    def set_markov_test(self, order, p):
        if order <= 0:
            self.p_markov_test_0 = p
        elif order == 1:
            self.p_markov_test_1 = p
        else:
            self.p_markov_test_2 = p

    def generate_results_report(self, destination_path, method, activity, subfolder=None, xyz_file_path=""):
        """
        Generate html report of EEG microstates analysis
        Args:
            destination_path: String,
                Path to save files
            method: String,
                Method to perform analysis
                ['kmeans', 'kmedoids', 'aahc', 'pca', 'ica', 'dbscan', 'brich']
            activity: String,
                Activity performed
            subfolder: String, default=None
                Name of subfolder to save results
        Returns:
            Images, gif and html report in destination_path folder
        """
        # Make folders
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        if subfolder is not None:
            destination_path = os.path.join(destination_path, subfolder)
        images_path = os.path.join(destination_path, "images")
        if not os.path.exists(images_path):
            os.makedirs(images_path)
        results_path = os.path.join(destination_path, "results")
        if not os.path.exists(results_path):
            os.makedirs(results_path)
        # Save results as a pickle
        self.activity = activity
        print("Result.pickle saved")
        # Save alpha wave potential
        path_for_alpha_wave = self.save_alpha_wave(images_path)
        print("Alpha wave image saved")
        # Save peaks on signal image
        self.draw_signal_and_peaks(images_path)
        # Save microstates images
        self.save_each_microstate_image(images_path, xyz_file_path=xyz_file_path)
        path_to_microstates_image = self.save_microstates_images(images_path)
        if path_to_microstates_image:
            print("Microstates image saved")
        # Save gif
        data_for_gif = self.data_for_gif[:200]
        path_to_gif = self.save_gif(data_for_gif, images_path)
        print("Gif saved")
        # Save transition matrix
        path_to_transition_matrix = self.save_transition_matrix(images_path)
        print("Transition matrix image saved")
        time_occurences = [p * self.n_data_points / self.fs for p in self.empirical_p]
        self.time_occurrences = time_occurences
        self.total_time = round(self.n_data_points / self.fs, 2)
        microstate_times = get_microstates_time_chain(self.clusters_chain, self.fs)
        stats = get_microstate_time_stats(microstate_times)
        self.stats = stats
        pickle_path = self.save_results(results_path)
        params_index = {
            "path_for_alpha_wave": os.path.abspath(path_for_alpha_wave),
            "path_to_microstates_image":
                os.path.abspath(path_to_microstates_image) if path_to_microstates_image else None,
            "path_to_gif": os.path.abspath(path_to_gif) if path_to_gif else None,
            "path_to_transition_matrix": os.path.abspath(path_to_transition_matrix),
            "method": method,
            "activity": activity,
            "n_samples": self.n_data_points,
            "n_channels": self.n_channels,
            "n_maps": len(self.cluster_centers) if self.cluster_centers is not None else 4,
            "p_empirical": self.empirical_p,
            "total_time": self.total_time,
            "time_occurrences": time_occurences,
            "max_entropy": self.h_max,
            "entropy": self.h,
            "mc_entropy": self.h_mc,
            "alpha": self.alpha,
            "markov_p0": "{:.2E}".format(Decimal(str(self.p_markov_test_0))),
            "markov_p1": "{:.2E}".format(Decimal(str(self.p_markov_test_1))),
            "markov_p2": "{:.2E}".format(Decimal(str(self.p_markov_test_2))),
            "symmetry_p": "{:.2E}".format(Decimal(str(self.p_symmetry_test))),
            "cond_homo_p": "{:.2E}".format(Decimal(str(self.p_conditional_homogenity))),
            "microstate_labels": ['A', 'B', 'C', 'D']
            # "stats": stats,
        }
        params_chain = {
            "method": method,
            "activity": activity,
            "microstate_times": microstate_times,
            "stats": stats,
            "subfolder": subfolder,
            "microstate_labels": ['A', 'B', 'C', 'D']
        }
        # Prototype saving report
        save_report(results_path, params_index, params_chain)
        print("Report saved")
        self.pickle_path = pickle_path

    def draw_signal_and_peaks(self, path):
        GFP = self.alpha_wave[:1500]
        microstates = self.clusters_chain
        # Change it to list of elements from list of lists with one element
        data = [x[0] for x in GFP]
        # Get size to display well the whole range of microstates
        size = (20, 5)
        fig = plt.figure(1, figsize=size)
        points = np.arange(len(GFP)) / self.fs
        last_microstate = microstates[0]
        start_point = 0
        colors = {
            0: "green",
            1: "blue",
            2: "red",
            3: "yellow"
        }
        for point, microstate in enumerate(microstates):
            if last_microstate != microstate:
                last_point = point
                plt.fill_between(x=points,
                                 y1=data,
                                 where=(points >= start_point / self.fs) & (points <= last_point / self.fs),
                                 color=colors[last_microstate],
                                 alpha=0.6)
                last_microstate = microstate
                start_point = last_point
        legend_patches = [Patch(color=color, label=label) for label, color in colors.items()]
        plt.legend(handles=legend_patches)
        plt.plot(points, data)
        destination_path = os.path.join(path, "peaks.jpg")
        plt.savefig(destination_path)
        plt.clf()

    def get_microstates_figures(self):
        cm = mpl.colormaps['seismic']
        figures = []
        for i, microstate in enumerate(self.cluster_centers):
            fig, ax = plt.subplots()
            ax.imshow(eeg_to_map(microstate), cmap=cm, origin='lower')
            plt.axis('off')
            figures.append(fig)
        return figures


def results_factory(filename=None, method=None):
    """
    Create new empty result from name and method or load from filename
    Args:
        filename: String,
            Path to saved results as .pickle
        method: String,
            Method of new model
    Returns:
        Results: Loads or creates new results
    """
    if filename:
        with open(filename, "rb") as file:
            results = pickle.load(file)
            if not isinstance(results, Results):
                raise TypeError(f"Unpickled object is not of type {Results}")
            return results
    if not method:
        raise SyntaxError("There is a need for keyword argument: method\n"
                          "or give a path for pickled results")
    return Results(method)


def load_results(filename) -> Results:
    """
    Load results file
    Args:
        filename: String,
        Path to a pickled results
    Returns:
        Results of given path
    """
    if filename:
        with open(filename, 'rb') as file:
            results = pickle.load(file)
            if not isinstance(results, Results):
                raise TypeError(f"Unpickled object is not of type {Results}")
            return results



def save_results_to_df(path_to_pickle, activity=' ', imagining=' '):
    """
    Creates a dictionary with lists of values obtained in results pickle
    Args:
        path_to_pickle: String, path,
            Path to the pickle file with results
        activity: String,
            Name of the activity of the results
        imagining: String,
            String that describes what kins of imagining test it was
    Returns:
        df: Pandas.DataFrame containing the results data
    """
    if not os.path.exists(path_to_pickle):
        raise FileNotFoundError("There is not such a pickle file")
    result = load_results(path_to_pickle)
    data = {
        "activity": activity,
        "imagining": imagining,
        "probability_A": result.empirical_p[0],
        "probability_B": result.empirical_p[1],
        "probability_C": result.empirical_p[2],
        "probability_D": result.empirical_p[3],
        "time_A": result.time_occurrences[0],
        "time_B": result.time_occurrences[1],
        "time_C": result.time_occurrences[2],
        "time_D": result.time_occurrences[3],
        "A_min": result.stats["0"]['min'],
        "A_max": result.stats["0"]['max'],
        "A_mean": result.stats["0"]['mean'],
        "A_std": result.stats["0"]['std'],
        "B_min": result.stats["1"]['min'],
        "B_max": result.stats["1"]['max'],
        "B_mean": result.stats["1"]['mean'],
        "B_std": result.stats["1"]['std'],
        "C_min": result.stats["2"]['min'],
        "C_max": result.stats["2"]['max'],
        "C_mean": result.stats["2"]['mean'],
        "C_std": result.stats["2"]['std'],
        "D_min": result.stats["3"]['min'],
        "D_max": result.stats["3"]['max'],
        "D_mean": result.stats["3"]['mean'],
        "D_std": result.stats["3"]['std'],
        "P_A_A": result.transition_matrix[0][0],
        "P_A_B": result.transition_matrix[0][1],
        "P_A_C": result.transition_matrix[0][2],
        "P_A_D": result.transition_matrix[0][3],
        "P_B_A": result.transition_matrix[1][0],
        "P_B_B": result.transition_matrix[1][1],
        "P_B_C": result.transition_matrix[1][2],
        "P_B_D": result.transition_matrix[1][3],
        "P_C_A": result.transition_matrix[2][0],
        "P_C_B": result.transition_matrix[2][1],
        "P_C_C": result.transition_matrix[2][2],
        "P_C_D": result.transition_matrix[2][3],
        "P_D_A": result.transition_matrix[3][0],
        "P_D_B": result.transition_matrix[3][1],
        "P_D_C": result.transition_matrix[3][2],
        "P_D_D": result.transition_matrix[3][3],
    }
    data = {key: [value] for key, value in data.items()}
    df = pd.DataFrame(data)
    return df


def save_all_sportsman_data_to_csv(path_to_files, method="kmeans"):
    if not os.path.exists(path_to_files):
        raise FileNotFoundError(f"There isn't such a file as {path_to_files}")

    df = pd.DataFrame()

    sportman_paths = {sportsman: os.path.join(path_to_files, sportsman) for sportsman in os.listdir(path_to_files) if match_data_folder(sportsman)}
    for sportsman, folder in sportman_paths.items():
        activities = {activity: os.path.join(folder, activity) for activity in os.listdir(folder)}
        for activity, activity_path in activities.items():
            # Get listening pickle
            listening_path = os.path.join(activity_path, method, "listening", "results")
            listening_pickle = [os.path.join(listening_path, file) for file in os.listdir(listening_path) if file.endswith(".pickle")][0]

            # Get imagining pickle
            imagining_path = os.path.join(activity_path, method, "imagining", "results")
            imagining_pickle = [os.path.join(imagining_path, file) for file in os.listdir(listening_path) if file.endswith(".pickle")][0]

            listening_df = save_results_to_df(listening_pickle, activity=activity, imagining="guided")
            imagining_df = save_results_to_df(imagining_pickle, activity=activity, imagining="self-guided")
            df = pd.concat([df, listening_df, imagining_df], ignore_index=True)

    df.to_csv(os.path.join(path_to_files, "results.csv"), index=False)


def progress(count, total, suffix=''):
    """
    Prints progress of given iterative task to console
    Args:
        count: int,
            Current iteration
        total: int,
            Total iterations
        suffix: String,
            String added at the end of progress bar
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben


def get_microstates_time_chain(microstates_chain, fs):
    """
    Get list  microstate and time of its occurrence
    Args:
        microstates_chain: list, numpy array,
            Microstates chain
        fs: int,
            Sampling frequency
    Returns:
        List: [[microstate, occurrence_time],...]
    """
    time_frame = round(1 / fs, 3)
    microstates_time_list = [[]]
    current_state = 0
    current_cluster = microstates_chain[0]
    microstates_time_list[current_state] = [current_cluster, time_frame]
    for i in microstates_chain[1:]:
        new_cluster = i
        if new_cluster == current_cluster:
            microstates_time_list[current_state][1] += time_frame
        else:
            microstates_time_list.append([new_cluster, time_frame])
            current_state += 1
        current_cluster = new_cluster
    return microstates_time_list


def get_microstate_time_stats(microstate_times):
    """
    Calculate min, max, mean and std for microstate_times
    Args:
        microstate_times: list of lists,
            list of microstates and times of their occurences
    Returns:
        stats: min, max, mean, std in form of dict
    """
    each_microstate_times = {
        "0": [],
        "1": [],
        "2": [],
        "3": []
    }
    
    for microstate_time in microstate_times:
        each_microstate_times[f"{microstate_time[0]}"].append(microstate_time[1])
    stats = {
        
    }
    for microstate, times in each_microstate_times.items():
        stats[microstate] = {
            'min': min(times),
            'max': max(times),
            'mean': np.array(times).mean(),
            'std': np.array(times).std(),
            "hist": np.array(np.unique(times, return_counts=True)).T
        }
    return stats
