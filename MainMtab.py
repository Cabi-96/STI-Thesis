# -----------------------------------------------------------------
#                           MAIN
# -----------------------------------------------------------------


from MtabAnnotationApi import MtabAnnotationApi
from tabulate import tabulate
import pandas as pd
import numpy as np

api = MtabAnnotationApi("C:/Users/ANTHONY/Desktop/TestMtab/")
api.post_request()

cea = api.getList_CEA_Global()
print("CEA")
print(cea[0])
print(cea[1])
#print(cea[2])
#print(cea[3])

cpa = api.getList_CPA_Global()
print("CPA")
print(cpa[0])
print(cpa[1])
#print(cpa[2])
#print(cpa[3])

cta = api.getList_CTA_Global()
print("CTA")
#Pour chaque CTA, le premier index est nul. Je l'ai enlevé dans le for juste en dessous.
print(cta[0])
print(cta[1])
#print(cta[2])
#print(cta[3])

#Check length
#lengthValidate = False
#if len(cea) == len(cta) and len(cea) == len(cpa):
#    lengthValidate = True




numberOfDf = len(cpa)
listDf = list()
listDictDf = list()
for i in range(0,numberOfDf,1):
    df = pd.DataFrame(data=cea[i],
                      columns = cpa[i],
                      dtype=str)
    df = df.iloc[1: , :]
    cta[i].pop(0)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    df.drop(labels=[""],axis=1,inplace=True )
    df = df.loc[:,~df.columns.duplicated()]
    df.reset_index(drop=True)
    print("After drop")
    print(tabulate(df, headers='keys', tablefmt='psql'))
    listDf.append(df)
    j=0
    dictDf = dict()
    for j in range(0,len(cpa[i]),1):
        dictDf[tuple(cta[i][j])] = cpa[i][j]
    listDictDf.append(dictDf)
    # df.to_csv(r'File Name.csv',index=False)
    # df.to_excel(r'File Name.xlsx', index=False)

print(listDictDf)


for i in range(1,len(listDictDf),1):
    common_element = set(cta[0][0]).intersection(cta[i][0])
    if len(common_element) == len(cta[0][0]):
        print("Tous les types de la liste sujet se retrouvent dans la liste cible. Nous suggérons donc de choisir le premier choix d'intégration de dataset.")
        #DF1
        df1 = listDf[0]
        #DF2
        df2 = listDf[i]
        listDf[0] = df1.append(df2, ignore_index=True, sort=False)
        print(tabulate(listDf[0], headers='keys', tablefmt='psql'))
    elif len(common_element) > 0:
        print("Tous les types de la liste sujet ne se retrouvent pas dans la liste cible. Nous suggérons donc de choisir le deuxième choix d'intégration de dataset.")
    else :
        print("Aucun type n'est retrouvé dans la liste cible. Le deuxième choix d'intégration sera utilisé.")


