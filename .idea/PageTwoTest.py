#Interface
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import os

#Algo Integration
from requests.exceptions import MissingSchema, HTTPError
from tabulate import tabulate
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
from MtabExtractTable import MtabAnnotationApi



class PageTwoTest(Frame):

    def __init__(self, root, file_path):
        ######Frame pagetwo  : two container one for result (frame_data2 and one for questions and choices frame_selection)
        Frame.__init__(self, root)

        ## two frames
        self.label_frame_data2 = tk.LabelFrame(frame_pageTwo, text="Excel Data")
        self.label_frame_data2.pack(side="left", padx=2, pady=2,fill="both", expand="yes")
        self.label_frame_selection = tk.LabelFrame(frame_pageTwo, text="Selection", width = "400")
        self.label_frame_selection.pack(side="left", padx=2, pady=2, fill="y")

        self.frame_questions = tk.LabelFrame(label_frame_selection, text="Questions")
        self.frame_questions.pack(expand="no", fill="x",padx = 5)

        #Boutton pour revenir a la page précédente.
        self.button4 = tk.Button(frame_pageTwo, text='Previous page', command=lambda:raise_frame(frame_pageOne))
        self.button4.pack(side='bottom', padx = 5)

        ##### Frame question 3 (third page)
        self.frame_pageThree = Frame(root)
        self.frame_pageThree.pack(fill="both", expand="yes")
