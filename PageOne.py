#Interface
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import pandas as pd
import os

#Algo Integration
from requests.exceptions import MissingSchema, HTTPError
from tabulate import tabulate
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import pathlib
import requests

from MtabExtractTable import MtabAnnotationApi

# initalise the tkinter GUI
root = tk.Tk()

root.geometry("1720x960")  # set the root dimensions
root.pack_propagate(False)  # tells the root to not let the widgets inside it determine its size.
root.resizable(0, 0)  # makes the root window fixed in size.

f1 = Frame(root,width=1720, height=960)
f2 = Frame(root,width=1720, height=960)

listFrame1 = list()
listFrame2 = list()
file_path = ""


for frame in (f1, f2):
    frame.grid(row=0, column=0, sticky='news')
    frame.pack_propagate(0)


# Frame for TreeView
frame1 = tk.LabelFrame(f1, text="Excel Data")
frame1.place(height=250, width=500)

frame2 = tk.LabelFrame(f2, text="Excel Data")
frame2.place(height=250, width=500)

# Frame for open file dialog
file_frame = tk.LabelFrame(f1, text="Options")
file_frame.place(height=100, width=400, rely=0.89, relx=0)

file_frame2 = tk.LabelFrame(f2, text="Options")
file_frame2.place(height=100, width=400, rely=0.89, relx=0)

# Buttons
button1 = tk.Button(file_frame, text="Browse A Folder", command=lambda: File_dialog())
button1.place(rely=0.65, relx=0.10)

button2 = tk.Button(file_frame, text="Load Files", command=lambda: Load_excel_data())
button2.place(rely=0.65, relx=0.40)

def load_uri(frame):
    # Create the dataFrames
    print(label_file["text"])
    api = MtabAnnotationApi(label_file["text"])
    api.extractTableHTML()

    cea = api.getList_CEA_Global()
    print("CEA")
    print(cea)

    cpa = api.getList_CPA_Global()
    print("CPA")
    print(cpa)

    cta = api.getList_CTA_Global()
    print("CTA")
    # Pour chaque CTA, le premier index est nul. Je l'ai enlevé dans le for juste en dessous.
    print(cta)

    numberOfDf = len(cpa)
    listDf = list()
    listDictDf = list()

    global listFrame2
    for frame in listFrame2:
        frame.destroy()
    listFrame2 = list()
    #Compter
    rely = -0.30
    relx = 0.0
    #file_path = label_file["text"]
    i = 0
    for i in range(0, numberOfDf, 1):
        df = pd.DataFrame(data=cea[i],
                          columns=cpa[i],
                          dtype=str)
        #Supprime la premiere ligne du fichier en ajustant les indexes
        df = df.reindex(df.index.drop(0)).reset_index(drop=True)
        cta[i].pop(0)
        listCol = df.columns.values.tolist()
        #Supprime les colonnes qui n'ont pas été trouvées par Mtab
        if "" in listCol:
            df.drop(labels=[""], axis=1, inplace=True)
        #Supprime les colonnes dupliquées
        df = df.loc[:, ~df.columns.duplicated()]
        #Affiche le tableau
        print(tabulate(df, headers='keys', tablefmt='psql'))
        listDf.append(df)
        j = 0
        dictDf = dict()
        for j in range(0, len(cpa[i]), 1):
            dictDf[tuple(cta[i][j])] = cpa[i][j]
        listDictDf.append(dictDf)

        ##--------------------------------------------Afficher dataFrames-------------------------------------------------------------------------
        listFrame2.append(tk.LabelFrame(f2, text='df'))
        if i % 3 != 0 or i == 0:
            rely = rely + 0.30
            listFrame2[i].place(height=250, width=500, rely=rely, relx=relx)
        else:
            relx = relx + 0.30
            rely = 0.0
            listFrame2[i].place(height=250, width=500, rely=rely, relx=relx)

        tvI = ttk.Treeview(listFrame2[i])
        tvI.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(listFrame2[i], orient="vertical",
                                   command=tvI.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(listFrame2[i], orient="horizontal",
                                   command=tvI.xview)  # command means update the xaxis view of the widget
        tvI.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget
        tvI["column"] = list(df.columns)
        tvI["show"] = "headings"

        for column in tvI["columns"]:
            tvI.heading(column, text=column)  # let the column heading = column name
            df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
            for row in df_rows:
                tvI.insert("", "end",
                           values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    frame.tkraise()

button3 = tk.Button(file_frame, text="Load URI", command=lambda: load_uri(f2))
button3.place(rely=0.65, relx=0.60)

#Boutton pour revenir a la page précédente.
button4 = tk.Button(file_frame2, text='Previous page', command=lambda:raise_frame(f1))
button4.place(rely=0.65, relx=0.40)

button5 = tk.Button(file_frame, text='Next Page', command=lambda:raise_frame(f2))
button5.place(rely=0.65, relx=0.80)


# The file/file path text
label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)

def File_dialog():
    """This Function will open the file explorer and assign the chosen file path to label_file"""
    """filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))"""
    krepertoire = filedialog.askdirectory(title="Sélectionnez un répertoire de destination ...", mustexist=True)
    label_file["text"] = krepertoire
    return None


def insert_treeview():
    frame2 = tk.LabelFrame(f1, text="Excel Data")
    frame2.place(height=100, width=100)


def Load_excel_data():
    """If the file selected is valid this will load the file into the Treeview"""

    directory = os.fsencode(label_file["text"])
    #Changer l'init ici il faut transformer listFrame en variable globale.
    global listFrame1
    for frame in listFrame1:
        frame.destroy()
    listFrame1 = list()
    #Compter
    rely = -0.30
    relx = 0.0
    #file_path = label_file["text"]
    i = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        listFrame1.append(tk.LabelFrame(f1, text=filename))
        if i % 3 != 0 or i == 0:
            rely = rely + 0.30
            listFrame1[i].place(height=250, width=500, rely=rely, relx=relx)
        else:
            relx = relx + 0.30
            rely = 0.0
            listFrame1[i].place(height=250, width=500, rely=rely, relx=relx)

        global file_path
        file_path = label_file["text"]+"/"+filename

        if file_path.endswith(".csv"):
            try:
                excel_filename = r"{}".format(file_path)
                if excel_filename[-4:] == ".csv":
                    df = pd.read_csv(excel_filename)
                else:
                    df = pd.read_excel(excel_filename)

            except ValueError:
                tk.messagebox.showerror("Information", "The file you have chosen is invalid")
                return None
            except FileNotFoundError:
                tk.messagebox.showerror("Information", f"No such file as {file_path}")
                return None


        tvI = ttk.Treeview(listFrame1[i])
        tvI.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(listFrame1[i], orient="vertical",
                                   command=tvI.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(listFrame1[i], orient="horizontal",
                                   command=tvI.xview)  # command means update the xaxis view of the widget
        tvI.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget
        tvI["column"] = list(df.columns)
        tvI["show"] = "headings"

        for column in tvI["columns"]:
            tvI.heading(column, text=column)  # let the column heading = column name
            df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
            for row in df_rows:
                tvI.insert("", "end",
                           values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        i = i +1
    return None


def raise_frame(frame):
    frame.tkraise()

raise_frame(f1)
root.mainloop()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Integration Algo
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





