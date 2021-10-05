#Interface
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import os
import PageOneTest


#bool URI loaded
uriLoad = False
listDf = list()
listDictDf = list()
cta = list()
increment = 1


#variables
isDebug = 0
file_path_absolute = os.path.dirname(__file__)
file_path_debug = os.path.join(file_path_absolute, ".idea\\files\\case_test")
listFrame1 = list()
listFrame2 = list()
file_path = ""


def main():
    root = Tk()
    root.title("Tk")
    root.geometry('370x340')
    app = PageOneTest.PageOneTest(root, file_path)
    app.pack(expand=True, fill=BOTH)
    root.mainloop()

main()