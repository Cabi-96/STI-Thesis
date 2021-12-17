from tkinter import *
import logging

logger = logging.getLogger(__name__)


class PageFor(Frame):

    #def __init__(self, *args, **kwargs):
        #Frame.__init__(self, *args, **kwargs)
        #frame = tkinterweb.HtmlFrame(self)
        #frame.load_website("https://www.google.com/")
        #frame.pack(fill="both", expand=True)



    def show(self):
        self.lift()