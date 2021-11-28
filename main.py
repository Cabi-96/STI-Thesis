import threading
import tkinter as tk
import webbrowser
import logging
import logging.config
from datetime import datetime

from tkinter import *
from tkinter.ttk import Progressbar

import os
from application.PageOne import PageOne
from application.PageTwo import PageTwo
from application.PageThree import PageThree
import pathlib

from http.server import HTTPServer, CGIHTTPRequestHandler

#### variables
from application.PageFive import PageFive
from application.PageFor import PageFor

#### set variables
isDebug = 0
file_path_absolute = os.path.dirname(__file__)
file_path_debug = os.path.join(file_path_absolute, ".idea\\files\\case_test")
PORT = 7410



class Container(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.displayed_page = -1

        #page 1
        self.p1 = PageOne(self, bg='white')
        self.p1.button3 = tk.Button(self.p1.Label_options, text="Load URI", state="disable", command=lambda:self.load_uri())
        self.p1.button3.pack(side='left', padx = 5)

        #page 2
        self.p2 = PageTwo(self, bg='white')

        #button terminer pour aller page 3
        #self.p2.button_Q3_SelectProposition = tk.Button(self.p2.label_frame_selection, text='Finish', command=lambda:[self.p3.show_df_result(self.p2.df),self.p2.refreshTvResult(self.p2.isNbFilesSup)])
        self.p2.button_Q3_SelectProposition = tk.Button(self.p2.label_frame_selection, text='Finish', state="disable", command=lambda:self.load_finish())

        self.p2.button_Q3_SelectProposition.pack(side='bottom', padx = 5)

        #page 3
        self.p3 = PageThree(self, bg='white')
        self.p3.button_Q3_SelectProposition = tk.Button(self.p3, text='Core attribute to Uri', command=lambda:self.p3.transformCoreToUri(self.p2.getCta()))
        self.p3.button_Q3_SelectProposition.pack(side='bottom', padx = 5)
        #page 3
        self.p4 = PageFor(self, bg='white')

        #page 3
        self.p5 = PageFive(self, bg='white')

        #progress bar
        self.pframe = Frame(self)
        self.progress = Progressbar(self.pframe, orient=HORIZONTAL,length=500,  mode='indeterminate')
        self.progress.place(in_=self.pframe, anchor="c", relx=.5, rely=.5)


        self.p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.pframe.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        root.config(menu=self.create_menubar())

        self.p1.show()
        self.displayed_page = 1


    def show_help(self):
        #pathBase = str(pathlib.Path(__file__).parent.resolve())
        #strip_character = "\\"

        pathBase = str(pathlib.Path(__file__).parent.resolve())

        ROOT_DIR =pathBase+'\\readme.md'

        os.startfile(ROOT_DIR)


    def show_nextpage(self):
        if self.displayed_page == 1:
            #print(self.displayed_page)
            self.p2.show()
            self.displayed_page = 2

        elif self.displayed_page == 2:
            self.p3.show()
            self.displayed_page = 3

        elif self.displayed_page == 3:
            self.p1.show()
            self.displayed_page = 1

        #On retourne d'office à la page 1
        elif self.displayed_page == 4:
            self.p1.show()
            self.displayed_page = 1

        elif self.displayed_page == 5:
            self.p1.show()
            self.displayed_page = 1


    def show_previouspage(self):
        if self.displayed_page == 2:
            self.p1.show()
            self.displayed_page = 1

        elif self.displayed_page == 3:
            self.p2.show()
            self.displayed_page = 2
        #On retourne d'office à la page 1
        elif self.displayed_page == 4:
            self.p1.show()
            self.displayed_page = 1

        elif self.displayed_page == 5:
            self.p1.show()
            self.displayed_page = 1


    def show_pageFor(self):
        #pathBase = str(pathlib.Path(__file__).parent.resolve())
        #ROOT_DIR =pathBase+'\\graph-annotation.html'
        #print(ROOT_DIR)
        #self.p4.show()
        #self.displayed_page = 4
        current_directory = os.getcwd().split(os.sep)[-1]
        #webbrowser.open_new_tab("http://localhost:"+ str(PORT) + "/"+ current_directory + "/graph-annotation.html")
        webbrowser.open_new_tab("http://localhost:"+ str(PORT) + "/graph-annotation.html")


    def show_pageFive(self):
        self.p5.show()
        self.displayed_page = 5



    def load_uri(self):
        def launchProgressBar():
            self.pframe.lift()
            self.progress.start()
            self.p2.load_uri(self.p1)
            self.progress.stop()
            self.displayed_page = 2

        threading.Thread(target=launchProgressBar).start()

    def load_finish(self):
        def launchProgressBar():
            self.pframe.lift()
            self.progress.start()
            self.p3.show_df_result(self.p2.df)
            self.p2.refreshTvResult(self.p2.isNbFilesSup)
            self.progress.stop()
            self.displayed_page = 2

        threading.Thread(target=launchProgressBar).start()


    def create_menubar(self):
        menubar = tk.Menu(self)

        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Help",command=self.show_help)
        menu_file.add_command(label="Exit",command=root.destroy)


        menu_navigate = tk.Menu(menubar, tearoff=0)
        menu_navigate.add_command(label="Next page", command = self.show_nextpage)
        menu_navigate.add_command(label="Previous page", command = self.show_previouspage)

        menu_graph_comparison = tk.Menu(menubar, tearoff=0)
        menu_graph_comparison.add_command(label="Graph", command = self.show_pageFor)
        #menu_graph_comparison.add_command(label="Comparison", command = self.show_pageFive)


        # TODO : close firefox quand on exit ?

        menubar.add_cascade(label="File", menu=menu_file)
        menubar.add_cascade(label="Navigate", menu=menu_navigate)
        menubar.add_cascade(label="Graph", menu=menu_graph_comparison)

        return menubar


if __name__ == "__main__":
    #logger
    global logger
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create filehandler with desired filename.
    fh = logging.FileHandler('log/'+ '{}.log'.format(datetime.now().strftime('%Y_%m_%d')))
    fh.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
    fh.setFormatter(log_formatter)

    ## Add filehandler to logger.
    logger.addHandler(fh)
    logger.debug("Begin")

    os.chdir('.')
    webServer = HTTPServer(('localhost', PORT), RequestHandlerClass=CGIHTTPRequestHandler)
    print("Server enabled: http://localhost:" + str(PORT))
    t = threading.Thread(target=webServer.serve_forever, daemon=True)
    t.start()

    root = tk.Tk()
    root.title("TabIntegration")
    iconPath = str(pathlib.Path(__file__).parent.resolve()) + "\\Icon\\LogoApp.png"
    #root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=iconPath))
    #root.iconbitmap('C:/Users/ANTHONY/Downloads/icons8-doughnut-chart-24.ico')

    main = Container(root)
    main.pack(side="top", fill="both", expand=True)

    root.wm_geometry("800x600")
    root.mainloop()

