from DataIntoDF import DataInfoDF
from collections import Counter
import pandas as pd

def printDf(df):
    print(df)
    df.to_csv(r'C:\Users\ANTHONY\Desktop\ECOLE\MA1\Mémoire\Outil\File Name.csv',index=False)

#def cleanDbrOrDbo(value):
#    index = value.rfind('/')
#    value = value[index+1:]
#    value = value.replace(',','\,')
#    return value

def executeSparqlQuery(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

#Va permettre d'insérer dans la colonne du dataframe, le resultat de la query SPARQL
def insertDataDf(df,results):
    df.at[i,item] = str(df.at[i,item]).replace("nan","")
    for result in results["results"]["bindings"]:
        predicate = result["object"]["value"]
        df.at[i,item] = str(df.at[i,item]) + str(predicate) + " "

#Va permettre de retrouver les ontologies/colonnes lorsqu'on arrive pas à trouver une valeur pour une cellule. (Ca permet de remplir le tableau)
def ontologiesSearch(df,rowCount,item):
    #Ici je récupère le dbr de la colonne sujet.
    i=0
    dictlist = list()
    while i < rowCount:

        dbrSubject0 = str(df.at[i, headers[0]])
        #dbrSubject0 = cleanDbrOrDbo(dbrSubject0)

        #Ici je récupère le dbr de la colonne manquante.
        #print(dbrSubject)

        dbrSubject1 = str(df.at[i, item])
        #dbrSubject1 = cleanDbrOrDbo(dbrSubject1)

        #On ne reprend pas les nan
        if(dbrSubject1 != 'nan'):
            #Je créé une query sparql qui me permet de récupérer des predicats intéressants.
            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select distinct ?predicate where { \n { <"+dbrSubject0+"> ?predicate <"+dbrSubject1+">} \n}"
            #print(queryString)
            results = executeSparqlQuery(queryString)
            for result in results["results"]["bindings"]:
                predicate = result["predicate"]["value"]
                #print("predicate")
                #print(predicate)
                #Je récupère toutes les valeurs pour pouvoir vérifier leurs occurences.
                dictlist.append(predicate)
            #print("Resultats query ontology")
            #print(results)
        i = i+1

    #print("Liste d'ontologies retrouvées")
    #print(dictlist)

    #Je reprends celui avec le plus d'occurences.
    most_common,num_most_common = Counter(dictlist).most_common(1)[0]
    #print(most_common,num_most_common)
    #print("Fin de la liste")
    #print(value+" "+count)

    return most_common

# Code SPARQL vient de : https://stackoverflow.com/questions/58519010/constructing-graph-using-rdflib-for-the-outputs-from-sparql-select-query-with
from SPARQLWrapper import SPARQLWrapper, JSON
#labelName = URIRef("<http://dbpedia.org/resource/" + name +">")

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

#Create the dataFrames
dataInfoDF = DataInfoDF('annotations_CEA_12_05_2021(1).csv','cpa.csv')

df1 = dataInfoDF.runTab1()
df2 = dataInfoDF.runTab2()
print("DataFrame 1")
print(df1)
print("DataFrame 2")
print(df2)
#Permet de retrouver tous les noms des colonnes/ontologies.
ontologies1 = dataInfoDF.getOntologiesTable1()
ontologies2 = dataInfoDF.getOntologiesTable2()
#Boolean qui permet de savoir si la colonne sujet trouve une correspondance avec une colonne du deuxième dataset.
isSameColumn = False

#Premier cas, lorsque la colonne sujet match une colonne du deuxième dataset! Comme pour la classe DataInfoDF j'estime que la colonne sujet est la numéro 0. Trouver un moyen de récupérer la classe sujet de l'outil.
for ontology in ontologies2:
    if ontologies1[0] == ontology:
        isSameColumn = True
        break

# if(isSameColumn) -> Performance n^4 -> Dans le mémoire faudra en parler commme une faiblesse !
# else -> Performance ? Encore à tester!
if(isSameColumn):
    #Je mélange les deux datasets avec le append
    df = result = df1.append(df2, ignore_index=True, sort=False)

    # print the list of all the column headers
    #print("The column headers :")
    headers = list(df.columns.values)
    #print(headers)
    i = 0
    rowCount = len(df.index)

    #STI du premier cas.
    while i < rowCount:
        for item in headers:
            #Si l'item est null il faut le remplir.
            if pd.isnull(df.at[i,item]):

                #Ici je récupère la cellule de la colonne sujet.
                dbrSubject = df.at[i, headers[0]]
                #dbrSubject = cleanDbrOrDbo(dbrSubject)
                #print(dbrSubject)

                #Ici je récupère la cellule de la colonne pour l'ontologie qui m'intéresse je remove un chiffre s'il y a en a un à la fin.
                itemOntology = item
                if(item[-1].isdigit()):
                    itemOntology = item[:-1]
                dbo = itemOntology
                #print(dbo)

                #Je décide de vérifier les ontologies pouvant correspondre au tableau.
                dbo = ontologiesSearch(df,rowCount,item)
                #Via la query d'au dessus j'ai pu récupérer de nouveaux dbo qui peuvent correspondre à mon dbr
                #Vérifier le rdf type avec l'ontologie de la colonne!
                queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <"+dbrSubject+"> <"+dbo+"> ?object } \n}"
                results1 = executeSparqlQuery(queryString)
                #J'écris les résultats trouvé grâce à la query au dessus.
                insertDataDf(df,results1)
        i = i+1
    print("DataFrame Final")
    printDf(df)
else:
    print("test")


