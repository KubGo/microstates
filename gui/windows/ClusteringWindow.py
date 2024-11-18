from gui.windows.AbstractWindow import AbstractWindow
from customtkinter import filedialog
from pathlib import Path
import customtkinter

class ClusteringWindow(AbstractWindow):
    
    def __init__(self, master, language):
        super(AbstractWindow, self).__init__(master)
        # Paths for files to cluster
        self.file_paths = None
        self.init()
        
    def init(self):
        self.clustering_info = customtkinter.CTkLabel(self, text="Clustering window")
        self.clustering_info.grid(row=0, column=0, columnspan=3)
        self.chose_file_dialog = customtkinter.CTkButton(self, command=self.openFile)
        self.chose_file_dialog.grid(row=1, column=0, padx=20, pady=10)
        self.clustering_algorithm_chose = customtkinter.CTkOptionMenu(
            self,
            width=150,
            values=[
                "K-means",
                "AAHC",
                "K-medoids",
                "PCA",
                "ICA"
            ]
        )
        self.clustering_algorithm_chose.grid(row=4, column=0, pady=10, padx=20)
    
    def refresh_text(self, language):
        pass
    
    def show(self):
        self.grid(row=0, column=1, padx=(20, 20), pady=(20,20), sticky="nsew")
    
    def hide(self):
        self.grid_forget()
        
    def openFile(self):
        filepaths = filedialog.askopenfiles(
            title="Chose EEG electrodes data",
            filetypes=[('csv files', "*.csv")]
        )
        self.file_paths = [filepath.name for filepath in filepaths]
