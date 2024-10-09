import numpy as np
from sklearn.cluster import DBSCAN
from clustering.models.abstractModel import AbstractModel
from clustering.utilities import reorder_microstates

class DBScanModel(AbstractModel):
    def cluster_microstates(self, data, eps=100, min_samples=10):
        """
        Prototype clustering with DBScan based on sklearn.cluster.DBSCAN
        Args:
            data: numpy array,
                EEG data to create clusters, shape n_data x n_channels
            eps: float,
                Maximum distance between two samples for one to be considered
                as in the neighbourhood
            min_samples: int,
                The number of samples in a neighborhood for a point to be
                considered as a core point
        Returns:
            umpy array n_maps x n_channels,
            Maps of cluster centers
        Notes:
            It is only a prototype function and may not return a valid cluster centers
            and set method as None
            Also Saves n_channels and cluster_centers to the results of model
            For more info, see here:
            https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html
        """
        self.results.n_channels = data.shape[1]
        data_copy = np.copy(data)
        gfp = np.std(data_copy, axis=1)
        gfp_peaks = self.get_local_maxima(gfp)
        peaks_data = data_copy[gfp_peaks, :]
        

        # def objective(trial):
        #     dbscan_model = DBSCAN(eps=trial.suggest_float("eps", 0.0001, 100.0))
        #     dbscan_model.fit(peaks_data)
        #     clusters_number = len(dbscan_model.core_sample_indices_)
        #     return abs(clusters_number - self.n_maps)
        # study = optuna.create_study(direction="minimize",
        #                             sampler=optuna.samplers.TPESampler(seed=1234))
        # study.optimize(objective, n_trials=200)
        # params = study.best_params
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        dbscan.fit(data_copy)
        cluster_centers = []
        # print(len(dbscan.core_sample_indices_))
        i = 0
        while len(cluster_centers) < 4:
            index = dbscan.core_sample_indices_[i]
            i += 1
            if index < 0:
                continue
            cluster_center = data_copy[index, :]
            cluster_centers.append(cluster_center)
            
        dbscan.core_sample_indices_
        cluster_centers = reorder_microstates(np.array(cluster_centers))
        self.results.cluster_centers = np.array(cluster_centers)