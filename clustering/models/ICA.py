import numpy as np
from sklearn.decomposition import FastICA
from clustering.models.abstractModel import AbstractModel
from clustering.utilities import reorder_microstates

class ICAModel(AbstractModel):
    def cluster_microstates(self, data, algorithm='parallel', whiten='arbitrary-variance', fun='exp', max_iter=200):
        """
        Clustering with Fast-ICA based on sklearn.decomposition.FastICA
        Args:
            data: numpy array,
                EEG data to create clusters, shape n_data x n_channels
            algorithm: {'parallel', 'deflation'}
                Algorithm to use
            whiten: String or False
                Whitening strategy to use,
                further information sklean documentation
            fun: String
                Function for approximation to neg-entropy
            max_iter: int,
                Maximum number of iteration during fit
        Returns: numpy array n_maps x n_channels,
            Maps of cluster centers
        Notes:
            Also Saves n_channels and cluster_centers to the results of model
            For more info, see here:
            https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.FastICA.html
        """
        n_clusters = self.n_maps
        self.results.n_channels = data.shape[1]

        gfp = data.std(axis=1)
        gfp_peaks = self.get_local_maxima(gfp)
        data_cluster = data[gfp_peaks, :]
        data_cluster_norm = data_cluster - data_cluster.mean(axis=1, keepdims=True)
        data_cluster_norm /= data_cluster_norm.std(axis=1, keepdims=True)

        params = {
            "n_components": n_clusters,
            "algorithm": algorithm,
            "whiten": whiten,
            "fun": fun,
            "max_iter": max_iter}

        ica = FastICA(**params)
        S_ = ica.fit_transform(data_cluster_norm)
        maps = np.array([ica.components_[k, :] for k in range(n_clusters)])
        maps = reorder_microstates(maps)
        self.results.cluster_centers = maps
        return maps