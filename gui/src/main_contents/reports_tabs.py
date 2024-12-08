from clustering.results.Results import load_results, Results
import flet as ft

class ResultsTab(ft.Tab):
    def __init__(self, results_path: str):
        super().__init__()

        self.results = load_results(results_path)
        self.text = f"{self.results.id}- {self.results.activity}"

        self.content = ft.Container(
            content=ft.Text("Works!")
        )
