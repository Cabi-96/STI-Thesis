#Interface
import pathlib
import threading
import tkinter as tk
import time
from tkinter import *
from tkinter.ttk import Progressbar
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


    def __init__(self, root):
        tk.Frame.__init__(self, root)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        #page 1
        self.p1 = PageOne(self, bg='white')

        self.p1.button3 = tk.Button(self.p1.Label_options, text="Load URI", state="disable", command=lambda:self.load_uri())#, command=lambda:self.p2.load_uri(self.p1))
        self.p1.button3.pack(side='left', padx = 5)

        self.p1.button5 = tk.Button(self.p1.Label_options, text='Next Page', command=lambda:self.p2.show())
        self.p1.button5.pack(side='left', padx = 5)

        #page 2
        self.p2 = PageTwo(self, bg='white')
        self.p2.button4 =  tk.Button(self.p2.label_frame_selection, text='Previous page', command=lambda:self.p1.show())
        self.p2.button5 =  tk.Button(self.p2.label_frame_selection, text='Next page', command=lambda:self.p3.show())
        self.p2.button4.pack(side='bottom', padx = 5)
        self.p2.button5.pack(side='bottom', padx = 5)


        #button terminer pour aller page 3
        self.p2.button_Q3_SelectProposition = tk.Button(self.p2.label_frame_selection, text='Terminer', command=lambda:[self.p3.show_df_result(self.p2.df),self.p2.refreshTvResult(self.p2.isNbFilesSup)])
        self.p2.button_Q3_SelectProposition.pack(side='bottom', padx = 5)


        #page 3
        self.p3 = PageThree(self, bg='white')
        self.p3.button4 =  tk.Button(self.p3, text='Previous page', command=lambda:self.p2.show())
        self.p3.button4.pack()

        #progress bar
        self.pframe = Frame(self)
        self.progress = Progressbar(self.pframe, orient=HORIZONTAL,length=500,  mode='indeterminate')
        self.progress.place(in_=self.pframe, anchor="c", relx=.5, rely=.5)



        self.p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.pframe.place(in_=container, x=0, y=0, relwidth=1, relheight=1)



        root.config(menu=self.create_menubar())


        self.p1.show()


    def load_uri(self):
        def launchProgressBar():
            self.pframe.lift()
            self.progress.start()
            self.p2.load_uri(self.p1)

            self.progress.stop()

        threading.Thread(target=launchProgressBar).start()

        #self.p2.load_uri(self.p1)



    def create_menubar(self):
        menubar = tk.Menu(self)

        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Help")
        menu_file.add_command(label="Exit",command=root.destroy)

        menu_navigate = tk.Menu(menubar, tearoff=0)
        menu_navigate.add_command(label="Next page")
        menu_navigate.add_command(label="Previous page")

        # TODO : close firefox quand on exit


        menubar.add_cascade(label="File", menu=menu_file)
        menubar.add_cascade(label="Navigate", menu=menu_navigate)

        return menubar







if __name__ == "__main__":
    root = tk.Tk()
    root.title("TabIntegration")
    # Icon from : https://icons8.com/icon/set/data/material-rounded
    #iconPath = str(pathlib.Path().absolute())+'\Icon\LogoApp.png'
    iconPath = os.path.abspath(os.curdir) + "\\application\\Icon\\LogoApp.png"
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=iconPath))

    #root.iconbitmap('C:/Users/ANTHONY/Downloads/icons8-doughnut-chart-24.ico')

    # menu tutorial https://www.delftstack.com/fr/tutorial/tkinter-tutorial/tkinter-menubar/
    main = Container(root)
    main.pack(side="top", fill="both", expand=True)



    root.wm_geometry("800x600")
    root.mainloop()