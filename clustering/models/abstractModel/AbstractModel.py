import os
import pickle
from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
import datetime

from math import log2
from scipy.stats import chi2
from sklearn.decomposition import PCA
from clustering.models.markovTests import MarkovTest
from clustering.results import results_factory
from clustering.utilities import entropy

CAP_XYZ_PATH = os.path.abspath('cap2.csv')


class AbstractModel(ABC):
    """
        Abstract class to work as an interface
        to more detailed classes for operations
        on microstates

    """
    results = None

    def __init__(self, method=None, activity=None, filename=None, n_maps=4, f_sampling=250):
        self.method = method
        self.activity = activity
        self.filename = filename
        self.n_maps = n_maps
        self.f_sampling = f_sampling
        self.results = results_factory(filename, method)
        self.results.fs = f_sampling

    @abstractmethod
    def cluster_microstates(self, data):
        pass

    def transform_to_microstates(self, data, interpol=False):
        """
        Transforms data to chain of microstates
        Args:
            data: numpy array number of data x number of channels,
                EEG data to convert into chain of microstates
            interpol: Boolean,
                If True, interpolate to the closest peak value
        Returns:
            numpy array,
                List of microstates that occur in data
        """
        maps = self.results.cluster_centers
        if maps is None:
            print("There are no clusters to perform transformation.\n"
                  "Performing clustering for default arguments first.")
            self.cluster_microstates(data)
            maps = self.results.cluster_centers
            if maps is None:
                print("No cluster centers for this method.")
                return
        gfp_peaks = self.get_local_maxima(data.std(axis=1))
        n_channels = self.results.n_channels
        self.results.n_data_points = data.shape[0]

        # --- normalized data ---
        data_norm = data - data.mean(axis=1, keepdims=True)
        data_norm /= data_norm.std(axis=1, keepdims=True)

        # -- GEV -- #
        maps_norm = maps - maps.mean(axis=1, keepdims=True)
        maps_norm /= maps_norm.std(axis=1, keepdims=True)

        # -- Data cluster data -- #
        data_cluster = data[gfp_peaks, :]
        data_cluster_norm = data_cluster - data_cluster.mean(axis=1, keepdims=True)
        data_cluster_norm /= data_cluster_norm.std(axis=1, keepdims=True)

        if interpol:
            # interpolates to peaks
            corr = np.dot(data_cluster_norm, maps.T) / n_channels  # get correlation to the microstates
            microstates_at_gfp = np.argmax(corr ** 2, axis=1)  # microstates at GFP peak
            del corr
            n_data = data_norm.shape[0]
            microstates_chain = np.zeros(n_data)
            for t in range(n_data):
                # If microstate is a peak, get microstate from microstates_at_gfp
                if t in gfp_peaks:
                    i = gfp_peaks.tolist().index(t)
                    microstates_chain[t] = microstates_at_gfp[i]
                else:
                    # Check what peak is closes and add its microstate
                    i = np.argmin(np.abs(t - gfp_peaks))
                    microstates_chain[t] = microstates_at_gfp[i]
            microstates_chain = microstates_chain.astype('int')
        else:
            # Check which microstate map correlates the most with actual state
            corr = np.dot(data_norm, maps.T) / n_channels
            microstates_chain = np.argmax(corr ** 2, axis=1)
            del corr

        self.results.data_for_gif = data
        self.results.clusters_chain = microstates_chain
        return microstates_chain

    def plot_data(self, data, f_sampling=None):
        """Plot the data

        Args:
            data: numpy array
                Data to plot
            f_sampling: int
                Frequency of sampling [Hz]

        Returns:
            Plots the data
        """

        if f_sampling is None:
            f_sampling = self.f_sampling

        # Time axis in seconds
        t = np.arange(len(data)) / f_sampling

        fig = plt.figure(1, figsize=(20, 4))
        plt.plot(t, data, '-k', linewidth=1)
        plt.xlabel("time [s]", fontsize=24)
        plt.ylabel(r"Potential [\mu V]", fontsize=24)
        plt.tight_layout()
        plt.show()

    def calculate_p_empirical(self, data, n_clusters=None):
        """
        Empirical symbol distribution
        Args:
            data: numpy array
                EEG microstates data
            n_clusters: int
                Number of microstate clusters, default=self.n_maps
        Returns:
            p: empirical distribution
        """
        if n_clusters is None:
            n_clusters = self.n_maps

        p = np.zeros(n_clusters)
        n = len(data)

        for i in range(n):
            p[data[i]] += 1.0
        p /= n
        self.results.empirical_p = p
        return p

    def get_transition_matrix(self, data, n_clusters=None):
        """
        Calculates transition matrix of microstates
        Args:
            data: numpy array
                EEG microstates data
            n_clusters:  int
                Number of microstate clusters, default=self.n_maps
        Returns:
            transition_matrix: Empirical transition matrix of states
        """
        if n_clusters is None:
            n_clusters = self.n_maps

        transition_matrix = np.zeros((n_clusters, n_clusters))
        n = len(data)
        for i in range(n - 1):
            transition_matrix[data[i], data[i + 1]] += 1.0
        p_row = np.sum(transition_matrix, axis=1)
        for i in range(n_clusters):
            if p_row[i] != 0.0:
                for j in range(n_clusters):
                    transition_matrix[i, j] /= p_row[i]
        self.results.transition_matrix = transition_matrix

        return transition_matrix

    def get_max_entropy(self, n_clusters=None):

        if n_clusters is None:
            n_clusters = self.n_maps
        propability = 1 / n_clusters
        probabilities = [propability for _ in range(n_clusters)]
        h_max = entropy(probabilities)
        self.results.h_max = h_max
        return h_max

    def markov_test(self, microstates_chain: list, order: int, alpha=0.01, n_clusters=None):
        """
        Test for Markovianity of given order
        Args:
            microstates_chain: numpy array or list
                Microstates chain
            n_clusters: int, default number of maps
                Number of clusters
            alpha: float, dafualt 0.01
                Significance level
            order: int
                Order of Markovian test
        Returns:
            p: p-value of the Chi2 test for independence
        """
        if n_clusters is None:
            n_clusters = self.n_maps
        test = MarkovTest(microstates_chain, n_clusters, alpha)
        p = test.test_markov(order)
        self.results.set_markov_test(order, p)
        return p

    def symmetry_test(self, microstates_chain: list, alpha=0.01, n_clusters=None):
        """
        Check symmetry of microstates sequence
        Args:
            microstates_chain: numpy array or list
                Microstates chain
            n_clusters: int, default number of maps,
                Number of clusters
            alpha: float, default 0.01
                Significance level
        Returns:
            p: p-value of the Chi2 test for independence
        """
        if n_clusters is None:
            n_clusters = self.n_maps
        n = len(microstates_chain)
        f_ij = np.zeros((n_clusters, n_clusters))
        for t in range(n - 1):
            i = microstates_chain[t]
            j = microstates_chain[t + 1]
            f_ij[i, j] += 1.0
        T = 0.0
        for i, j in np.ndindex(f_ij.shape):
            if i != j:
                f = f_ij[i, j] * f_ij[j, i]
                if f > 0:
                    num_ = 2 * f_ij[i, j]
                    den_ = f_ij[i, j] + f_ij[j, i]
                    T += (f_ij[i, j] * np.log(num_ / den_))
        T *= 2.0
        df = n_clusters * (n_clusters - 1) / 2
        # p = chi2test(T, df, alpha)
        p = chi2.sf(T, df, loc=0, scale=1)
        self.results.p_symmetry_test = p
        return p

    def get_local_maxima(self, x: np.array):
        """
        Get indexes of local maxima of 1D-array
        Args:
            x: numpy array
            numeric sequence
        Returns:
            maximas: list of local maxima
        """
        dx = np.diff(x)
        zc = np.diff(np.sign(dx))
        maxima = 1 + np.where(zc == -2)[0]
        self.results.maxima = maxima
        return maxima

    def get_potential_energy_alpha_wave(self, data):
        """
        Saves points of potential energy alpha wave to results
        Args:
            data: numpy array,
            EEG data
        """
        pca = PCA(copy=True, n_components=1, whiten=False)
        alpha_wave = pca.fit_transform(data)
        self.results.alpha_wave = alpha_wave

    def global_explained_variance(self, data):
        """
        Saves GEV to results
        Args:
            data: numpy.array
                EEG data
        """
        if self.results.cluster_centers is None:
            print("Clustering hasn't been done or there are no cluster centers.")
            return
        microstates_chain = self.results.clusters_chain
        if microstates_chain is None:
            microstates_chain = self.transform_to_microstates(data)

        n_channels = data.shape[1]
        n_clusters = self.n_maps

        gfp = np.std(data, axis=1)
        gfp2 = np.sum(gfp ** 2)

        maps = self.results.cluster_centers
        maps_norm = maps - maps.mean(axis=1, keepdims=True)
        maps_norm /= maps_norm.std(axis=1, keepdims=True)

        data_norm = data - data.mean(axis=1, keepdims=True)
        data_norm /= data_norm.std(axis=1, keepdims=True)

        corr = np.dot(data_norm, maps_norm.T) / n_channels

        gev = np.zeros(n_clusters)
        for k in range(n_clusters):
            r = microstates_chain == k
            gev[k] = np.sum(gfp[r] ** 2 * corr[r, k] ** 2) / gfp2
        microstates_labels = ['A', 'B', 'C', 'D']
        self.results.gev = {
            f"microstate {microstates_labels[i]}": gev[i] for i in range(n_clusters)
        }
        self.results.gev["total"] = gev.sum()

    def perform_analysis(self, data, clustering=True, alpha=0.01, interpolMicrostates=False):
        """
        Performs whole analysis of data
        Args:
            data: numpy array
                EEG data to analyse
            clustering: Boolean,
                If True, perform clustering on the data.
                If False, use cluster centers from previous calculations.
            alpha: float, default=0.01,
                Significance level for statistical tests
        Returns:
            Results: Results class that contains all the calculations performed.
        Notes:
            Actions performed:
                - if clustering == True, clustering data,
                - data transformation to microstates,
                - potential energy of alpha wave calculations,
                - global explained variance calculations,
                - empirical symbol distribution calculation,
                - transition matrix of microstates chains calculation,
                - entropies calculations,
                - markov tests,
                - symmetry test,
                - conditional homogenity test.
        """
        if clustering:
            self.cluster_microstates(data)
        self.results.n_data_points = data.shape[0]
        # Set alpha for results
        self.results.alpha = alpha
        # Get microstates chain for data
        microstates_chain = self.transform_to_microstates(data, interpol=interpolMicrostates)
        # Get alpha wave potential energy
        self.get_potential_energy_alpha_wave(data)
        # Get global explained variance
        self.global_explained_variance(data)
        # Get empirical symbol distribution (probabilities of each microstate)
        self.calculate_p_empirical(microstates_chain)
        # Get transitions_matrix
        self.get_transition_matrix(microstates_chain)
        # Get maximal entropy of the microstates
        self.get_max_entropy()
        # Get entropy
        self.results.h = entropy(self.results.empirical_p)
        self.entropy_markov_chain(self.results.empirical_p, self.results.transition_matrix)
        # Markov tests of order 0, 1 and 2
        self.markov_test(microstates_chain, 0, alpha=alpha)
        self.markov_test(microstates_chain, 1, alpha=alpha)
        self.markov_test(microstates_chain, 2, alpha=alpha)
        # Symmetry test
        self.symmetry_test(microstates_chain, alpha=alpha)
        # Conditional homogenity test
        self.conditional_homogenity_test(microstates_chain, 500,  alpha=alpha)
        print("Analysis done.")
        return self.results

    def print_matrix(self, T: np.array):
        """
        Print console friendly matrix T
        Args:
            T: numpy array
                Matrix to print
        """

        for i, j in np.ndindex(T.shape):
            if j == 0:
                print("|{:.3f}".format(T[i, j]), end='')
            elif j == T.shape[1] - 1:
                print("{:.3f}|\n".format(T[i, j]), end='')
            else:
                print("{:.3f}".format(T[i, j]), end='')


    def save_model(self, path, model_name=None):
        """
        Saves model to specified path
        """
        if not os.path.exists(path):
            os.makedirs(path)
        if model_name is None:
            model_name = datetime.datetime.now().strftime("%d_%m_%y") + "_model.pickle"
        path_to_save_model = os.path.join(path, model_name)
        with open(path_to_save_model, 'wb') as file:
            pickle.dump(self, file, protocol=pickle.HIGHEST_PROTOCOL)

    def entropy_markov_chain(self, probabilities, transition_matrix):
        """
        Markov chain entropy rate
        Args:
            probabilities: list, numpy array
                Probabilities of each microstate
            transition_matrix: numpy array n_maps x n_maps
                Matrix of microstates transitions
        Returns:
            h: Markov chain entropy rate
        """
        h = 0
        for i, j in np.ndindex(transition_matrix.shape):
            if transition_matrix[i, j] > 0:
                h -= probabilities[i] * transition_matrix[i, j] * log2(transition_matrix[i, j])
        self.results.h_mc = h
        return h

    def conditional_homogenity_test(self, microstates_chain, block_length, n_cluster=None, alpha=0.01):
        """
        Test conditional homogenity
        Args:
            microstates_chain: numpy array, list,
                Microstates chain
            block_length: int,
                Length of divided block
            n_cluster: int, default n_maps
                Number of clusters
            alpha: float
                Significance level
        Returns:
            p value of 2 chi-squared test
        """
        if n_cluster is None:
            n_cluster = self.n_maps
        n_data = len(microstates_chain)
        n_blocks = int(np.floor(float(n_data) / float(block_length)))

        f_ijk = np.zeros((n_blocks, n_cluster, n_cluster))
        f_ij = np.zeros((n_blocks, n_cluster))
        f_jk = np.zeros((n_cluster, n_cluster))
        f_i = np.zeros(n_blocks)
        f_j = np.zeros(n_cluster)

        # Calculate f_ijk (time / block dep. transition matrix)
        for i in range(n_blocks):
            for ii in range(block_length - 1):
                j = microstates_chain[i * block_length + ii]
                k = microstates_chain[i * block_length + ii + 1]
                f_ijk[i, j, k] += 1
                f_ij[i, j] += 1
                f_jk[j, k] += 1
                f_i[i] += 1
                f_j[j] += 1

        T = 0.0
        for i, j, k in np.ndindex(f_ijk.shape):
            f = f_ijk[i, j, k] * f_j[j] * f_ij[i, j] * f_jk[j, k]
            if f > 0:
                num_ = f_ijk[i, j, k] * f_j[j]
                den_ = f_ij[i, j] * f_jk[j, k]
                T += (f_ijk[i, j, k] * log2(num_ / den_))
        T *= 2
        df = (n_blocks - 1) * (n_cluster - 1) * n_cluster
        p = chi2.sf(T, df, loc=0, scale=1)
        self.results.p_conditional_homogenity = p
        return p


