from . interfaces import AbstractSection
import flet as ft

class ClusteringSettingsSection(AbstractSection):
    
    def __init__(self, content_page):
        super().__init__(content_page)
    
        self.clustering_alogorithm_selector = ft.Dropdown(
            label="Clustering algorithm",
            options=[
                ft.dropdown.Option("K-means"),
                ft.dropdown.Option("K-medoids"),
                ft.dropdown.Option("PCA"),
                ft.dropdown.Option("ICA"),
                ft.dropdown.Option("AAHC")
            ],
            value="K-means"
        )

        self.use_interpolation = ft.Checkbox(
            label="Interpolate signal between peaks",
            value=False
        )

        self.controls = [
            self.clustering_alogorithm_selector,
            self.use_interpolation
        ]
