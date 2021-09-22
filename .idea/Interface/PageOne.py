import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

import pandas as pd
import os

# initalise the tkinter GUI
root = tk.Tk()

root.geometry("1720x960")  # set the root dimensions
root.pack_propagate(False)  # tells the root to not let the widgets inside it determine its size.
root.resizable(0, 0)  # makes the root window fixed in size.

# Frame for TreeView
frame1 = tk.LabelFrame(root, text="Excel Data")
frame1.place(height=250, width=500)

# Frame for open file dialog
file_frame = tk.LabelFrame(root, text="Open File")
file_frame.place(height=100, width=400, rely=0.89, relx=0)

# Buttons
button1 = tk.Button(file_frame, text="Browse A File", command=lambda: File_dialog())
button1.place(rely=0.65, relx=0.50)

button2 = tk.Button(file_frame, text="Load File", command=lambda: Load_excel_data())
button2.place(rely=0.65, relx=0.30)

button3 = tk.Button(file_frame, text="Next Page", command=lambda: nextPage())
button3.place(rely=0.65, relx=0.80)

# The file/file path text
label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)

## Treeview Widget
""""
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

treescrolly = tk.Scrollbar(frame1, orient="vertical",
                           command=tv1.yview)  # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(frame1, orient="horizontal",
                           command=tv1.xview)  # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set,
              yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget
"""

def File_dialog():
    """This Function will open the file explorer and assign the chosen file path to label_file"""
    """filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))"""
    krepertoire = filedialog.askdirectory(title="Sélectionnez un répertoire de destination ...", mustexist=True)
    label_file["text"] = krepertoire
    return None


def insert_treeview():
    frame2 = tk.LabelFrame(root, text="Excel Data")
    frame2.place(height=100, width=100)


def Load_excel_data():
    """If the file selected is valid this will load the file into the Treeview"""

    directory = os.fsencode(label_file["text"])
    listFrame = list()
    #Compter
    rely = -0.30
    relx = 0.0
    #file_path = label_file["text"]
    i = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        frame = tk.LabelFrame(root, text=filename)
        print(filename)
        if i % 3 != 0 or i == 0:
            print("if")
            print(i)
            rely = rely + 0.30
            frame.place(height=250, width=500,rely=rely, relx=relx)
        else:
            print("else")
            print(i)
            relx = relx + 0.30
            rely = 0.0
            frame.place(height=250, width=500,rely=rely, relx=relx)
        listFrame.append(frame)


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

        #clear_data() il va falloir clear tous les tableaux

        tvI = ttk.Treeview(listFrame[i])
        tvI.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(listFrame[i], orient="vertical",
                                   command=tvI.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(listFrame[i], orient="horizontal",
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

#Pensez à l'utiliser
def clear_data():
    tv1.delete(*tv1.get_children())
    return None

def nextPage():
    root.destroy()
    import PageTwo





root.mainloop()
