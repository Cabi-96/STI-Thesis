#Interface
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.messagebox import showinfo

#Algo Integration
import copy
from requests.exceptions import HTTPError
import pandas as pd
import logging
import validators

from application.utils.MtabExtractTable import MtabAnnotationApi
from application.utils.utils import printDf, executeSparqlQuery, insertColumnDf

logger = logging.getLogger(__name__)



class PageTwo(Frame):

    def __init__(self, *args, **kwargs):
        ######Frame pagetwo  : two container one for result (frame_data2 and one for questions and choices frame_selection)
        Frame.__init__(self, *args, **kwargs)

        # variables
        self.textBox_changedf2 = list()
        self.label_changedf2 = list()
        self.textBox_changedf1 = list()
        self.label_changedf1 = list()
        self.listFrame2 = list()
        self.increment = 1
        self.uriLoad = False
        self.isNbFilesSup = False
        self.listTvi = list()
        self.cta = list()
        self.button_Q2_SelectProposition = None

        #### two frames: data and selection (questions)
        ## data
        self.label_frame_data = tk.LabelFrame(self, text="Excel Data",width=500,bg='white')
        self.label_frame_data.pack(side='left',expand="yes", fill="both")

        ## selection
        self.label_frame_selection = Frame(self,bg='white',width=350)
        self.label_frame_selection.pack(fill="y", expand="no", side='left')

        self.label_frame_selection.propagate(0)
        self.label_frame_data.propagate(0)

        #frame result
        self.frameDf = tk.LabelFrame(self.label_frame_data, text='df resultat',bg='white')
        self.tvResult = ttk.Treeview(self.frameDf)
        treescrolly = tk.Scrollbar(self.tvResult, orient="vertical",
                                   command=self.tvResult.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(self.tvResult, orient="horizontal",
                                   command=self.tvResult.xview)  # command means update the xaxis view of the widget
        self.tvResult.configure(xscrollcommand=treescrollx.set,
                                yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget


        ##frame questions in frame selection
        self.frame_questions = tk.LabelFrame(self.label_frame_selection, text="Questions")
        self.frame_questions.pack(expand="yes", fill="both",padx = 5)

        self.listDf = list()
        self.numberOfDf = 0
        self.df = None


    def getCta(self):
        return self.cta

    def show(self):
        self.lift()

    def initObject(self):
        self.increment = 1
        self.uriLoad = False
        self.isNbFilesSup = False
        self.listTvi = list()
        self.frameDf.pack_forget()
        self.listDf = list()
        self.numberOfDf = 0
        self.df = None
        for i in range(0, len(self.listFrame2), 1):
            self.listFrame2[i].destroy()
        self.listFrame2.clear()

    def load_uri(self, p1):
        # Create the dataFrames
        self.initObject()

        for record in self.tvResult.get_children():
            self.tvResult.delete(record)


        api = MtabAnnotationApi(p1.label_file["text"])
        api.extractTableHTML()

        cea = api.getList_CEA_Global()
        #print("CEA")
        #print(cea)

        cpa = api.getList_CPA_Global()
        #print("CPA")
        #print(cpa)

        self.cta = api.getList_CTA_Global()
        #print("CTA")
        # Pour chaque CTA, le premier index est nul. Je l'ai enlevé dans le for juste en dessous.
        #print(cta)

        self.numberOfDf = len(cpa)
        listDictDf = list()

        for frame in self.listFrame2:
            frame.destroy()
        self.listFrame2 = list()

        #file_path = label_file["text"]
        for i in range(0, self.numberOfDf, 1):
            self.df = pd.DataFrame(data=cea[i],
                                   columns=cpa[i],
                                   dtype=str)
            #Supprime la premiere ligne du fichier en ajustant les indexes
            self.df = self.df.reindex(self.df.index.drop(0)).reset_index(drop=True)
            self.cta[i].pop(0)
            listCol = self.df.columns.values.tolist()
            #Supprime les colonnes qui n'ont pas été trouvées par Mtab
            if "" in listCol:
                self.df.drop(labels=[""], axis=1, inplace=True)
            #Supprime les colonnes dupliquées
            self.df = self.df.loc[:, ~self.df.columns.duplicated()]
            #Affiche le tableau
            #print(tabulate(self.df, headers='keys', tablefmt='psql'))
            self.listDf.append(self.df)

            dictDf = dict()
            for j in range(0, len(cpa[i]), 1):
                dictDf[tuple(self.cta[i][j])] = cpa[i][j]
            listDictDf.append(dictDf)

            #print("Load uri self.df")
            #print(self.df)

            ##--------------------------------------------Afficher dataFrames-------------------------------------------------------------------------
            self.listFrame2.append(tk.LabelFrame(self.label_frame_data, text='df',bg='white'))
            #On affiche que les deux premiers DF frames
            if i < 2:
                self.isNbFilesSup = True
                self.listFrame2[i].pack(fill="both",expand="yes", pady = 10, padx = 10)


            tvI = ttk.Treeview(self.listFrame2[i])
            self.listTvi.append(tvI)
            tvI.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

            treescrolly = tk.Scrollbar(self.listFrame2[i], orient="vertical",
                                       command=tvI.yview)  # command means update the yaxis view of the widget
            treescrollx = tk.Scrollbar(self.listFrame2[i], orient="horizontal",
                                       command=tvI.xview)  # command means update the xaxis view of the widget
            tvI.configure(xscrollcommand=treescrollx.set,
                          yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
            treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
            treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget
            tvI["column"] = list(self.df.columns)
            tvI["show"] = "headings"

            for column in tvI["columns"]:
                tvI.heading(column, text=column)  # let the column heading = column name
                df_rows = self.df.to_numpy().tolist()  # turns the dataframe into a list of lists

            for row in df_rows:
                tvI.insert("", "end",
                           values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

        self.uriLoad = True
        self.first_question_show()


    def column_to_uri(self):
        for label in self.label_changedf1:
            label.destroy()

        for textb in self.textBox_changedf1:
            textb.destroy()

        for label in self.label_changedf2:
            label.destroy()

        for textb in self.textBox_changedf2:
            textb.destroy()

        self.label_changedf1 = list()
        self.textBox_changedf1 = list()
        self.label_changedf2 = list()
        self.textBox_changedf2 = list()


        df1 = self.listDf[0]
        df2 = self.listDf[self.increment]
        #print("test")
        columnsDf1 = list(df1.columns)
        columnsDf2 = list(df2.columns)

        i = 0
        change_columnsDf1 = list()
        for column in columnsDf1:
            if str(column).startswith("http") or str(column) == 'Core attribute':
                print('')
            else:
                change_columnsDf1.append(str(i)+'#'+str(column))

            i = i + 1

        i = 0
        change_columnsDf2 = list()
        for column in columnsDf2:
            if str(column).startswith("http") or str(column) == 'Core attribute':
                print('')
            else:
                change_columnsDf2.append(str(i)+'#'+str(column))

            i = i + 1

        if len(change_columnsDf1) + len(change_columnsDf2) > 0:
            self.label_changeColumn = tk.Text(self.frame_questions,background='SystemButtonFace',highlightthickness = 0, borderwidth=0,font=("aerial", 9), height= 3)
            self.label_changeColumn.insert("end","Some Columns have not been identified as URI. You can change it by writing the URI in the input text.")
            self.label_changeColumn.config(state='disabled')
            self.label_changeColumn.pack(padx = 5,fill="none",expand="false")

            i = 0
            #print(len(self.label_changedf1))
            for column in change_columnsDf1:
                self.label_changedf1.append(ttk.Label(self.frame_questions, text=str(column), wraplengt=750))
                self.label_changedf1[i].pack(padx = 5,fill="none",expand="false")
                self.textBox_changedf1.append(ttk.Entry(self.frame_questions))
                self.textBox_changedf1[i].pack(padx = 5,fill="none",expand="false")
                i = i + 1

            i = 0
            for column in change_columnsDf2:
                self.label_changedf2.append(ttk.Label(self.frame_questions, text=str(column), wraplengt=750))
                self.label_changedf2[i].pack(padx = 5,fill="none",expand="false")
                self.textBox_changedf2.append(ttk.Entry(self.frame_questions))
                self.textBox_changedf2[i].pack(padx = 5,fill="none",expand="false")
                i = i + 1

            self.button_column_to_uri_OK = tk.Button(self.frame_questions, text='OK', command=lambda:self.column_to_uri_command())
            self.button_column_to_uri_OK.pack(padx = 5,fill="none",expand="false")

    def column_to_uri_command(self):
        #self.button_Q1_OK["state"] = "disable"
        #print("Column_to_uri_command")
        i = 0
        for textBox in self.textBox_changedf1:
            increment = str(self.label_changedf1[i]['text']).split('#')[0]
            if str(textBox.get()).strip().startswith('http://dbpedia.org/ontology/'):
                self.listDf[0].rename(columns={ self.listDf[0].columns[int(increment)]: str(textBox.get()) }, inplace = True)
            i = i +1

        i = 0
        for textBox in self.textBox_changedf2:
            increment = str(self.label_changedf2[i]['text']).split('#')[0]
            if str(textBox.get()).strip().startswith('http://dbpedia.org/ontology/'):
                self.listDf[self.increment].rename(columns={ self.listDf[self.increment].columns[int(increment)]: str(textBox.get()) }, inplace = True)
            i = i +1

        self.button_column_to_uri_OK.destroy()
        #self.refreshTv()
        self.ask_question()
        self.show()


    def first_question_show(self):
        df1 = self.listDf[0]
        df2 = self.listDf[self.increment]
        #print("test")
        columnsDf1 = list(df1.columns)
        columnsDf2 = list(df2.columns)

        i = 0
        change_columnsDf1 = list()
        for column in columnsDf1:
            if str(column).startswith("http") or str(column) == 'Core attribute':
                print('')
            else:
                change_columnsDf1.append(str(i)+'#'+str(column))

            i = i + 1

        i = 0
        change_columnsDf2 = list()
        for column in columnsDf2:
            if str(column).startswith("http") or str(column) == 'Core attribute':
                print('')
            else:
                change_columnsDf2.append(str(i)+'#'+str(column))

            i = i + 1

        if len(change_columnsDf1) + len(change_columnsDf2) > 0:
            self.column_to_uri()
        else :
            self.ask_question()
        self.show()





    def ask_question(self):
        for widgets in self.frame_questions.winfo_children():
            widgets.destroy()


        if self.uriLoad  == True:
            common_element = set(self.cta[0][0]).intersection(self.cta[self.increment][0])
            frame_text = "CTA from the first Dataset :" + str(self.cta[0][0]) + "\n" + "\nCTA from the second Dataset :" + str(self.cta[self.increment][0]) + "\n" + "\nHere are the common elements :" + str(common_element)

            if len(common_element) == len(self.cta[0][0]):
                frame_text += "\nAll the types in the subject list are found in the target list.\nWe suggest to choose the first choice of dataset integration."
            elif len(common_element) > 0:
                frame_text += "\nNot all types in the subject list are found in the target list. We therefore suggest to choose the second choice of dataset integration."
            else:
                frame_text += "\nNo type is found in the target list."


            self.label_cta = tk.Text(self.frame_questions,background='SystemButtonFace',highlightthickness = 0, borderwidth=0,font=("aerial", 9), height= 15)
            self.label_cta.insert("end",frame_text)
            self.label_cta.config(state='disabled')
            self.label_cta.pack(padx = 5,fill="none",expand="false")

            self.label_rep_Q1 = ttk.Label(self.frame_questions, text="To select the first choice type 1 otherwise type 2:", wraplengt=750)
            self.label_rep_Q1.pack(padx = 5,fill="none",expand="false")
            vcmd = (self.register(self.callback))
            self.textBox_rep_Q1 = ttk.Entry(self.frame_questions, validate='all',validatecommand=(vcmd, '%P'))
            self.textBox_rep_Q1.pack(padx = 5,fill="none",expand="false")
            self.button_Q1_OK = tk.Button(self.frame_questions, text='OK', command=lambda:self.question_2())
            self.button_Q1_OK.pack(padx = 5,fill="none",expand="false")

    def callback(self, P):
        if str(P) == "1" or str(P) == "2" or str(P) == "":
            return True
        else:
            return False

    def refreshTv(self):
        z = -1
        #print(str(len(self.listTvi)))
        for tvI in self.listTvi:
            z = z + 1

            if z == 0:
                #print("I ici: "+str(z))
                for record in tvI.get_children():
                    tvI.delete(record)
                df = self.listDf[0]
                tvI["column"] = list(df.columns)
                tvI["show"] = "headings"

                nbrColumn = 0
                for column in tvI["columns"]:
                    nbrColumn += 1
                    tvI.heading(column, text=column)  # let the column heading = column name
                    df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
                for row in df_rows:
                    tvI.insert("", "end", values=row)

                # Set minimum size for columns
                for i in range(nbrColumn):
                    tvI.column('#' + str(nbrColumn), minwidth=300, stretch=0)
                    # tvResult.heading(i, text="Column {}".format(i))
                    tvI.column('#0', stretch=0)

                tvI.pack(fill="both", expand="yes", pady=10, padx=10)

            elif z == self.increment:
                #print("I ici: "+str(z))
                for record in tvI.get_children():
                    tvI.delete(record)
                #print("Je rentre "+str(z)+" fois")
                df = self.listDf[self.increment]
                #print(df)
                tvI["column"] = list(df.columns)
                tvI["show"] = "headings"

                nbrColumn = 0
                for column in tvI["columns"]:
                    nbrColumn += 1
                    tvI.heading(column, text=column)  # let the column heading = column name
                    df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
                for row in df_rows:
                    tvI.insert("", "end", values=row)

                # Set minimum size for columns
                for i in range(nbrColumn):
                    tvI.column('#' + str(nbrColumn), minwidth=300, stretch=0)
                    # tvResult.heading(i, text="Column {}".format(i))
                    tvI.column('#0', stretch=0)

                tvI.pack(fill="both", expand="yes", pady=10, padx=10)



    def refreshTvResult(self, isLastQuestion):

        for record in self.tvResult.get_children():
            self.tvResult.delete(record)

        self.tvResult["column"] = list(self.df.columns)
        self.tvResult["show"] = "headings"

        nbrColumn = 0
        for column in self.tvResult["columns"]:
            nbrColumn += 1
            self.tvResult.heading(column, text=column)  # let the column heading = column name
            df_rows = self.df.to_numpy().tolist()  # turns the dataframe into a list of lists
        for row in df_rows:
            self.tvResult.insert("", "end", values=row)

        # Set minimum size for columns
        for i in range(nbrColumn):
            self.tvResult.column('#' + str(nbrColumn), minwidth=300, stretch=0)
            #tvResult.heading(i, text="Column {}".format(i))
            self.tvResult.column('#0', stretch=0)

        self.tvResult.pack(fill="both",expand="yes", pady = 10, padx = 10)

        if self.increment == self.numberOfDf:
            self.isNbFilesSup = False

        #print("PAGE TWO"+str(self.increment))
        #printDf(self.df)
        #print("END PAGE TWO")

        if self.isNbFilesSup == True and isLastQuestion == True:
            self.increment = self.increment + 1
            if self.increment < len(self.listFrame2):
                self.listDf[0] = self.df

                self.listFrame2[self.increment].pack(fill="both",expand="yes", pady = 10, padx = 10)

                for widgets in self.listFrame2[0].winfo_children():
                    widgets.destroy()

                self.listFrame2[self.increment-1].pack_forget()
                self.frameDf.pack_forget()

                tvI = ttk.Treeview(self.listFrame2[0])
                self.listTvi[0] = tvI
                self.listTvi[0].place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

                treescrolly = tk.Scrollbar(self.listFrame2[0], orient="vertical",
                                           command=tvI.yview)  # command means update the yaxis view of the widget
                treescrollx = tk.Scrollbar(self.listFrame2[0], orient="horizontal",
                                           command=tvI.xview)  # command means update the xaxis view of the widget
                tvI.configure(xscrollcommand=treescrollx.set,
                              yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
                treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
                treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget
                tvI["column"] = list(self.df.columns)
                tvI["show"] = "headings"

                for column in tvI["columns"]:
                    tvI.heading(column, text=column)  # let the column heading = column name
                    df_rows = self.df.to_numpy().tolist()  # turns the dataframe into a list of lists

                for row in df_rows:
                    tvI.insert("", "end",
                               values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

                for widgets in self.frame_questions.winfo_children():
                    #if widgets['text'] != 'Terminer':
                    widgets.destroy()
                self.first_question_show()

    def askQuestion1(self,listProposition,listWikiLink):
        frameDf = tk.LabelFrame(self.frame_questions, text='Liste proposition')
        frameDf.pack(padx = 5,expand="false", fill="x")

        tvI = ttk.Treeview(frameDf)
        tvI.pack(padx = 5,fill="x",expand="false")

        treescrolly = tk.Scrollbar(frameDf, orient="vertical",
                                   command=tvI.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(frameDf, orient="horizontal",
                                   command=tvI.xview)  # command means update the xaxis view of the widget
        tvI.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

        tvI["column"] = ["Propositions"]
        tvI["show"] = "headings"

        for record in tvI.get_children():
            tvI.delete(record)

        for column in tvI["columns"]:
            tvI.heading(column, text=column)  # let the column heading = column name
            df_rows = listProposition  # turns the dataframe into a list of lists
            for row in df_rows:
                tvI.insert("", "end",values=row)

        self.button_Q_SelectProposition = tk.Button(self.frame_questions, text='Add', command=lambda:self.algo_question_proposition(tvI,listWikiLink))
        self.button_Q_SelectProposition.pack()
        #listComponentDestroy = list()
        #listComponentDestroy.append(button_Q_SelectProposition)
        #listComponentDestroy.append(frameDf)algo_question_proposition
        #return listComponentDestroy

    def question_2(self):
        self.button_Q1_OK["state"] = "disable"
        choice = self.textBox_rep_Q1.get()
        df1 = self.listDf[0]

        #print("Question 2"+str(self.increment))
        #printDf(df1)

        #print("End Question 2")
        df2 = self.listDf[self.increment]
        self.df = self.listDf[0]

        #print("ASK QUESTION 1 INCREMENT")
        #print(self.increment)

        frameProposition = None
        if choice == "1":


            columnDf1 =  df1.columns.values.tolist()
            columnDf2 =  df2.columns.values.tolist()

            listIndexDf2 = list()
            for i in range(len(columnDf2)):
                listIndexDf2.append(i)


            commonElement = list(set(columnDf1).intersection(columnDf2))
            commonElement.remove('Core attribute')
            #print(type(commonElement))
            listIndex = list()
            if len(commonElement) > 0:
                for element in commonElement:
                    listIndex.append(columnDf2.index(element))

                print(listIndexDf2)

                i = 0
                for index in listIndex:
                    #print('index')
                    #print(index)
                    del listIndexDf2[index-i]
                    i = i + 1
                df2tmp = copy.deepcopy(df2.iloc[:, listIndexDf2]) #return all columns except the nth column
                printDf(df2tmp)
            else:
                df2tmp = df2

            self.df = pd.merge(df1,df2tmp)

            #print("-----------------------------------------df--------------------")
            #printDf(self.df)


            #print("-----------------------------------------df1--------------------")
            #printDf(df1)


            #Evite les doublons dans le tableau final pour l'étape append
            #if self.increment == 1:
            #df1 = df1[~df1["Core attribute"].isin(self.df["Core attribute"])].dropna()

            cond = df1.iloc[:,0].isin(self.df.iloc[:,0])
            df1.drop(df1[cond].index, inplace = True)

            #print("df1")
            #printDf(df1)

            cond = df2tmp.iloc[:,0].isin(self.df.iloc[:,0])
            df2.drop(df2[cond].index, inplace = True)

            #print("df2tmp")
            #printDf(df2)

            self.df = self.df.append(df1,ignore_index=True,sort=False)

            #print("self.df")
            #printDf(self.df)

            self.df = self.df.append(df2, ignore_index=True, sort=False)

            self.df = self.df.drop_duplicates(keep='first').reset_index(drop=True)
            printDf(self.df)
            #self.df.to_excel(r'Première Question Tour'+str(self.increment)+'.xlsx', index=False)


            self.frameDf.pack(fill="both",expand="yes", pady = 10, padx = 10)
            self.tvResult.pack(fill="both",expand="yes", pady = 10, padx = 10)

            self.refreshTvResult(False)

        elif choice == "2":
            rowCountDf1 = len(df1.index)
            rowCountDf2 = len(df2.index)
            headerSubjectTable1 = df1.columns.values[0]
            #Skip the first column "Core attribute"
            headers = list(df2.columns.values)[1:]
            # Si on retrouve des dbo qui sont en lien avec notre dbr alors on en ressort des +
            listSubjectOntology = list()
            # Liste contenant les propositions de colonnes. JE SUIS ICI. FAIRE UNE CONDITION POUR N AJOUTER QUE DES VALEURS UNIQUES.
            listProposition = list()
            #REPASSER A 0
            i = 0
            while i < rowCountDf1:
                for item in headers:
                    #print("headerSubjectTable1")
                    #print(headerSubjectTable1)
                    dbrSubject = df1.at[i, headerSubjectTable1]
                    #print(dbrSubject+" "+item)
                    queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + dbrSubject + "> <" + item + "> ?object } \n}"
                    #print(queryString)
                    try:
                        results1 = executeSparqlQuery(queryString)
                    except HTTPError:
                        messagebox.showerror("Error", "Http Problem with DBpedia try later")
                    if results1["results"]["bindings"] and item != "http://dbpedia.org/ontology/wikiPageWikiLink":
                        listSubjectOntology.append(item)
                        resultInserCol = insertColumnDf(listProposition, item,df1.columns.values)
                        #print("Liste proposition :")
                        #print(listProposition)
                        if resultInserCol:
                            listProposition.append(resultInserCol)
                i = i + 1

            # Avec ça, on enlève les colonnes qui ont été insérées dans le df via le insert columnDf en haut.
            headers = set(headers) - set(listSubjectOntology)
            i = 0
            listWikiLink = list()
            headers.add('Core attribute')
            #print(df2.columns.values)
            # S'il y a encore des colonnes dans le headers, ca veut dire que toutes les colonnes vont faire une sorte de produit cartésien. On va prendre chaque cellule de la colonne sujet du df1 et voir si elle a un lien avec les cellules du df2. La perf est de n^4 pas terrible! Peut être moyen de descendre à n^3 mais je ne pense pas.
            if headers:
                while i < rowCountDf1:
                    j = 0
                    resultWiki = set()
                    while j < rowCountDf2:
                        for item in headers:
                            dbrSubject = df1.at[i, headerSubjectTable1]
                            dbrSubject1 = df2.at[j, item]
                            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select distinct ?predicate where { \n { <" + dbrSubject + "> ?predicate <" + dbrSubject1.replace(" ", "") + ">} \n}"
                            #print(queryString)
                            try:
                                results1 = executeSparqlQuery(queryString)
                            except HTTPError:
                                messagebox.showerror("Error", "Http Problem with DBpedia try later")
                            for result in results1["results"]["bindings"]:
                                predicate = result["predicate"]["value"]
                                # Pour l'instant ca va insérer automatiquement la colonne dans le df -> A changer.
                                #print("InsertCol2")
                                resultInserCol = insertColumnDf(listProposition, predicate,df1.columns.values)
                                #print("Fin InsertCol2")
                                if resultInserCol:
                                    listProposition.append(resultInserCol)
                                if predicate == "http://dbpedia.org/ontology/wikiPageWikiLink":
                                    #print(df2.at[j, item])
                                    resultWiki.add(df2.at[j, item]+' ')
                        j = j + 1
                    listWikiLink.append(resultWiki)
                    i = i + 1

            #df = df.drop_duplicates(subset=['Core Attribute'], keep='first')
            #self.df.to_excel(r'Première Question Tour'+str(self.increment)+'.xlsx', index=False)

            #print(tabulate(df, headers='keys', tablefmt='psql'))
            #if self.frameDf != None:
            #    self.frameDf.destroy()
            self.df = df1

            self.frameDf.pack(fill="both",expand="yes", pady = 10, padx = 10)
            self.tvResult.pack(fill="both",expand="yes", pady = 10, padx = 10)
            self.refreshTvResult(False)

            self.askQuestion1(listProposition,listWikiLink)
            #self.df.to_excel(r'Première Question Tour'+str(i)+'.xlsx', index=False)

        button_Q_SelectProposition = tk.Button(self.frame_questions, text='Questions',command=lambda:self.algo_question2_begin(button_Q_SelectProposition,frameProposition))
        button_Q_SelectProposition.pack()

    def algo_question2_begin(self,button_Q_SelectProposition,frameProposition):
        #print("Question 2")
        self.button_Q3_SelectProposition["state"] = "normal"
        button_Q_SelectProposition.destroy()

        if frameProposition != None:
            frameProposition[0].destroy()
            frameProposition[1].destroy()

        for widgets in self.frame_questions.winfo_children():
            #if widgets['text'] == 'Liste proposition' or :
            widgets.destroy()

        label_Add_Column = tk.Text(self.frame_questions,background='SystemButtonFace',highlightthickness = 0, borderwidth=0,font=("aerial", 9), height= 3)
        label_Add_Column.insert("end","If you have another column to add, write it down. \nExample : birthPlace. \nIf you have no more, click on continue:")
        label_Add_Column.config(state='disabled')
        label_Add_Column.pack(padx = 5,fill="none",expand="false")

        textBox_rep_Q2 = ttk.Entry(self.frame_questions)
        textBox_rep_Q2.pack(padx = 5,fill="none",expand="false")

        button_Q2_Proposition = tk.Button(self.frame_questions, text='Choose', command=lambda:self.algo_question2(textBox_rep_Q2,tvI))
        button_Q2_Proposition.pack(padx = 5,fill="none",expand="false")

        button_Q3_Continue = tk.Button(self.frame_questions, text='Continue', command=lambda:self.askQuestion3())
        button_Q3_Continue.pack()

        #Show la liste de proposition
        frameListProposition = tk.LabelFrame(self.frame_questions, text='List of proposals')
        frameListProposition.pack(padx = 5,expand="false", fill="x")

        tvI = ttk.Treeview(frameListProposition)
        tvI.pack(padx = 5,fill="x",expand="false")

        treescrolly = tk.Scrollbar(frameListProposition, orient="vertical",
                                   command=tvI.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(frameListProposition, orient="horizontal",
                                   command=tvI.xview)  # command means update the xaxis view of the widget
        tvI.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

        #Show button selection
        self.button_Q2_SelectProposition = tk.Button(self.frame_questions, text='Add', command=lambda:self.algo_question_proposition(tvI,None))
        self.button_Q2_SelectProposition.pack()

    def algo_question2(self,textBox_rep_Q2,tvI):
        listProposition = list()
        newColumn = str(textBox_rep_Q2.get())
        #if(newColumn == "-1"):
        #    return
        queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n SELECT ?predicate \nWHERE {\n?predicate a rdf:Property\nFILTER ( REGEX ( STR (?predicate), \"http://dbpedia.org/ontology/\", \"i\" ) )\nFILTER ( REGEX ( STR (?predicate), \"" + newColumn + "\", \"i\" ) )\n}\nORDER BY ?predicate"
        # print(queryString)
        try:
            results1 = executeSparqlQuery(queryString)
        except HTTPError:
            messagebox.showerror("Error", "Http Problem with DBpedia try later")
        for result in results1["results"]["bindings"]:
            predicate = result["predicate"]["value"]
            #print("predicate: "+predicate)
            if predicate != "http://dbpedia.org/ontology/wikiPageWikiLink":
                # Pour l'instant ca va insérer automatiquement la colonne dans le df -> A changer.
                resultInserCol = insertColumnDf(listProposition, predicate,self.df.columns.values)
                if resultInserCol and resultInserCol not in listProposition and resultInserCol not in self.df.columns.values:
                    listProposition.append(resultInserCol)

        #print(listProposition)

        tvI["column"] = ["Propositions"]
        tvI["show"] = "headings"

        for record in tvI.get_children():
            tvI.delete(record)

        for column in tvI["columns"]:
            tvI.heading(column, text=column)  # let the column heading = column name
            df_rows = listProposition  # turns the dataframe into a list of lists

        for row in df_rows:
            tvI.insert("", "end",values=row)




    def algo_question_proposition(self,tvI,listWikiLink):
        #get items from proposition's list
        for item in tvI.selection():
            columnAdd = tvI.item(item,"values")
            columnAdd = str(columnAdd)
            if(columnAdd.startswith("(")):
                columnAdd = columnAdd[2:]
                columnAdd = columnAdd[:-3]
            #print(columnAdd)
            if columnAdd == "http://dbpedia.org/ontology/wikiPageWikiLink":
                self.df[columnAdd] = 'nan'
                z = 0
                for wikiLink in listWikiLink:
                    #print(wikiLink)
                    for wiki in wikiLink:
                        #print(wiki)
                        self.df.at[z,columnAdd] = str(wiki)
                    z = z + 1
            else:
                self.df[columnAdd] = 'nan'
        #### refresh df resultat
        self.refreshTvResult(False)


    def askQuestion3(self):
        for widgets in self.frame_questions.winfo_children():
            widgets.destroy()


        label_Add_Column_Q3 = tk.Text(self.frame_questions,background='SystemButtonFace',highlightthickness = 0, borderwidth=0,font=("aerial", 9), height= 4)
        label_Add_Column_Q3.insert("end","Still can't find what you are looking for?\n Please insert the URI of the desired column.\n Example: http://dbpedia.org/ontology/deathDate")
        label_Add_Column_Q3.config(state='disabled')
        label_Add_Column_Q3.pack(padx = 5,fill="none",expand="false")
        textBox_rep_Q3 = ttk.Entry(self.frame_questions)
        textBox_rep_Q3.pack(padx = 5,fill="none",expand="false")
        button_Q3_SelectProposition = tk.Button(self.frame_questions, text='Add', command=lambda:self.algo_question3_proposition(str(textBox_rep_Q3.get())))
        button_Q3_SelectProposition.pack()



    def algo_question3_proposition(self,newColumn):
        if not validators.url(newColumn):
            showinfo(message='URI Not valid')
        elif newColumn not in self.df.columns.values :
            self.df[newColumn] = 'nan'
            self.refreshTvResult(False)
        else:
            #print("La colonne existe déjà dans le DF")
            showinfo(message='The column already exists in the DF')


