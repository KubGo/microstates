import os
import sys
import pickle
from decimal import Decimal
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import numpy as np
from clustering.utilities import match_data_folder


def save_report(destination_path, params_index, params_chain=None):
    """
    Saves html report to destination_path
    Args:
        destination_path: String,
            Path to a folder to save report
        params_index: dict,
            Dict of needed parameter to render main html page
        params_chain: dict,Default=None
            Dict of needed parameters to render chain html page
            if None, there isn't chain html page
    Returns:
        Report in destination_path folder
    """
    template_path = os.path.abspath(__file__)
    folder = os.path.join(os.path.dirname(template_path), "templates")
    environment = Environment(loader=FileSystemLoader(folder))
    template_index = environment.get_template("index.html")
    index_path = os.path.join(destination_path, "index.html")
    index_content = template_index.render(params_index)
    with open(index_path, mode='w', encoding="utf-8") as file:
        file.write(index_content)
    if params_chain is not None:
        template_chain = environment.get_template("microstates_chain.html")
        chain_path = os.path.join(destination_path, "microstates_chain.html")
        chain_content = template_chain.render(params_chain)
        with open(chain_path, mode='w', encoding="utf-8") as file:
            file.write(chain_content)


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
    result = load_pickle(path_to_pickle)
    data = {
        "name": result.name,
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


def generate_comparison_report(path_to_folder, analyse_breaks=False, separate_states=False):
    # if os.path.isdir(path_to_folder):
    #     print("Give a method folder path that contains following folders:\n"
    #           "\t-images\n"
    #           "\t-imagining\n"
    #           "\t-listening\n"
    #           "\t-results")
    #     return
    dirs = os.listdir(path_to_folder)
    if separate_states:
        if not os.path.exists(os.path.join(path_to_folder, "results")):
            os.makedirs(os.path.join(path_to_folder, "results"))
        if not all(folder in dirs for folder in ["listening", "imagining"]):
            print("Give a method folder path that contains following folders:\n"
                  "\t-imagining\n"
                  "\t-listening\n")
            raise FileNotFoundError("All needed files were not found.")

    else:
        if not all(folder in dirs for folder in ["images", "imagining", "listening", "results"]):
            print("Give a method folder path that contains following folders:\n"
                  "\t-images\n"
                  "\t-imagining\n"
                  "\t-listening\n"
                  "\t-results")
            raise FileNotFoundError("All needed files were not found.")
    # Destination path to save results
    destination_path = os.path.join(path_to_folder, "results")

    # Paths for pickled results
    path_for_pickle_listening = os.path.join(path_to_folder, "listening", "results")
    path_for_pickle_imagining = os.path.join(path_to_folder, "imagining", "results")
    results_paths = [path_for_pickle_listening, path_for_pickle_imagining]

    template_path = os.path.abspath(__file__)
    folder = os.path.join(os.path.dirname(template_path), "templates")
    environment = Environment(loader=FileSystemLoader(folder))
    template = environment.get_template("comparison.html")

    # Get listening and imagining results
    results = []
    for res_path in results_paths:
        files = os.listdir(res_path)
        for file in files:
            name, extension = os.path.splitext(file)
            if extension == ".pickle":
                file_path = os.path.join(res_path, file)
                result = load_pickle(filename=file_path)
                results.append(result)
                break
    path_for_breaks = None
    if analyse_breaks:
        parent_directory = path_to_folder
        print(f"Path to folder : {parent_directory}")
        path_for_start_breaks = os.path.join(parent_directory, "start_break", "results")
        path_for_end_breaks = os.path.join(parent_directory, "end_break", "results")
        paths = [path_for_start_breaks, path_for_end_breaks]
        for path in paths:
            files = os.listdir(path)
            for file in files:
                name, extension = os.path.splitext(file)
                if extension == ".pickle":
                    file_path = os.path.join(path, file)
                    result = load_pickle(filename=file_path)
                    results.append(result)
    time_occurences = []

    # Results = [listening, imagining, start_breaks, end_breaks]
    print(f"Results length: {len(results)}")

    for r in results:
        time_occurence = [round(r.empirical_p[i] + r.n_data_points / r.fs, 2) for i in range(4)]
        time_occurences.append(time_occurence)
    # Get all parameters
    params = {
        "name": results[0].name,
        "activity": results[0].activity,
        "method": results[0].method,
        "n_samples": [r.n_data_points for r in results],
        "n_channels": [r.n_channels for r in results],
        "n_maps": [len(r.cluster_centers) if r.cluster_centers is not None else 4 for r in results],
        "p_empirical": [r.empirical_p for r in results],
        "time_occurrences": time_occurences,
        "total_time": [r.total_time for r in results],
        "max_entropy": [r.h_max for r in results],
        "entropy": [r.h for r in results],
        "mc_entropy": [r.h_mc for r in results],
        "alpha": [results[0].alpha],
        "markov_p0": ["{:.2E}".format(Decimal(str(r.p_markov_test_0))) for r in results],
        "markov_p1": ["{:.2E}".format(Decimal(str(r.p_markov_test_1))) for r in results],
        "markov_p2": ["{:.2E}".format(Decimal(str(r.p_markov_test_2))) for r in results],
        "symmetry_p": ["{:.2E}".format(Decimal(str(r.p_symmetry_test))) for r in results],
        "cond_homo_p": ["{:.2E}".format(Decimal(str(r.p_conditional_homogenity))) for r in results],
        "stats": [r.stats for r in results],
        "analyse_breaks": analyse_breaks,
        "separate_states": separate_states,
        "GEV": [r.gev for r in results],
        "microstate_labels": ['A', 'B', 'C', 'D']
    }

    # Write html file
    comparison_content = template.render(params)
    comparison_path = os.path.join(destination_path, "comparison.html")

    with open(comparison_path, mode='w', encoding="utf-8") as file:
        file.write(comparison_content)
    print(f"Comparison done.\n"
          f"Available in {comparison_path}")
    
def load_pickle(filename):
    """
    Load pickle file
    Args:
        filename: String,
        Path to a pickled file, e.g. results in this case
    Returns:
        Path to a pickle file
    """
    if filename:
        with open(filename, 'rb') as file:
            results = pickle.load(file)
            return results