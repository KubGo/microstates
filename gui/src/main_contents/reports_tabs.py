from clustering.results.Results import load_results, Results
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from flet.plotly_chart import PlotlyChart
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px
import plotly.graph_objects as go
from .reporting_sections.transition_matrix_section import TransitionMatrixSection
from .reporting_sections.clustered_microstates_section import ClusteredMicrostatesSeciton
from .reporting_sections.probabilities_section import ProbabilitiesSection
from .reporting_sections.entropies_section import EntropiesSection

LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

class ResultsTab(ft.Tab):
    def __init__(self, results_path: str):
        super().__init__()
        matplotlib.use("svg")
        self.results = load_results(results_path)
        self.text = f"{self.results.id}- {self.results.activity}"
        
        self.obtained_microstates = ClusteredMicrostatesSeciton(self.results)
        
        self.prob_pie_chart = ProbabilitiesSection(self.results)

        self.transition_matrix_section = TransitionMatrixSection(self.results)
        
        self.entropies_section = EntropiesSection(self.results)

        self.report_content = ft.Column(
            controls=[
                self.obtained_microstates,
                self.prob_pie_chart,
                self.transition_matrix_section,
                self.entropies_section
            ],
            scroll=True,
        )
        
        self.content = ft.Container(
            content=self.report_content,
        )



