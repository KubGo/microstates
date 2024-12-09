import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from .interfaces import AbstractReportingSection
import seaborn as sn
import matplotlib.pyplot as plt

LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

class TransitionMatrixSection(AbstractReportingSection):

    def __init__(self, results):
        super().__init__(results)
        self.transition_matrix = self.results.transition_matrix
        microstates_labels = LABELS[:len(self.transition_matrix[0])]
        hm = sn.heatmap(self.transition_matrix,
                        annot=True,
                        cmap="coolwarm",
                        xticklabels=microstates_labels,
                        yticklabels=microstates_labels)
        
        fig = hm.get_figure()
        
        self.controls = [
            MatplotlibChart(hm.get_figure(), expand=True, isolated=True)
        ]
        plt.close('all')


