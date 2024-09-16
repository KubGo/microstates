import numpy as np
from clustering.models.abstractModel import AbstractModel

class KMeansModel(AbstractModel):

    def cluster_microstates(self, data, n_runs=10, max_error=1e-6, max_iter=500):
        """
            Clustering with k-means
        Args
            data: numpy array,
                EEG data to create clusters, shape n_data x n_channels
            n_runs: int, default=10,
                Number of runs for clustering
            max_error: float, default=1e-6,
                Error at witch clustering stops
            max_iter: int, default=500,
                Number of iterations to stop clustering
        Returns: numpy array n_maps x n_channels,
            Maps of cluster centers
        Notes:
            Also Saves n_channels and cluster_centers to the results of model
        """
        # TODO: Check correctness
        n_data = data.shape[0]
        n_channels = data.shape[1]
        self.results.n_channels = n_channels

        # Lower data by mean value??? don't know if it's needed
        data = data - data.mean(axis=1, keepdims=True)

        gfp = np.std(data, axis=1)
        gfp_peaks = self.get_local_maxima(gfp)
        # Get values of local peaks
        gfp_values = gfp[gfp_peaks]
        gfp2 = np.sum(gfp_values ** 2)  # Normalizing constant in GEV ?
        n_gfp = gfp_peaks.shape[0]

        #  clustering of GFP peak only
        peak_maps = data[gfp_peaks, :]
        sum_peak2 = np.sum(peak_maps ** 2)

        # Results for each k-means run

        cv_list = []  # cross-validation criterion for each k-means run
        gev_list = []  # GEV of each map for each k-means run
        gevT_list = []  # total GEV values for each k-means run
        maps_list = []  # microstate maps for each k-means run
        L_list = []  # microstate label sequence for each k-means run

        for run in range(n_runs):
            # initialize random cluster centroids (indices w.r.t. n_gfp)
            # get 4 random peaks
            np.random.seed(42)
            rndi = np.random.permutation(n_gfp)[:self.n_maps]
            maps = peak_maps[rndi, :]
            # Normalize row-wise
            maps /= np.sqrt(np.sum(maps ** 2, axis=1, keepdims=True))
            # initialize
            n_iter = 0
            var0 = 1.0
            var1 = 0.0
            # convergence criterion: variance estimate (step 6)
            while (np.abs((var0 - var1) / var0) > max_error) & (n_iter < max_iter):
                # (step 3) microstate sequence (= current cluster assignment)
                C = np.dot(peak_maps, maps.T)
                C /= (n_channels * np.outer(gfp[gfp_peaks], np.std(maps, axis=1)))
                L = np.argmax(C ** 2, axis=1)
                # step 4
                for k in range(self.n_maps):
                    peak_maps_t = peak_maps[L == k, :]
                    # (step 4a)
                    Sk = np.dot(peak_maps_t.T, peak_maps_t)
                    # (step 4b)
                    eigenvalues, eigenvectors = np.linalg.eig(Sk)
                    v = eigenvectors[:, np.argmax(np.abs(eigenvalues))]
                    v = v.real
                    maps[k, :] = v / np.sqrt(np.sum(v ** 2))
                # (Step 5)
                var1 = var0
                var0 = sum_peak2 - np.sum(np.sum(maps[L, :] * peak_maps, axis=1) ** 2)
                var0 /= (n_gfp * (n_channels - 1))
                n_iter += 1
            if n_iter < max_iter:
                print((f"\tK-means run {run + 1:d}/{n_runs:d} converged after "
                       f"{n_iter:d} iterations."))
            else:
                print((f"\tK-means run {run + 1:d}/{n_runs:d} did NOT converge "
                       f"after {max_iter:d} iterations."))

            # CROSS-VALIDATION criterion for this run (step 8)
            C_ = np.dot(data, maps.T)
            C_ /= (n_channels * np.outer(gfp, np.std(maps, axis=1)))
            L_ = np.argmax(C_ ** 2, axis=1)
            var = np.sum(data ** 2) - np.sum(np.sum(maps[L_, :] * data, axis=1) ** 2)
            var /= (n_data * (n_channels - 1))
            cv = var * (n_channels - 1) ** 2 / (n_channels - self.n_maps - 1.) ** 2

            # GEV (global explained variance) of cluster k
            gev = np.zeros(self.n_maps)
            for k in range(self.n_maps):
                r = L == k
                gev[k] = np.sum(gfp_values[r] ** 2 * C[r, k] ** 2) / gfp2
            gev_total = np.sum(gev)

            # store
            cv_list.append(cv)
            gev_list.append(gev)
            gevT_list.append(gev_total)
            maps_list.append(maps)
            L_list.append(L_)

        # select best run
        k_opt = np.argmin(cv_list)
        maps = maps_list[k_opt]
        gev = gev_list[k_opt]
        L_ = L_list[k_opt]

        self.results.cluster_centers = maps
        return maps