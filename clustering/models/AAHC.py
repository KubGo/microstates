import numpy as np
from clustering.models.abstractModel import AbstractModel

class AAHCModel(AbstractModel):

    def cluster_microstates(self, data):
        """
        Clustering with AAHC
        Args:
            data: numpy array,
                EEG data to create clusters, shape n_data x n_channels
        Returns: numpy array n_maps x n_channels,
            Maps of cluster centers
        Notes:
            Also Saves n_channels and cluster_centers to the results of model
        """
        n_clusters = self.n_maps

        def extract_row(A, k):
            v = A[k, :]
            A_ = np.vstack((A[:k, :], A[k + 1:, :]))
            return A_, v

        def extract_item(A, k):
            a = A[k]
            A_ = A[:k] + A[k + 1:]
            return A_, a

        n, n_channels = data.shape
        self.results.n_channels = n_channels
        gfp = data.std(axis=1)
        gfp_peaks = self.get_local_maxima(gfp)
        gfp_norm = np.sum(gfp ** 2)

        peak_maps = data[gfp_peaks, :]
        cluster_data = data[gfp_peaks, :]
        n_peak_maps = peak_maps.shape[0]
        print(f"Initial number of clusters: {n_peak_maps:d}\n")
        # -- cluster indices w.r.t. original size, normalized GFP peak data -- #
        peaks_indexes = [[k] for k in range(n_peak_maps)]

        # -- main loop: atomize + agglomerate -- #
        while n_peak_maps > n_clusters:
            blank_ = 80 * " "
            print(f"\r{blank_:s}\r\t\tAAHC > n: {n_peak_maps:d} => {n_peak_maps - 1:d}", end="")

            # -- correlations of the data sequence with each cluster -- #
            data_mean, data_std = data.mean(axis=1, keepdims=True), data.std(axis=1)
            maps_mean, maps_std = peak_maps.mean(axis=1, keepdims=True), peak_maps.std(axis=1)
            std_data_maps = 1. * n_channels * np.outer(data_std, maps_std)
            corr = np.dot(data - data_mean, np.transpose(peak_maps - maps_mean)) / std_data_maps

            # -- microstate sequence, ignore polarity -- #
            microstates_chain = np.argmax(corr ** 2, axis=1)

            # -- Global explained variance (GEV) of cluster k -- #
            gev = np.zeros(n_peak_maps)
            for k in range(n_peak_maps):
                r = microstates_chain == k
                gev[k] = np.sum(gfp[r] ** 2 * corr[r, k] ** 2) / gfp_norm
            imin = np.argmin(gev)

            peak_maps, _ = extract_row(peak_maps, imin)
            peaks_indexes, maps_to_re_assign = extract_item(peaks_indexes, imin)
            re_clustered_maps = []
            # -- re-assigning the maps -- #
            for k in maps_to_re_assign:
                current_map = cluster_data[k, :]
                peak_maps_mean, peak_maps_std = peak_maps.mean(axis=1, keepdims=True), peak_maps.std(axis=1)
                current_map_mean, current_map_std = current_map.mean(), current_map.std()
                std_data_maps = 1. * n_channels * peak_maps_std * current_map_std
                corr = np.dot(peak_maps - peak_maps_mean, current_map - current_map_mean) / std_data_maps
                new_index = np.argmax(corr ** 2)
                re_clustered_maps.append(new_index)
                peaks_indexes[new_index].append(k)
            n_peak_maps = len(peaks_indexes)

            # -- unique clusters list -> updated clusters -- #
            re_clustered_maps = list(set(re_clustered_maps))

            # -- re-clustering by eigenvector method -- #
            for i in re_clustered_maps:
                idx = peaks_indexes[i]
                Vt = cluster_data[idx, :]
                Sk = np.dot(Vt.T, Vt)
                eigenvalues, eigenvectors = np.linalg.eig(Sk)
                c = eigenvectors[:, np.argmax(np.abs(eigenvalues))]
                c = np.real(c)
                peak_maps[i] = c / np.sqrt(np.sum(c ** 2))

        print()
        self.results.cluster_centers = peak_maps
        return peak_maps