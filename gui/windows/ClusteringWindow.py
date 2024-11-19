from gui.windows.AbstractWindow import AbstractWindow
from customtkinter import filedialog
from pathlib import Path
import customtkinter

class ClusteringWindow(AbstractWindow):
    
    def __init__(self, master, language):
        super(AbstractWindow, self).__init__(master)
        # Paths for files to cluster
        self.file_paths = None
        self.data_options()
        self.clustering_options()
        self.init()
        
    def init(self):
        self.clustering_info = customtkinter.CTkLabel(self, text="Clustering window data add and adjustments", anchor='center')
        self.clustering_info.grid(row=0, column=0, columnspan=4)
        
        
        
    def data_options(self):
        self.data_options_frame = customtkinter.CTkFrame(self)
        # Data selection
        self.data_options_frame.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="NEWS")
        self.chose_file_dialog = customtkinter.CTkButton(self.data_options_frame, command=self.openFile)
        self.chose_file_dialog.grid(row=0, column=0, padx=20, pady=10)     
        # Frequency of signal
        self.frequency_label = customtkinter.CTkLabel(self.data_options_frame, text="Signal frequency [Hz]", anchor='center')
        self.frequency_label.grid(row=0, column=1, pady=(10, 5), padx=20)
        self.signal_frequency = customtkinter.CTkEntry(self.data_options_frame, placeholder_text="250")
        self.signal_frequency.grid(row=0, column=2, padx=20, pady=(10, 5))
        # Dirty signal at the begining
        self.start_remove_time_label = customtkinter.CTkLabel(self.data_options_frame, text="Time to remove from start")
        self.start_remove_time_label.grid(row=1, column=0, padx=20, pady=(10, 5))
        self.start_remove_time_entry = customtkinter.CTkEntry(self.data_options_frame, placeholder_text="0")
        self.start_remove_time_entry.grid(row=1, column=1, padx=(5,20), pady=(10, 5))
        # Dirty signal at the end
        self.end_remove_time_label = customtkinter.CTkLabel(self.data_options_frame, text="Time to remove from end")
        self.end_remove_time_label.grid(row=2 , column=0, padx=20, pady=(5, 20))
        self.end_remove_time_entry = customtkinter.CTkEntry(self.data_options_frame, placeholder_text="0")
        self.end_remove_time_entry.grid(row=2, column= 1, padx=(5, 20), pady=(5, 20))
        # Separator and id, activity indexes
        self.separator_label = customtkinter.CTkLabel(self.data_options_frame, text="Separator:")
        self.separator_label.grid(row=1, column=2, pady=(10, 5), padx=20)
        self.separator_entry = customtkinter.CTkEntry(self.data_options_frame, placeholder_text="_")
        self.separator_entry.grid(row=2, column=2, pady=(5, 20), padx=20)
        # Identifier
        self.identifier_label = customtkinter.CTkLabel(self.data_options_frame, text="Identifier index")
        self.identifier_label.grid(row=1, column=3, pady=10, padx=(20, 5))
        self.identifier_entry = customtkinter.CTkEntry(self.data_options_frame, placeholder_text="1")
        self.identifier_entry.grid(row=1, column=4, pady=10, padx=(5, 20))
        # Activity
        self.activity_label = customtkinter.CTkLabel(self.data_options_frame, text="Activity index:")
        self.activity_label.grid(row=2, column=3, pady=10, padx=(20, 5))
        self.activity_entry = customtkinter.CTkEntry(self.data_options_frame, placeholder_text="2")
        self.activity_entry.grid(row=2, column=4, pady=10, padx=(5, 20))
        
    def clustering_options(self):
        self.clustering_options_frame = customtkinter.CTkFrame(self)
        self.clustering_options_frame.grid(row=2, column=0, rowspan=3, columnspan=4, padx=20, pady=20, sticky="news")
        # Clustering algorithm
        self.clustering_algorithm_label = customtkinter.CTkLabel(self.clustering_options_frame, text="Algorithm:")
        self.clustering_algorithm_label.grid(row=0, column=0, pady=(10,0), padx=20)
        self.clustering_algorithm_chose = customtkinter.CTkOptionMenu(
            self.clustering_options_frame,
            width=150,
            values=[
                "K-means",
                "AAHC",
                "K-medoids",
                "PCA",
                "ICA"
            ]
        )
        self.clustering_algorithm_chose.grid(row=1, column=0, pady=10, padx=20)
        self.clustering_algorithm_chose.set("K-means")
        # Other functionalities (blank columns for now)
        self.clustering_options_frame.grid_columnconfigure(2, weight=1)
        # Clustering button
        self.clustering_btn = customtkinter.CTkButton(self.clustering_options_frame, text="Cluster")
        self.clustering_btn.grid(row=0, column=4, rowspan=2, padx=20, pady=10, sticky="e")
    
    def refresh_text(self, language):
        pass
    
    def show(self):
        self.grid(row=0, column=1, rowspan=3, columnspan=3, padx=(20, 20), pady=(20,20), sticky="nsew")
    
    def hide(self):
        self.grid_forget()
        
    def openFile(self):
        filepaths = filedialog.askopenfiles(
            title="Chose EEG electrodes data",
            filetypes=[('csv files', "*.csv")]
        )
        self.file_paths = [filepath.name for filepath in filepaths]
