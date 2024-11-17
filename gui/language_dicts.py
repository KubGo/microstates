from gui.windows import AbstractWindow

pl = {
    "appearance mode": "Wygląd:",
    "language": "Język:",
    "home_screen_text": 
        """
        Witaj,
        Aplikacja Microstates została stworzona do klasteryzacji i analizy mikrostanów.
        W menu po lewej stronie możesz wybrać jedną z zakładek w celu rozpoczęcia.
        """,
    "clustering_btn": "Klasteryzacja",
    "reports_btn": "Raporty",
    
}

en = {
    "appearance mode": "Appearance Mode:",
    "language": "Language:",
    "home_screen_text": 
        """
        Welcome,
        Microstates app was created for clustering and analyzing of microstates.
        In the menu on the left side You can chose one of tabs to begin.
        """,
    "clustering_btn": "Clustering",
    "reports_btn": "Reports",
    
}

class LanguageHandler():
    
    def __init__(self):
        self.windows = []
    
    def register(self, window: AbstractWindow):
        self.windows.append(window)

    def unregister(self, window: AbstractWindow):
        self.windows.remove(window)
        
    def refresh_text(self, language: dict):
        for window in self.windows:
            window.refresh_text(language)
