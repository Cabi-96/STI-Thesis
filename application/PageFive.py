#Interface
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk


import pandas as pd

from application.utils.utils import printDf, executeSparqlQuery, insertDataDf


class PageFive(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)




    def show(self):
        self.lift()