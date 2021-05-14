from csv import reader
from DataIntoDF import DataInfoDF
import pandas as pd

def printDf(df):
    print(df)
    df.to_csv(r'C:\Users\ANTHONY\Desktop\ECOLE\MA1\Mémoire\Outil\File Name.csv',index=False)

def cleanDbrOrDbo(value):
    index = value.rfind('/')
    value = value[index+1:]
    value = value.replace(',','\,')
    return value

def executeSparqlQuery(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


# Code SPARQL vient de : https://stackoverflow.com/questions/58519010/constructing-graph-using-rdflib-for-the-outputs-from-sparql-select-query-with
from SPARQLWrapper import SPARQLWrapper, JSON
#labelName = URIRef("<http://dbpedia.org/resource/" + name +">")

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

#Create the dataFrames
dataInfoDF = DataInfoDF('annotations_CEA_12_05_2021(1).csv','cpa.csv')

df1 = dataInfoDF.runTab1()
df2 = dataInfoDF.runTab2()

#Premier cas, lorsque la colonne sujet match une colonne du deuxième dataset!
#Je mélange les deux datasets avec le append
df = result = df1.append(df2, ignore_index=True, sort=False)

# print the list of all the column headers
print("The column headers :")
headers = list(df.columns.values)
print(headers)
i = 0
rowCount = len(df.index)

#STI du premier cas.
while i < rowCount:
    for item in headers:
        #Si l'item est null il faut le remplir.
        if pd.isnull(df.at[i,item]):

            #Ici je récupère la cellule de la colonne sujet.
            dbrSubject = df.at[i, headers[0]]
            dbrSubject = cleanDbrOrDbo(dbrSubject)
            #print(dbrSubject)

            #Ici je récupère la cellule de la colonne pour l'ontologie qui m'intéresse je remove un chiffre s'il y a en a un à la fin.
            itemOntology = item
            if(item[-1].isdigit()):
                itemOntology = item[:-1]
            dbo = cleanDbrOrDbo(itemOntology)
            #print(dbo)

            #Je retrouve l'objet qui m'intéresse pour l'ajouter dans le tableau.
            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { dbr:"+dbrSubject+" dbo:"+dbo+" ?object } \n}"
            results = executeSparqlQuery(queryString)
            #print(queryString))

            #On récupère le résultat de la query sparql. S'il y a un résultat on l'insère dans la colonne, sinon on cherche une ontology correspondante. -> Créer une méthode pour ça?
            if results["results"]["bindings"]:
                df.at[i,item] = str(df.at[i,item]).replace("nan","")
                for result in results["results"]["bindings"]:
                    predicate = result["object"]["value"]
                    df.at[i,item] = str(df.at[i,item]) + str(predicate) + " "
            else:
                #print("ELSE")
                #Je décide de vérifier la première ligne et de retrouver l'ontology de celle-ci. /!\ A AMELIORER-> Il faudrait vérifier toutes les lignes et prendre celle avec la plus grosse occurence.
                #Ici je récupère le dbr de la colonne sujet.
                dbrSubject0 = df.at[0, headers[0]]
                dbrSubject0 = cleanDbrOrDbo(dbrSubject0)

                #Ici je récupère le dbr de la colonne manquante.
                #print(dbrSubject)
                dbrSubject1 = df.at[0, item]
                dbrSubject1 = cleanDbrOrDbo(dbrSubject1)

                #print(dbrSubject1)
                #Je créé une query sparql qui me permet de récupérer des predicats intéressants.
                queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select distinct ?predicate where { \n { dbr:"+dbrSubject0+" ?predicate dbr:"+dbrSubject1+"} \n}"
                #print(queryString)
                results = executeSparqlQuery(queryString)

                #Via la query d'au dessus j'ai pu récupérer de nouveaux dbo qui peuvent correspondre à mon dbr -> Créer une méthode pour ça?
                if results["results"]["bindings"]:
                    df.at[i,item] = str(df.at[i,item]).replace("nan","")
                    for result in results["results"]["bindings"]:
                        predicate = result["predicate"]["value"]
                        if str(predicate) != "http://dbpedia.org/ontology/wikiPageWikiLink":
                            itemOntology = predicate
                            if(predicate[-1].isdigit()):
                                itemOntology = result[:-1]
                            dbo = cleanDbrOrDbo(itemOntology)
                            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { dbr:"+dbrSubject+" dbo:"+dbo+" ?object } \n}"
                            results1 = executeSparqlQuery(queryString)

                            if results1["results"]["bindings"]:
                                df.at[i,item] = str(df.at[i,item]).replace("nan","")
                                for result1 in results1["results"]["bindings"]:
                                    predicate = result1["object"]["value"]
                                    df.at[i,item] = str(df.at[i,item]) + str(predicate) + " "
    i = i+1

printDf(df)


