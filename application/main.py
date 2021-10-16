#Interface
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import os
from PageOne import PageOne
from PageTwo import PageTwo
from PageThree import PageThree


#variables
isDebug = 0
file_path_absolute = os.path.dirname(__file__)
file_path_debug = os.path.join(file_path_absolute, ".idea\\files\\case_test")

# TODO : désactiver le bouton next page si uri chargées
isLoadedURI = False

class Container(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)




        #page 1
        p1 = PageOne(self, bg='white')

        p1.button3 = tk.Button(p1.Label_options, text="Load URI", state="disable", command=lambda:p2.load_uri(p1))
        p1.button3.pack(side='left', padx = 5)

        p1.button5 = tk.Button(p1.Label_options, text='Next Page', command=lambda:p2.show())
        p1.button5.pack(side='left', padx = 5)

        #page 2
        p2 = PageTwo(self, bg='white')
        p2.button4 =  tk.Button(p2.label_frame_selection, text='Previous page', command=lambda:p1.show())
        p2.button5 =  tk.Button(p2.label_frame_selection, text='Next page', command=lambda:p3.show())
        p2.button4.pack(side='bottom', padx = 5)
        p2.button5.pack(side='bottom', padx = 5)


        #button terminer pour aller page 3
        p2.button_Q3_SelectProposition = tk.Button(p2.frame_questions, text='Terminer', command=lambda:p3.show_df_result(p2.df))
        p2.button_Q3_SelectProposition.pack(side='bottom', padx = 5)


        #page 3
        p3 = PageThree(self, bg='white')
        p3.button4 =  tk.Button(p3, text='Previous page', command=lambda:p2.show())
        p3.button4.pack()


        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p1.show()





if __name__ == "__main__":
    root = tk.Tk()
    root.title("Semantic Table Intepreter")

    # menu tutorial https://www.delftstack.com/fr/tutorial/tkinter-tutorial/tkinter-menubar/
    main = Container(root)
    main.pack(side="top", fill="both", expand=True)

    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar)
    filemenu.add_command(label="Open")
    filemenu.add_command(label="Save")
    filemenu.add_command(label="Exit")
    menubar.add_cascade(label="File", menu=filemenu)

    root.config(menu=menubar)

    root.wm_geometry("800x600")
    root.mainloop()