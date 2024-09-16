import numpy as np
from clustering.models.abstractModel import AbstractModel

class KMedoidsModel(AbstractModel):

    def cluster_microstates(self, data, n_runs=10, max_iter=500):
        """
        Clustering with k-medoids
        Args:
            data: numpy array,
                EEG data to create clusters, shape n_data x n_channels
            n_runs: Int
                Number of runs to perform
            max_iter: Int
                Maximal mumber of iterations
        Returns: numpy array n_maps x n_channels,
            Maps of cluster centers
        Notes:
            Also Saves n_channels and cluster_centers to the results of model
        """
        n_channels = data.shape[1]
        self.results.n_channels = n_channels
        n_clusters = self.n_maps
        data_copy = np.copy(data)
        gfp = np.std(data_copy, axis=1)
        gfp_peaks = self.get_local_maxima(gfp)
        data_copy = data_copy[gfp_peaks, :]
        data_cluster_norm = data_copy - data_copy.mean(axis=1, keepdims=True)
        data_cluster_norm /= data_cluster_norm.std(axis=1, keepdims=True)
        corr = np.corrcoef(data_cluster_norm)
        corr = corr ** 2
        n = corr.shape[0]
        dpsim = np.zeros((n, n_runs))
        idx = np.zeros((n, n_runs))
        maps_array = []
        for rep in range(n_runs):
            tmp = np.random.permutation(range(n))
            mu = tmp[:n_clusters]
            t = 0
            done = (t == max_iter)
            while not done:
                t += 1
                mu_old = mu
                dpsim[t, rep] = 0
                cl = np.argmax(corr[:, mu], axis=1)
                cl[mu] = range(n_clusters)
                for j in range(n_clusters):
                    I = np.where(cl == j)[0]
                    S_I_rowsum = np.sum(corr[I][:, I], axis=0)
                    Scl = max(S_I_rowsum)
                    ii = np.argmax(S_I_rowsum)
                    dpsim[t, rep] = dpsim[t, rep] + Scl
                    mu[j] = I[ii]
                if all(mu_old == mu) | (t == max_iter):
                    done = 1
            idx[:, rep] = mu[cl]
            dpsim[t + 1:, rep] = dpsim[t, rep]
            k_medoids_maps = np.unique(idx)
            maps = [(data_copy[k_medoids_maps.astype(int)[k]]) for k in range(n_clusters)]
            maps_array = np.array(maps)
            self.results.cluster_centers = maps_array
        return maps_array
