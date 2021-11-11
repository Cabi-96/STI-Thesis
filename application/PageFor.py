#Interface
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import tkinterweb


import pandas as pd

from application.utils.utils import printDf, executeSparqlQuery, insertDataDf


class PageFor(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        frame = tkinterweb.HtmlFrame(self)
        frame.load_website("https://www.google.com/")
        frame.pack(fill="both", expand=True)



    def show(self):
        self.lift()