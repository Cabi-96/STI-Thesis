#Interface
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import os
import logging

#Algo Integration
import pandas as pd

#variables
file_path = ""
logger = logging.getLogger(__name__)

class PageOne(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.label_frame_data = tk.LabelFrame(self, text="Excel Data",bg='white')
        self.label_frame_data.pack(fill="both",expand="yes")

        self.listFrame1 = list()
        self.listFrame2 = list()

        # Frame data : options
        self.Label_options = tk.LabelFrame(self, text="Options",bg='white')
        self.Label_options.pack(fill="both", pady=20, padx = 10, side='left')
        self.label_file = tk.Label(self.Label_options, text="No File Selected",bg='white')
        self.label_file.pack(pady = 20)

        # Frame data : Buttons
        self.button1 = tk.Button(self.Label_options, text="Browse A Folder", command=lambda: self.File_dialog())
        self.button1.pack(side='left', padx = 5)

        self.button2 = tk.Button(self.Label_options, text="Load Files", command=lambda: self.Load_excel_data())
        self.button2.pack(side='left', padx = 5)

        #if path is empty disable button LoadFiles
        if(file_path == ""):
            self.button2["state"] = "disable"


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

        for widgets in self.label_frame_data.winfo_children():
            widgets.destroy()

        i = 0
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            frameFile = tk.LabelFrame(self.label_frame_data, text=filename, bg='white')
            frameFile.pack(fill="both",expand="yes", pady = 10, padx = 10)

            global file_path
            file_path = self.label_file["text"]+"/"+filename

            if file_path.endswith(".csv"):
                try:
                    excel_filename = r"{}".format(file_path)
                    df = pd.read_csv(excel_filename)
                except ValueError:
                    tk.messagebox.showerror("Information", "The file you have chosen is invalid")
                    return None
                except FileNotFoundError:
                    tk.messagebox.showerror("Information", f"No such file as {file_path}")
                    return None
            else:
                tk.messagebox.showerror("Error", "This is not a CSV file")

            tvI = ttk.Treeview(frameFile)
            tvI.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

            treescrolly = tk.Scrollbar(frameFile, orient="vertical",
                                       command=tvI.yview)  # command means update the yaxis view of the widget
            treescrollx = tk.Scrollbar(frameFile, orient="horizontal",
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





