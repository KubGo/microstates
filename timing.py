from timeit import timeit

import os

NUMBER_OF_TESTS = 10
PATH_TO_TIME_RESULTS = 'prototyping/time_results.txt'
for method in ('kmeans', 'pca', 'ica', 'kmedoids', 'aahc', 'dbscan'):

    command = f"""
from testing import Test\nfrom clustering.models import model_factory\nfrom dataPreparing import readTestFile\nmodel = model_factory("P28", \"{method}\")\ntest_data = readTestFile("prototyping/P28/P28_Fitness_Activity_clean_signal.csv")\ntest = Test(model= model, test_data=test_data, break_time = 17.0)\ntest.test_data_separatly("prototyping/tempResults")\n
    """
    time = timeit(command, number=NUMBER_OF_TESTS)
    if not os.path.exists(PATH_TO_TIME_RESULTS):
        with open(PATH_TO_TIME_RESULTS,'x', encoding="utf-8") as file:
            file.write(f"{method} mean time to perform {time / NUMBER_OF_TESTS}")
    else:
        with open(PATH_TO_TIME_RESULTS, 'a', encoding="utf-8") as file:
            file.write(f"{method} mean time to perform {time / NUMBER_OF_TESTS}")
          