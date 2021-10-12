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


#variables
isDebug = 0
file_path_absolute = os.path.dirname(__file__)
file_path_debug = os.path.join(file_path_absolute, ".idea\\files\\case_test")
listFrame1 = list()
listFrame2 = list()
file_path = ""

class PageOneTest(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.label_frame_data = tk.LabelFrame(self, text="Excel Data")
        self.label_frame_data.pack(fill="both",expand="yes")

        # Frame data : options
        self.Label_options = tk.LabelFrame(self, text="Options")
        self.Label_options.pack(fill="both", pady=20, padx = 10, side='left')
        self.label_file = tk.Label(self.Label_options, text="No File Selected")
        self.label_file.pack(pady = 20)

        # Frame data : Buttons
        self.button1 = tk.Button(self.Label_options, text="Browse A Folder", command=lambda: self.File_dialog())
        self.button1.pack(side='left', padx = 5)

        self.button2 = tk.Button(self.Label_options, text="Load Files", command=lambda: self.Load_excel_data())
        self.button2.pack(side='left', padx = 5)

        #if path is empty disable button LoadFiles
        if(file_path == ""):
            self.button2["state"] = "disable"

        self.button3 = tk.Button(self.Label_options, text="Load URI", state="disable", command=lambda: self.load_uri(frame_pageTwo))
        self.button3.pack(side='left', padx = 5)

        self.button5 = tk.Button(self.Label_options, text='Next Page', command=lambda:self.raise_frame(frame_pageTwo))
        self.button5.pack(side='left', padx = 5)

    def show(self):
        self.lift()


    def File_dialog(self):
        """This Function will open the file explorer and assign the chosen file path to label_file"""
        """filename = filedialog.askopenfilename(initialdir="/",
                                                  title="Select A File",
                                                  filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))"""
        krepertoire = filedialog.askdirectory(title="Sélectionnez un répertoire de destination ...", mustexist=True)
        self.label_file["text"] = krepertoire

        #active buttons loadUri and loadFiles
        self.button2["state"] = "normal"
        self.button3["state"] = "normal"

        return None

    def Load_excel_data(self):
        """If the file selected is valid this will load the file into the Treeview"""
        directory = os.fsencode(self.label_file["text"])
        #Changer l'init ici il faut transformer listFrame en variable globale.
        #global listFrame1
        #for frame in listFrame1:
        #    frame.destroy()
        listFrame1 = list()

        i = 0
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            listFrame1.append(tk.LabelFrame(self.label_frame_data, text=filename))
            listFrame1[i].pack(fill="both",expand="yes", pady = 10, padx = 10)

            global file_path
            file_path = self.label_file["text"]+"/"+filename

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

            #columns
            for column in tvI["columns"]:
                tvI.heading(column, text=column)  # let the column heading = column name

            #rows
            df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
            for row in df_rows:
                tvI.insert("", "end", values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
            i = i +1

        return None


    def load_uri(frame):
        # Create the dataFrames
        #print(label_file["text"])
        api = MtabAnnotationApi(label_file["text"])
        api.extractTableHTML()

        cea = api.getList_CEA_Global()
        #print("CEA")
        #print(cea)

        cpa = api.getList_CPA_Global()
        #print("CPA")
        #print(cpa)

        global cta
        cta = api.getList_CTA_Global()
        #print("CTA")
        # Pour chaque CTA, le premier index est nul. Je l'ai enlevé dans le for juste en dessous.
        #print(cta)

        numberOfDf = len(cpa)
        global listDf
        listDf = list()
        global listDictDf
        listDictDf = list()

        global listFrame2
        for frame in listFrame2:
            frame.destroy()
        listFrame2 = list()

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
            #print(tabulate(df, headers='keys', tablefmt='psql'))
            listDf.append(df)
            j = 0
            dictDf = dict()
            for j in range(0, len(cpa[i]), 1):
                dictDf[tuple(cta[i][j])] = cpa[i][j]
            listDictDf.append(dictDf)

            ##--------------------------------------------Afficher dataFrames-------------------------------------------------------------------------
            listFrame2.append(tk.LabelFrame(label_frame_data2, text='df'))
            listFrame2[i].pack(fill="both",expand="yes", pady = 10, padx = 10)


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
        global uriLoad
        uriLoad = True
        #frame.tkraise()



