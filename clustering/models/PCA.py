import numpy as np
from sklearn.decomposition import PCA
from clustering.models.abstractModel import AbstractModel

class PCAModel(AbstractModel):
    def cluster_microstates(self, data, copy=True, whiten=True, svd_solver="auto"):
        """
        Clustering with PCA based on sklearn.decomposition.PCA
        Args:
            data: data: numpy array,
                EEG data to create clusters, shape n_data x n_channels
            copy: Boolean,
                If True, data will not be overwritten
            whiten: Boolean,
                If True, remove relative variance scales of components,
                further info in sklearn documentation
            svd_solver: String,
                Solver to use from 'auto', 'full', 'arpack', 'randomized'
        Returns: numpy array n_maps x n_channels,
            Maps of cluster centers
        Notes:
            Also Saves n_channels and cluster_centers to the results of model
            For more info, see here:
            https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
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
            "copy": copy,
            "whiten": whiten,
            "svd_solver": svd_solver}
        pca = PCA(**params)
        pca.fit(data_cluster_norm)
        maps = np.array(pca.components_)
        del pca, params
        self.results.cluster_centers = maps
        return maps