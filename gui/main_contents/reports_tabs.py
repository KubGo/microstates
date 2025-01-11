from clustering.results.results import load_results, AbstractResults,  Results, ComparisonResults, ResultType
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from flet.plotly_chart import PlotlyChart
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px
import plotly.graph_objects as go
from .reporting_sections.transition_matrix_section import TransitionMatrixSection
from .reporting_sections.clustered_microstates_section import ClusteredMicrostatesSeciton, GroupsMicrostatesSection
from .reporting_sections.probabilities_section import ProbabilitiesSection, GroupProbabilitiesSection
from .reporting_sections.entropies_section import EntropiesSection, GroupsEntropiesSection
from .reporting_sections.statictical_test_results_section import StaticticalTestResultsSection

LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

class ResultsTabFactory:
    def __init__(self):
        pass

    def get_results_tab(self, results_path: str) -> ft.Tab:
        results = load_results(results_path)
        if results.type == ResultType.SINGLE_RESULT:
            return ResultsTab(results)
        if results.type == ResultType.COMPARISON_RESULTS:
            return ComparisonResultsTab(results)

class ResultsTab(ft.Tab):
    def __init__(self, results: AbstractResults):
        super().__init__()
        matplotlib.use("svg")
        self.results = results
        self.text = self.results.get_name()
        
        self.obtained_microstates = ClusteredMicrostatesSeciton(self.results)
        
        self.prob_pie_chart = ProbabilitiesSection(self.results)

        self.transition_matrix_section = TransitionMatrixSection(self.results)
        
        self.entropies_section = EntropiesSection(self.results)

        self.statistical_tests_results = StaticticalTestResultsSection(self.results)

        self.report_content = ft.Column(
            controls=[
                self.obtained_microstates,
                self.prob_pie_chart,
                self.transition_matrix_section,
                self.entropies_section,
                self.statistical_tests_results,
            ],
            scroll=True,
        )
        
        self.content = ft.Container(
            content=self.report_content,
        )

class ComparisonResultsTab(ft.Tab):
    def __init__(self, results: AbstractResults):
        super().__init__()
        matplotlib.use("svg")
        self.results = results
        self.text = self.results.get_name()
        
        self.obtained_microstates = GroupsMicrostatesSection(self.results)
        
        self.prob_pie_chart = GroupProbabilitiesSection(self.results)

        # self.transition_matrix_section = TransitionMatrixSection(self.results)
        
        self.entropies_section = GroupsEntropiesSection(self.results)

        # self.statistical_tests_results = StaticticalTestResultsSection(self.results)

        self.report_content = ft.Column(
            controls=[
                self.obtained_microstates,
                self.prob_pie_chart,
            #    self.transition_matrix_section,
                self.entropies_section,
            #    self.statistical_tests_results,
            ],
            scroll=True,
        )
        
        self.content = ft.Container(
            content=self.report_content,
        )

