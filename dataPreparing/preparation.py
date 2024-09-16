import os
import pandas as pd
from art import tprint

def prepare_folder(path_to_folder, destination_path, time=5, fs=250):
    """
    Prepares data in folder by deleting time x fs samples from start and end at each file
    Args:
        path_to_folder: String,
            path to a folder containing csv files
        destination_path: String,
            path to a folder to save csv files
        time: int, default = 5,
            time to delete from start and end
        fs: int, default = 250,
            Sampling frequency
    """
    if not os.path.exists(path_to_folder):
        print(f"There is no such a folder as {path_to_folder},\n"
              f"check if it is a correct name")
    files = [os.path.join(path_to_folder, f) for f in os.listdir(path_to_folder) if
             os.path.isfile(os.path.join(path_to_folder, f))]
    for file in files:
        prepare_file(file, destination_path, time, fs)
        print(f"{os.path.basename(file)} - done.")
    print(f"Data in {os.path.abspath(path_to_folder)} prepared \n"
          f"and saved in {os.path.abspath(destination_path)}")


def prepare_file(path_to_file, destination_path=None, time=5, fs=250):
    """
    Prepare data in file by deleting time x fs samples from start and end
    Args:
        path_to_file: String,
            Path to a file to clean
        destination_path: String,
            Path to a destination folder to save the data,
            if None, don't save
        time: float, default=5,
            Time in seconds to delete from the start and end
        fs: int, default=250,
            Frequency of data sampling
    Returns: numpy array,
        Returns cleaned numpy array that is saved in destination path as csv file
    """
    if not os.path.exists(path_to_file):
        print("There is no such a file.")
        return
    file_name = os.path.basename(path_to_file)
    name, extension = os.path.splitext(file_name)
    if extension != ".csv":
        print("Only csv files reading")
        return
    data = pd.read_csv(path_to_file, index_col=0)
    samples_to_delete = round(time * fs)
    clean_data = data.iloc[samples_to_delete:-samples_to_delete, :]
    if destination_path is not None:
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        path_to_save = os.path.join(destination_path, file_name)
        clean_data.to_csv(path_to_save)
    return clean_data.to_numpy()


def concat_from_folder(path_to_folder, breaks_time=5, fs=250):
    """
    Concatenates all files csv files from folder with 2s break given at break_times_dict
    Args:
        path_to_folder: String,
            Path to a folder
        breaks_time: int, default=5,
            Time of breaks at start and end of data
        fs: int, default=250,
            Frequency of sampling
    Returns:
        Numpy array: Concatenated csv data
    """
    df = pd.DataFrame()
    if not os.path.exists(path_to_folder):
        raise FileNotFoundError(f"There isn't such a folder as: {path_to_folder}")

    files = [os.path.join(path_to_folder, f) for f in os.listdir(path_to_folder) if
             os.path.isfile(os.path.join(path_to_folder, f))]

    # Check if at least two csv inside
    csv_count = 0
    for file in files:
        file_name = os.path.basename(file)
        name, extension = os.path.splitext(file_name)
        if extension == ".csv":
            csv_count += 1
            if csv_count == 2:
                break
    if csv_count < 2:
        raise FileNotFoundError(f"There is not enough csv to concat or there are any csv in folder {path_to_folder}")
    for file in files:
        file_name = os.path.basename(file)
        name_file, extension = os.path.splitext(file_name)
        if extension == ".csv":
            df_to_add = pd.read_csv(file, index_col=0)
            break_records = breaks_time * fs
            df_to_add = df_to_add.iloc[break_records:-break_records, :]
            df = pd.concat([df, df_to_add])
            print(f"{os.path.basename(file)} - done.")

    print("All csv files concatenated with breaks given at times dict")
    return df.to_numpy()


def create_breaks_files(path_to_folder, destination_path,
                        time_start_end=5, fs=250):
    """
    Create csv files with start and end breaks of activities
    Args:
        path_to_folder: String,
            Path to a folder with csv files
        destination_path: String,
            Path to a folder to save the csv file
        time_start_end: int, default = 5,
            Time to cut from start and end of file as a break
        fs: int, default = 250,
            Sampling frequency
    Returns:String,
        Path to saved break times csv
    """
    if not os.path.exists(path_to_folder):
        print(f"Print there is no such a folder as: {path_to_folder}")

    files = [os.path.join(path_to_folder, f) for f in os.listdir(path_to_folder) if
             os.path.isfile(os.path.join(path_to_folder, f))]
    name = None
    starting_break = time_start_end * fs
    ending_break = time_start_end * fs
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    for file in files:
        file_name_path, extension = os.path.splitext(file)
        if extension == ".csv":
            file_name = os.path.basename(file)
            print(file_name)
            file_name = file_name.split("_")
            name = file_name[0]
            activity = "_".join(file_name[1:file_name.index("clean")])

            data = pd.read_csv(file, index_col=0)
            # paths to save breaks data files
            path_to_save_start = os.path.join(destination_path, "_".join([name, activity, "start_break.csv"]))
            break_data_start = data.iloc[:starting_break, :]  # Starting break
            break_data_start.to_csv(path_to_save_start)
            path_to_save_end = os.path.join(destination_path, "_".join([name, activity, "end_break.csv"]))
            break_data_end = data.iloc[-ending_break:, :]  # Ending break
            break_data_end.to_csv(path_to_save_end)

    print("Breaks data saved")
    return os.path.join(destination_path)

def concat_activities(path_to_folder, destination_path, time=5, fs=250, analyse_breaks=False):
    """
    Create concatenated csv files for single activity with data from all participants
    Args:
        analyse_breaks:
        path_to_folder: String, path,
            Path to folder that contains folders for all participants data
        destination_path: String, path,
            Destination path to save that data
        time: int, default=5,
            Time of start and end breaks for each activity
        fs: int, default=250,
            Sampling frequency

    Returns:
        Path to folders with prepared data
    """
    if not os.path.exists(path_to_folder):
        print(f"There is no such a folder as {path_to_folder},\n"
              f"check if it is a correct name")

    # Get folders for each participant
    folders = [os.path.join(path_to_folder, f) for f in os.listdir(path_to_folder) if
             os.path.isdir(os.path.join(path_to_folder, f))]

    # Check and create destination paths
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    path_to_concatenated_files = os.path.join(destination_path, "concatenatedActivities")
    if not os.path.exists(path_to_concatenated_files):
        os.makedirs(path_to_concatenated_files)

    # Create dict to store data frames
    concated_files = {
        "Your_Home_Venue": pd.DataFrame(),
        "Training_Session": pd.DataFrame(),
        "Successful_Competition": pd.DataFrame(),
        "Start_high_level_championship": pd.DataFrame(),
        "Slow_Start": pd.DataFrame(),
        "Fitness_Activity": pd.DataFrame()
    }

    for folder in folders:
        name = os.path.basename(folder)
        tprint(name)
        files = [os.path.join(folder, f) for f in os.listdir(folder) if
                 os.path.isfile(os.path.join(folder, f))]
        path_to_save_files = os.path.join(destination_path, name)
        if analyse_breaks:
            breaks_folder = os.path.join(path_to_save_files, "breaks")
            create_breaks_files(folder, breaks_folder)
        for file in files:
            file_name_path, extension = os.path.splitext(file)
            if extension == ".csv":
                file_name = os.path.basename(file)
                print(file_name)
                file_name_list = file_name.split("_")
                activity = "_".join(file_name_list[1:file_name_list.index("clean")])
                if activity == 'Squats':
                    print(f"Skipping {activity}")
                    continue
                prepare_file(file, path_to_save_files)
                path_to_saveed_pd_file = os.path.join(path_to_save_files, file_name)
                df = pd.read_csv(path_to_saveed_pd_file, index_col=0)
                old_df = concated_files[activity]
                new_df = pd.concat([df, old_df])
                concated_files[activity] = new_df

    for activity, data in concated_files.items():
        path_to_save = os.path.join(path_to_concatenated_files, activity + "_concatenated.csv")
        data.to_csv(path_to_save)
        print(f"Concatenated activity-{activity} done.")

def readTestFile(test_file_path, delimiter = "_", name_group = 1, prepared=False, time = 5, fs=250, index_col = 0):
    """Reads test file data from csv of eeg

    Args:
        test_file_path (Path, String): Path to csv file containing eeg data
        delimiter (str, optional): Delimiter used to separate parts of file name, eg. participant_testDescription_date Defaults to "_".
        name_group (int, optional): Group where the test description is, eg. for participant_testDescription_date it would be 1. Defaults to 1.
        prepared (bool, optional): If true, data is prepared and the data preparation is ommited. Defaults to False.
        time (int, optional): Time to delete from start and end if the preparation of data is needed. Defaults to 5.
        fs (int, optional): Sampling frequency of the data. Number of data points captured per second Defaults to 250.
        index_col (int, optional): Index column of the data. Defaults to 0.

    Raises:
        FileNotFoundError: Raises if the file doesn't exist. 

    Returns:
        dict: Dictionary describing the test in form: {testDescription : testData}
    """
    if not os.path.exists(test_file_path):
        raise FileNotFoundError(f"There is not such a file as {test_file_path}\n" +
                                f"Check if the specified path is correct.")
    file_name = os.path.basename(test_file_path).split(delimiter)[name_group]
    if not prepared:
        data = prepare_file(test_file_path)
        return {
            "testDescription": file_name,
            "data": data
        }
    return {
            "testDescription": file_name,
            "data": pd.read_csv(test_file_path, index_col=index_col).to_numpy()
        }

def readTestFiles(test_files_path, delimiter = "_", name_group = 1, prepared=False, time = 5, fs=250, index_col = 0 ):
    """Reads test files from folder

    Args:
        test_files_path (Path, String): Path to a folder containing csv files with test results
        delimiter (str, optional): Delimiter used to separate parts of file name, eg. participant_testDescription_date Defaults to "_".
        name_group (int, optional): Group where the test description is, eg. for participant_testDescription_date it would be 1. Defaults to 1.
        prepared (bool, optional): If true, data is prepared and the data preparation is ommited. Defaults to False.
        time (int, optional): Time to delete from start and end if the preparation of data is needed. Defaults to 5.
        fs (int, optional): Sampling frequency of the data. Number of data points captured per second Defaults to 250.
        index_col (int, optional): Index column of the data. Defaults to 0.


    Returns:
        List: List of dictionaries describing the tests in form: {testDescription : testData}
    """
    test_files = [os.path.join(test_files_path, f) for f in os.listdir(test_files_path) if os.path.isfile(os.path.join(test_files_path, f))]
    test_data_list = []
    for test_file_path in test_files:
        test_data_list.append(readTestFile(test_file_path,
                                           delimiter = delimiter,
                                           name_group = name_group,
                                           prepared=prepared,
                                           time = time,
                                           fs=fs,
                                           index_col = index_col))
    return test_data_list
