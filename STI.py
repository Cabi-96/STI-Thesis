from collections import defaultdict
from time import sleep

from requests.exceptions import MissingSchema, HTTPError

from DataIntoDF import DataInfoDF
from tabulate import tabulate
import pandas as pd
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON
import pathlib
import requests

from MtabAnnotationApi import MtabAnnotationApi


def printDf(df):
    print(tabulate(df, headers='keys', tablefmt='psql'))
    # df.to_csv(r'File Name.csv',index=False)
    df.to_excel(r'File Name.xlsx', index=False)


def cleanLastDigit(item):
    # Ici je récupère la cellule de la colonne pour l'ontologie qui m'intéresse je remove un chiffre s'il y a en a un à la fin.
    itemOntology = item
    if (item[-1].isdigit()):
        itemOntology = item[:-1]
    # print(itemOntology)
    return itemOntology


def executeSparqlQuery(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


# Va permettre d'insérer dans la colonne du dataframe, le resultat de la query SPARQL ici en fonction du cas passé en argument, on vérifie son rdf type ou pas.
"""
def insertDataDfOld(df, results, i, key, item):
    print("InsertDataDF")
    
    if key is not None:
        stringFilter = ""

        # Ici on récupère toutes les ontologies de la colonne une par une.
        for object in key:
            stringFilter += "?object = <" + object + "> ||\n"
        stringFilter = stringFilter[:-3]
        print(stringFilter)

        for result in results["results"]["bindings"]:
            predicate = result["object"]["value"]
            # print(item)
            # print(predicate)

            # Cette query va permettre de vérifier que l'entité qu'on va insérer dans le tableau possède dans son rdf type, les différentes ontologies de la colonne.
            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + predicate + "> rdf:type ?object } \n FILTER (" + stringFilter + ")\n}"
            #print(queryString)
            resultsFilter = executeSparqlQuery(queryString)
            # print("FILTER")
            print(queryString)
            if resultsFilter["results"]["bindings"]:
                # Faire disparaitre la valeur NaN avec fillna() mais pas réussi. df.fillna('') -> A AMELIORER! Créer une fonction c'est presque le meme code qu'en bas, sauf que le replace se fait sur le nan et le replace d'en dessous sur <NA>
                if len(str(df.at[i, item])) == 3:
                    df.at[i, item] = str(df.at[i, item]).replace("nan", "")
                df.at[i, item] = str(df.at[i, item]) + str(predicate) + " "
    else:
        for result in results["results"]["bindings"]:
            predicate = result["object"]["value"]
            #print(predicate)
            if len(str(df.at[i, item])) == 4:
                df.at[i, item] = str(df.at[i, item]).replace("<NA>", "")
            elif len(str(df.at[i, item])) == 3:
                df.at[i, item] = str(df.at[i, item]).replace("nan", "")
            #print(df.at[i, item])
            #print(len(str(df.at[i, item])))
            df.at[i, item] = str(df.at[i, item]) + str(predicate) + " "
"""


def insertDataDf(df, results, i, item):
    for result in results["results"]["bindings"]:
        predicate = result["object"]["value"]
        #print(predicate)
        if len(str(df.at[i, item])) == 4:
            df.at[i, item] = str(df.at[i, item]).replace("<NA>", "")
        elif len(str(df.at[i, item])) == 3:
            df.at[i, item] = str(df.at[i, item]).replace("nan", "")
            # print(df.at[i, item])
            # print(len(str(df.at[i, item])))
        df.at[i, item] = str(df.at[i, item]) + str(predicate) + " "


def insertColumnDf(listProposition, column):
    index = column.rfind('/')
    tmpColumn = column[index + 1:]
    listColumnName = list()
    for proposition in listProposition:
        index = proposition.rfind('/')
        tmpproposition = proposition[index + 1:]
        listColumnName.append(tmpproposition)
    if tmpColumn not in listColumnName:
        return column

def askQuestion1(df,listProposition):
    #listProposition.append('http://dbpedia.org/ontology/birthDate')
    #listProposition.append('http://dbpedia.org/ontology/deathDate')
    print("Question 1")
    choice = 0
    while int(choice) != -1:
        print("Propositions: ")
        i = 0
        for proposition in listProposition:
            print(str(i) + " " + proposition)
            i = i + 1
        if len(listProposition) == 0:
            print("Plus ou pas de choix dans la liste de propositions.")
            break
        choice = input("Sélectionner les propositions une par une en écrivant leurs numéros (-1 pour sortir de la question):")
        if int(choice) == -1 or len(listProposition) == 0:
            print(choice)
            print("Tous les choix ont été enregistrés")
            break
        column = listProposition[int(choice)]
        # print(choice+" "+column)
        df[column] = 'nan'
        #df[column] = df[column].astype('string')
        printDf(df)
        listProposition.remove(column)
        print("Le choix " + column + " a été ajouté au dataframe")

def askQuestion2(df):
    listProposition = list()
    print("Question 2")
    newColumn = "0"
    while newColumn != "-1":
        newColumn = input("Si vous avez une autre colonne à ajouter ecrivez le. Exemple : birthPlace. Si vous n'en avez plus, écrivez -1:")
        if(newColumn == "-1"):
            break
        queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n SELECT ?predicate \nWHERE {\n?predicate a rdf:Property\nFILTER ( REGEX ( STR (?predicate), \"http://dbpedia.org/ontology/\", \"i\" ) )\nFILTER ( REGEX ( STR (?predicate), \"" + newColumn + "\", \"i\" ) )\n}\nORDER BY ?predicate"
        # print(queryString)
        results1 = executeSparqlQuery(queryString)
        for result in results1["results"]["bindings"]:
            predicate = result["predicate"]["value"]
            if predicate != "http://dbpedia.org/ontology/wikiPageWikiLink":
                # Pour l'instant ca va insérer automatiquement la colonne dans le df -> A changer.
                resultInserCol = insertColumnDf(listProposition, predicate)
                if resultInserCol and resultInserCol not in listProposition and resultInserCol not in df.columns.values:
                    listProposition.append(resultInserCol)
        choice = 0
        while int(choice) != -1:
            if len(listProposition) == 0:
                print("Plus ou pas de choix dans la liste.")
                break
            i = 0
            for proposition in listProposition:
                print(str(i) + " " + proposition)
                i = i + 1
            choice = input("Sélectionner les propositions une par une en écrivant leurs numéros (-1 pour sortir de la question):")
            if int(choice) == -1:
                # print(choice)
                print("Tous les choix ont été enregistrés")
                break
            column = listProposition[int(choice)]
            # print(choice+" "+column)
            df[column] = 'nan'
            #df[column] = df[column].astype('string')
            listProposition.remove(column)
            printDf(df)
    return df

def askQuestion3(df):
    listProposition = list()
    print("Question 3")
    print("Ce que vous cherchez n'a toujours pas été trouvé? Veuillez insérer l'URI de la colonne souhaitée. Exemple : http://dbpedia.org/ontology/deathDate  ")
    newColumn = "0"
    while newColumn != "-1":
        newColumn = input("Si vous avez un autre URI à ajouter ecrivez le. Si vous n'en avez plus, écrivez -1:")
        newColumn = newColumn.strip()
        try:
            request = requests.get(newColumn)
        except ConnectionError:
            print('Le lien n existe pas')
        except MissingSchema:
            print('Le lien n existe pas')
        else:
            #print('Le lien existe')
            if newColumn and newColumn not in listProposition and newColumn not in df.columns.values:
                df[newColumn] = 'nan'
                #df[newColumn] = np.nan
                #df[newColumn] = df[newColumn].astype('string')
                printDf(df)
            else:
                print("La colonne existe déjà dans le DF")
    return df

# -----------------------------------------------------------------
#                           MAIN
# -----------------------------------------------------------------


# Create the dataFrames
path = str(pathlib.Path().absolute())

api = MtabAnnotationApi(path+'/.idea/files/case_3')
api.post_request()

cea = api.getList_CEA_Global()
print("CEA")
print(cea)

cpa = api.getList_CPA_Global()
print("CPA")
print(cpa)

cta = api.getList_CTA_Global()
print("CTA")
# Pour chaque CTA, le premier index est nul. Je l'ai enlevé dans le for juste en dessous.
print(cta)

numberOfDf = len(cpa)
listDf = list()
listDictDf = list()
for i in range(0, numberOfDf, 1):
    df = pd.DataFrame(data=cea[i],
                      columns=cpa[i],
                      dtype=str)
    print(tabulate(df, headers='keys', tablefmt='psql'))
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
    print(tabulate(df, headers='keys', tablefmt='psql'))
    listDf.append(df)
    j = 0
    dictDf = dict()
    for j in range(0, len(cpa[i]), 1):
        dictDf[tuple(cta[i][j])] = cpa[i][j]
    listDictDf.append(dictDf)
    # df.to_csv(r'File Name.csv',index=False)
    # df.to_excel(r'File Name.xlsx', index=False)

#print(listDictDf)

for i in range(1, len(listDictDf), 1):
    common_element = set(cta[0][0]).intersection(cta[i][0])
    print(cta[0][0])
    print(cta[i][0])
    print("Voici les éléments en communs :" + str(common_element))
    if len(common_element) == len(cta[0][0]):
        print(
            "Tous les types de la liste sujet se retrouvent dans la liste cible. Nous suggérons donc de choisir le premier choix d'intégration de dataset.")
    elif len(common_element) > 0:
        print(
            "Tous les types de la liste sujet ne se retrouvent pas dans la liste cible. Nous suggérons donc de choisir le deuxième choix d'intégration de dataset.")
    else:
        print("Aucun type n'est retrouvé dans la liste cible. Le deuxième choix d'intégration sera utilisé.")

    choice = input("Pour choisir le premier choix taper 1 sinon taper 2 :")
    df1 = listDf[0]
    df2 = listDf[i]
    if choice == "1":
        # DF1

        df = df1.append(df2, ignore_index=True, sort=False)
        print(tabulate(df, headers='keys', tablefmt='psql'))
        """
        Implementation not finished with the dictionnary, it's possible to check the type of the data that has been inserted.
        dictDf1 = listDictDf[0]
        dictDf2 = listDictDf[i]
        #print("DICTF1")
        #print(dictDf1)
        #print("DICTF2")
        #print(dictDf2)
        dictDf = dictDf1 | dictDf2
        #print(dictDf)
        
        # print the list of all the column headers
        # print("The column headers :")
        headers = list(df.columns.values)
        # print(headers)
        j = 0
        rowCount = len(df.index)
        headers = list(df.columns.values)
        # STI du premier cas.
        #print(dictDf)
        while j < rowCount:
            for key, item in dictDf.items():
                # Si l'item est null il faut le remplir.
                for itemObj in item:
                    if itemObj and pd.isnull(df.at[i, itemObj]):
                        # Ici je récupère la cellule de la colonne sujet.
                        dbrSubject = df.at[i, headers[0]]
                        #print("ITEM: "+item)
                        queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + dbrSubject + "> <" + itemObj + "> ?object } \n}"
                        #print(queryString)
                        results1 = executeSparqlQuery(queryString)
                        # J'écris les résultats trouvés grâce à la query au dessus.
                        #print("TEST INSERT DATA")
                        insertDataDfOLd(df, results1, j, key, itemObj)
                j = j + 1
            print("DataFrame Final")
            printDf(df)
        """
        #Question 2

        askQuestion2(df)

        # Question 3
        listDf[0] = askQuestion3(df)
    # Si les colonnes sujet ne correspondent pas.
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
        i = 1
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
                    print("Problème Http avec l'application Mtab veuillez ressayer plus tard.")
                if results1["results"]["bindings"]:
                    listSubjectOntology.append(item)
                    resultInserCol = insertColumnDf(listProposition, item)
                    #print(str(resultInserCol)+" in:")
                    #print("Liste proposition :")
                    #print(listProposition)
                    if resultInserCol and resultInserCol not in listProposition and item not in df1.columns.values:
                        listProposition.append(resultInserCol)
            i = i + 1

        # Avec ça, on enlève les colonnes qui ont été insérées dans le df via le insert columnDf en haut.
        headers = set(headers) - set(listSubjectOntology)
        i = 0
        # S'il y a encore des colonnes dans le headers, ca veut dire que toutes les colonnes vont faire une sorte de produit cartésien. On va prendre chaque cellule de la colonne sujet du df1 et voir si elle a un lien avec les cellules du df2. La perf est de n^4 pas terrible! Peut être moyen de descendre à n^3 mais je ne pense pas.
        if headers:
            while i < rowCountDf1:
                j = 0
                while j < rowCountDf2:
                    for item in headers:
                        dbrSubject = df1.at[i, headerSubjectTable1]
                        dbrSubject1 = df2.at[j, item]
                        queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select distinct ?predicate where { \n { <" + dbrSubject + "> ?predicate <" + dbrSubject1 + ">} \n}"
                        #print(queryString)
                        try:
                            results1 = executeSparqlQuery(queryString)
                        except HTTPError:
                            print("Problème Http avec l'application Mtab veuillez ressayer plus tard.")
                        for result in results1["results"]["bindings"]:
                            predicate = result["predicate"]["value"]
                            if predicate != "http://dbpedia.org/ontology/wikiPageWikiLink":
                                # Pour l'instant ca va insérer automatiquement la colonne dans le df -> A changer.
                                resultInserCol = insertColumnDf(listProposition, predicate)
                                if resultInserCol and resultInserCol not in listProposition and predicate not in df1.columns.values:
                                    listProposition.append(resultInserCol)
                    j = j + 1
                i = i + 1
        # Permet d'itérer sur un nombre de proposition. En donnant leur index dans la liste pour permettre de facilement les sélectionner.
        # Question 1
        askQuestion1(df1,listProposition)

        # Question 2
        askQuestion2(df1)

        # Question 3
        # Rajouter des colonnes que l'algorithme n'aura pas retrouver
        df = askQuestion3(df1)
        listDf[0] = df



print("Inserting values...")
rowCount = len(df.index)
headers = list(df.columns.values)
i = 0
# STI du deuxième cas. Très similaire sauf qu'on ne boucle pas sur la meme chose. Ici on boucle sur les colonnes du df. Dans le premier cas c'est via le dictionnaire. -> A améliorer. Créer une méthode pour éviter d'avoir 2 fois le meme code.
while i < rowCount:
    for item in headers:
        # Si l'item est null il faut le remplir. -> Faudrait changer le if. Ici le nan est en string via la fonction insertColumnDf il faudrait éviter de la mettre en string.
        if pd.isnull(df.at[i, item]) or df.at[i, item] == 'nan':
            # Ici je récupère la cellule de la colonne sujet.
            dbrSubject = df.at[i, headers[0]]
            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + dbrSubject + "> <" + item + "> ?object } \n}"
            #print(queryString)
            results1 = executeSparqlQuery(queryString)
            # J'écris les résultats trouvés grâce à la query au dessus.
            insertDataDf(df, results1, i, item)
    i = i + 1

print("DataFrame Final")
printDf(df)
print("Done")
