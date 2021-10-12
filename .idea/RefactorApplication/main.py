#Interface
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import os
from PageOneTest import PageOneTest
from PageTwoTest import PageTwoTest
from PageThreeTest import PageThreeTest


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


class Container(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)


        #page 1
        p1 = PageOneTest(self)

        p1.button3 = tk.Button(p1.Label_options, text="Load URI", state="disable", command=lambda:p2.load_uri(p1))
        p1.button3.pack(side='left', padx = 5)

        p1.button5 = tk.Button(p1.Label_options, text='Next Page', command=lambda:p2.show())
        p1.button5.pack(side='left', padx = 5)

        #page 2
        p2 = PageTwoTest(self)
        p2.button4 =  tk.Button(p2, text='Previous page', command=lambda:p1.show())
        p2.button4.pack(side='bottom', padx = 5)


        #button terminer pour aller page 3
        p2.button_Q3_SelectProposition = tk.Button(p2.frame_questions, text='Terminer', command=lambda:p3.show_df_result(df,tvResult))
        p2.button_Q3_SelectProposition.pack()


        #page 3
        p3 = PageThreeTest(self)


        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p1.show()





if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tk")
    root.geometry('370x340')

    main = Container(root)
    main.pack(side="top", fill="both", expand=True)

    root.wm_geometry("400x400")
    root.mainloop()