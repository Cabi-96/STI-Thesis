#Interface
import tkinter as tk
import pandas as pd
import logging

from tkinter import *
from tkinter import messagebox, ttk, filedialog
from tkinter.filedialog import asksaveasfile, askopenfilename, asksaveasfilename
from urllib.error import HTTPError
from application.utils.utils import printDf, executeSparqlQuery, insertDataDf, writeHtmlFile

logger = logging.getLogger(__name__)


class PageThree(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.df = None

        self.tvResult = ttk.Treeview(self)
        self.tvResult.pack(fill="both",expand="yes", pady = 10, padx = 10)   # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(self.tvResult, orient="vertical",
                                   command=self.tvResult.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(self.tvResult, orient="horizontal",
                                   command=self.tvResult.xview)  # command means update the xaxis view of the widget
        self.tvResult.configure(xscrollcommand=treescrollx.set,
                                yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

        self.button = tk.Button(self, text="Save File as xlsx", command=self.saveXlsx)
        self.button.pack(side='left', padx = 5)

        self.button = tk.Button(self, text="Save File as csv", command=self.saveCsv)
        self.button.pack(side='left', padx = 5)

    def show(self):
        self.lift()

    def transformCoreToUri(self, cta):
        #self.df.columns.values[0] = ''.join(cta[0][0])

        self.df.rename(columns={ self.df.columns[0]: ' '.join(cta[0][0]) }, inplace = True)


        for record in self.tvResult.get_children():
            self.tvResult.delete(record)

        self.tvResult["column"] = list(self.df.columns)
        self.tvResult["show"] = "headings"

        for column in self.tvResult["columns"]:
            self.tvResult.heading(column, text=column)  # let the column heading = column name
            df_rows = self.df.to_numpy().tolist()  # turns the dataframe into a list of lists

        for row in df_rows:
            self.tvResult.insert("", "end",
                                 values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        self.show()
        writeHtmlFile(self.df)


    def saveXlsx(self):
        #SAVING_PATH = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
        #self.df.to_csv(SAVING_PATH,index=False)
        try:
            savefile = asksaveasfilename(filetypes=(("Excel files", "*.xlsx"),
                                                    ("All files", "*.*") ))
            self.df.to_excel(savefile + ".xlsx", index=False, sheet_name="Results")
        except:
            tk.messagebox.showerror("Error. Please try again.")
        return

    def saveCsv(self):
        #SAVING_PATH = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
        #self.df.to_csv(SAVING_PATH,index=False)
        try:
            savefile = asksaveasfilename(filetypes=(("Excel files", "*.csv"),
                                                    ("All files", "*.*") ))
            self.df.to_csv(savefile + ".csv", index=False)
        except:
            tk.messagebox.showerror("Error. Please try again.")
        return

    """
     select ?object where { 
     { <http://dbpedia.org/resource/Dave_Fleischer> <http://dbpedia.org/ontology/wikiPageWikiLink> ?object } 
     filter(regex(?object,'^http://dbpedia.org/resource/Superman$')) 
     }
    """


    def show_df_result(self,df):
        rowCount = len(df.index)
        #print(rowCount)
        headers = list(df.columns.values)
        i = 0
        printDf(df)
        while i < rowCount:
            #print(i)
            for item in headers:
                if item != "http://dbpedia.org/ontology/wikiPageWikiLink":
                    # Si l'item est null il faut le remplir. -> Faudrait changer le if. Ici le nan est en string via la fonction insertColumnDf il faudrait éviter de la mettre en string.
                    print("item: "+item)
                    print(str(i)+" "+df.at[i, item])
                    if pd.isnull(df.at[i, item]) or df.at[i, item] == 'nan' or df.at[i, item] == '':
                        # Ici je récupère la cellule de la colonne sujet.
                        dbrSubject = df.at[i, headers[0]]
                        if str(item).startswith("http:"):
                            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + str(dbrSubject) + "> <" + str(item) + "> ?object } \n}"
                            #print(queryString)
                            try:
                                results1 = executeSparqlQuery(queryString)
                            except HTTPError:
                                messagebox.showerror("Error", "Http Problem with DBpedia try later")
                            # J'écris les résultats trouvés grâce à la query au dessus.
                            df = insertDataDf(df, results1, i, item)
            i = i + 1

        #print("UTILS.PRINTDF FINAL")
        #printDf(df)
        writeHtmlFile(df)


        for record in self.tvResult.get_children():
            self.tvResult.delete(record)

        self.tvResult["column"] = list(df.columns)
        self.tvResult["show"] = "headings"

        for column in self.tvResult["columns"]:
            self.tvResult.heading(column, text=column)  # let the column heading = column name
            df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists

        for row in df_rows:
            self.tvResult.insert("", "end",
                                 values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        self.df = df
        self.show()