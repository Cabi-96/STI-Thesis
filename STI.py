from collections import defaultdict
from time import sleep

from requests.exceptions import MissingSchema

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
def insertDataDf(df, results, i, key, item):
    if key is not None:
        itemOntology = cleanLastDigit(key)
        objectFilter = itemOntology.split(" ")
        stringFilter = ""

        # Ici on récupère toutes les ontologies de la colonne une par une.
        for object in objectFilter:
            stringFilter += "?object = <" + object + "> ||\n"
        stringFilter = stringFilter[:-3]

        for result in results["results"]["bindings"]:
            predicate = result["object"]["value"]
            # print(item)
            # print(predicate)

            # Cette query va permettre de vérifier que l'entité qu'on va insérer dans le tableau possède dans son rdf type, les différentes ontologies de la colonne. A CHANGER ICI.
            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + predicate + "> rdf:type ?object } \n FILTER (" + stringFilter + ")\n}"
            #print(queryString)
            resultsFilter = executeSparqlQuery(queryString)
            # print("FILTER")
            #print(queryString)
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

#Peut etre delete
def insertColumnDf_OLD(df,column):
    index = column.rfind('/')
    tmpColumn = column[index+1:]
    listColumnName = list()

    for item in df.columns.values:
        index = item.rfind('/')
        item = item[index+1:]
        listColumnName.append(item)

    print(tmpColumn)
    print(listColumnName)

    if tmpColumn not in listColumnName:
        #Permet d'ajouter la colonne au df mais en com pour mettre les propositions.
        #df[column] = np.nan
        #df[column] = df[column].astype('string')
        return column


def insertColumnDf(listProposition,column):
    index = column.rfind('/')
    tmpColumn = column[index+1:]
    listColumnName = list()
    for proposition in listProposition:
        index = proposition.rfind('/')
        tmpproposition = proposition[index+1:]
        listColumnName.append(tmpproposition)
    if tmpColumn not in listColumnName:
        return column


# -----------------------------------------------------------------
#                           MAIN
# -----------------------------------------------------------------


# Create the dataFrames
path = str(pathlib.Path().absolute())
dataInfoDF = DataInfoDF(path+'/.idea/files/annotations_CEA_12_05_2021.csv', path+'/.idea/files/cta.csv')

df1 = dataInfoDF.runTab1()
dictDf1 = dataInfoDF.getOntologiesDictTable().copy()
df2 = dataInfoDF.runTab2()
dictDf2 = dataInfoDF.getOntologiesDictTable().copy()

#print("Df1 dict")
#print(dictDf1)
#print("Df2 dict")
#print(dictDf2)

print("DataFrame 1")
print(tabulate(df1, headers='keys', tablefmt='psql'))
print("DataFrame 2")
print(tabulate(df2, headers='keys', tablefmt='psql'))

# Permet de retrouver tous les noms des colonnes/ontologies.
ontologies1 = dataInfoDF.getOntologiesTable1()
ontologies2 = dataInfoDF.getOntologiesTable2()


# Boolean qui permet de savoir si la colonne sujet trouve une correspondance avec une colonne du deuxième dataset.
isSameColumn = False

# Premier cas, lorsque la colonne sujet match une colonne du deuxième dataset! Comme pour la classe DataInfoDF j'estime que la colonne sujet est la numéro 0. Trouver un moyen de récupérer la classe sujet de l'outil.
for ontology in ontologies2:
    if ontologies1[0] == ontology:
        isSameColumn = True
        break

# if(isSameColumn) -> Performance n^3 -> Dans le mémoire faudra en parler commme une faiblesse ou comme force, n^3 ca reste correcte !
# else -> Performance ? Encore à tester!
if (isSameColumn):
    # Je mélange les deux datasets avec le append
    df = df1.append(df2, ignore_index=True, sort=False)
    print("DICTF1 ET DICTF2")
    print(dictDf1)
    print(dictDf2)
    dictDf = dictDf1 | dictDf2
    print(dictDf)
    # print the list of all the column headers
    # print("The column headers :")
    headers = list(df.columns.values)
    # print(headers)
    i = 0
    rowCount = len(df.index)
    headers = list(df.columns.values)
    # STI du premier cas.
    print(dictDf)
    while i < rowCount:
        for key, item in dictDf.items():
            print("Dans la boucle key,item: ")
            print(key)
            print(item)
            # Si l'item est null il faut le remplir.
            if item and pd.isnull(df.at[i, item]):
                # Ici je récupère la cellule de la colonne sujet.
                dbrSubject = df.at[i, headers[0]]
                #print("ITEM: "+item)
                queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + dbrSubject + "> <" + item + "> ?object } \n}"
                #print(queryString)
                results1 = executeSparqlQuery(queryString)
                # J'écris les résultats trouvé grâce à la query au dessus.
                insertDataDf(df, results1, i, key, item)
        i = i + 1
    print("DataFrame Final")

    # Clean les headers qui ont un chiffre à la fin.
    #for item in headers:
    #    if (item[-1].isdigit()):
    #        df.rename(columns={item: item[:-1]}, inplace=True)
    printDf(df)
# Si les colonnes sujet ne correspondent pas.
else:
    rowCountDf1 = len(df1.index)
    rowCountDf2 = len(df2.index)
    headerSubjectTable1 = df1.columns.values[0]
    headers = list(df2.columns.values)
    #Si on retrouve des dbo qui sont en lien avec notre dbr alors on en ressort des +
    listSubjectOntology = list()
    #Liste contenant les propositions de colonnes. JE SUIS ICI. FAIRE UNE CONDITION POUR N AJOUTER QUE DES VALEURS UNIQUES.
    listProposition = list()
    i = 0
    while i < rowCountDf1:
        for item in headers:
            dbrSubject = df1.at[i, headerSubjectTable1]
            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + dbrSubject + "> <" + item + "> ?object } \n}"
            #print(queryString)
            results1 = executeSparqlQuery(queryString)
            if results1["results"]["bindings"]:
                listSubjectOntology.append(item)
                resultInserCol = insertColumnDf(listProposition,item)
                if resultInserCol and resultInserCol not in listProposition:
                    listProposition.append(resultInserCol)
        i = i+1

    #Avec ça, on enlève les colonnes qui ont été insérées dans le df via le insert columnDf en haut.
    headers = set(headers) - set(listSubjectOntology)
    i = 0
    j = 0
    #S'il y a encore des colonnes dans le headers, ca veut dire que toutes les colonnes va faire une sorte de produit cartésien. On va prendre chaque cellule de la colonne sujet du df1 et voir si elle a un lien avec les cellules du df2. La perf est de n^4 pas terrible! Peut être moyen de descendre à n^3 mais je ne pense pas.
    if headers:
        while i < rowCountDf1:
            while j < rowCountDf2:
                for item in headers:
                    dbrSubject = df1.at[i, headerSubjectTable1]
                    dbrSubject1 = df2.at[j, item]
                    queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select distinct ?predicate where { \n { <" + dbrSubject + "> ?predicate <" + dbrSubject1 + ">} \n}"
                    #print(queryString)
                    results1 = executeSparqlQuery(queryString)
                    for result in results1["results"]["bindings"]:
                        predicate = result["predicate"]["value"]
                        if predicate != "http://dbpedia.org/ontology/wikiPageWikiLink":
                            #Pour l'instant ca va insérer automatiquement la colonne dans le df -> A changer.
                            resultInserCol = insertColumnDf(listProposition,predicate)
                            if resultInserCol and resultInserCol not in listProposition:
                                listProposition.append(resultInserCol)
                j = j+1
            i = i+1
    i = 0
    #Permet d'itérer sur un nombre de proposition. En donnant leur index dans la liste pour permettre de facilement les sélectionner.
    #Question 1
    listProposition.append('http://dbpedia.org/ontology/birthDate')
    #listProposition.append('http://dbpedia.org/ontology/deathDate')
    print("Propositions: ")
    for proposition in listProposition:
        print(str(i)+" "+proposition)
        i = i + 1
    choice = 0
    while int(choice) != -1:
        if len(listProposition) == 0:
            print("Plus de choix dans la liste.")
            break
        choice = input("Sélectionner les propositions une par une en écrivant leurs numéros (-1 pour sortir de la question):")
        if int(choice) == -1 or len(listProposition) == 0:
            print(choice)
            print("Tous les choix ont été enregistrés")
            break
        column = listProposition[int(choice)]
        #print(choice+" "+column)
        df1[column] = np.nan
        df1[column] = df1[column].astype('string')
        printDf(df1)
        listProposition.remove(column)
        print("Le choix "+column+" a été ajouté au dataframe")

    #Question 2
    listProposition.clear()
    print("Voulez-vous proposer des colonnes à rajouter? Veuillez insérer la valeur. Exemple : birthPlace  ")
    newColumn = input("Ecrivez votre choix :")
    queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n SELECT ?predicate \nWHERE {\n?predicate a rdf:Property\nFILTER ( REGEX ( STR (?predicate), \"http://dbpedia.org/ontology/\", \"i\" ) )\nFILTER ( REGEX ( STR (?predicate), \""+newColumn+"\", \"i\" ) )\n}\nORDER BY ?predicate"
    #print(queryString)
    results1 = executeSparqlQuery(queryString)
    for result in results1["results"]["bindings"]:
        predicate = result["predicate"]["value"]
        if predicate != "http://dbpedia.org/ontology/wikiPageWikiLink":
            #Pour l'instant ca va insérer automatiquement la colonne dans le df -> A changer.
            resultInserCol = insertColumnDf(listProposition,predicate)
            if resultInserCol and resultInserCol not in listProposition:
                listProposition.append(resultInserCol)
    i = 0
    for proposition in listProposition:
        print(str(i)+" "+proposition)
        i = i + 1
    choice = 0
    while int(choice) != -1:
        if len(listProposition) == 0:
            print("Plus de choix dans la liste.")
            break
        choice = input("Sélectionner les propositions une par une en écrivant leurs numéros (-1 pour sortir de la question):")
        if int(choice) == -1:
            #print(choice)
            print("Tous les choix ont été enregistrés")
            break
        column = listProposition[int(choice)]
        #print(choice+" "+column)
        df1[column] = np.nan
        df1[column] = df1[column].astype('string')
        listProposition.remove(column)
        printDf(df1)

    #Question 3
    #Rajouter des colonnes que l'algorithme n'aura pas retrouver
    print("Ce que vous cherchez n'a toujours pas été trouvé? Veuillez insérer l'URI de la colonne souhaitée. Exemple : http://dbpedia.org/ontology/deathDate  ")
    newColumn = input("Ecrivez votre choix :")
    newColumn = newColumn.strip()
    try:
        request = requests.get(newColumn)
    except ConnectionError:
        print('Link does not exist')
    except MissingSchema:
        print('Link does not exist')
    else:
        print('Link exists')
        df1[newColumn] = np.nan
        df1[newColumn] = df1[newColumn].astype('string')
        printDf(df1)
    #A changer il faudrait directement utiliser df
    df = df1

    """
    api = MtabAnnotationApi("")
    api.extract_entity(newColumn)
    if newColumn != "":
        resultsApi = search_entity(newColumn)
    print("Voici les différents mots retrouver avec votre entrée: ")
    i = 0
    for resultApi in resultsApi:
        print(str(i)+" "+resultApi)
        i = i + 1
    choice = input("Sélectionner la proposition en écrivant son numéro: ")
    column = resultsApi[int(choice)]
    """
    """
    Query pour les matchs.
    SELECT ?pred 
    WHERE
     { 
       ?pred a rdf:Property
       FILTER ( REGEX ( STR (?pred), "http://dbpedia.org/ontology/", "i" ) )
       FILTER ( REGEX ( STR (?pred), "birthdate", "i" ) )
     }
    ORDER BY ?pred 
    """

print("Inserting values...")
#Insert values.
i = 0
rowCount = len(df.index)
headers = list(df.columns.values)
# STI du deuxième cas. Très similaire sauf qu'on ne boucle pas sur la meme chose. Ici on boucle sur les colonnes du df. Dans le premier cas c'est via le dictionnaire. -> A améliorer. Créer une méthode pour éviter d'avoir 2 fois le meme code.
while i < rowCount:
    for item in headers:
        # Si l'item est null il faut le remplir. -> Faudrait changer le if. Ici le nan est en string via la fonction insertColumnDf il faudrait éviter de la mettre en string.
        if  pd.isnull(df.at[i, item]):
            # Ici je récupère la cellule de la colonne sujet.
            dbrSubject = df.at[i, headers[0]]
            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + dbrSubject + "> <" + item + "> ?object } \n}"
            #print(queryString)
            results1 = executeSparqlQuery(queryString)
            # J'écris les résultats trouvés grâce à la query au dessus.
            insertDataDf(df, results1, i,None, item)
    i = i + 1
print("DataFrame Final")
printDf(df)
print("Done")
