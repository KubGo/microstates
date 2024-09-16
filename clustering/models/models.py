import os
from clustering.utilities import load_model
from . KMeans import KMeansModel
from . KMedoids import KMedoidsModel
from . AAHC import  AAHCModel
from . PCA import PCAModel
from . ICA import ICAModel
from . DBScan import DBScanModel


def model_factory(name, method: str, path=None, n_maps=4, f_sampling=250):
    if path is not None:
        if os.path.exists(path):
            files = os.listdir(path)
            for file in files:
                _, extension = os.path.splitext(file)
                if extension == ".pickle":
                    path = os.path.join(path, file)
                    model = load_model(path)
                    return model
        raise FileNotFoundError("Model was not found")

    if method.lower().replace("-", "") == "kmeans":
        model = KMeansModel(name, method)
        return model
    elif method.lower().replace("-", "") == "kmedoids":
        model = KMedoidsModel(name, method)
        return model
    elif method.lower().replace("-", "") == "aahc":
        model = AAHCModel(name, method)
        return model
    elif method.lower().replace("-", "") == "pca":
        model = PCAModel(name, method)
        return model
    elif method.lower().replace("-", "") == "ica":
        model = ICAModel(name, method)
        return model
    elif method.lower().replace("-", "") == "dbscan":
        model = DBScanModel(name, method)
        return model
    else:
        raise NotImplementedError(f"Model {method} not found, only these models are available:\n"
              "['kmeans', 'kmedoids', 'aahc', 'pca', 'ica', 'dbscan']")