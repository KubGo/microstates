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

        self.vertical_alignment = ft.CrossAxisAlignment.START

        self.use_interpolation = ft.Checkbox(
            label="Interpolate signal between peaks",
            value=False,
        )
        
        self.analysis_strategy = ft.RadioGroup(
            ft.Column([
                ft.Text("Analysis to perform"),
                ft.Radio("Whole signal analysis",
                        value="whole_signal_analysis"),
                ft.Radio("Two groups signal analysis (common microstates)",
                        value="two_groups_common_microstates"),
                ft.Radio("Two groups signal analysis (separate microstates)",
                        value="two_groups_separate_microstates")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
            ),
            value="whole_signal_analysis",
        )

        self.controls = [
            self.clustering_alogorithm_selector,
            self.use_interpolation,
            self.analysis_strategy
        ]
