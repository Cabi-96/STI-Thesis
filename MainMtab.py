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
print(cea[2])
print(cea[3])
cpa = api.getList_CPA_Global()
print("CPA")
print(cpa[0])
print(cpa[1])
print(cpa[2])
print(cpa[3])
cta = api.getList_CTA_Global()
print("CTA")
print(cta[0])
print(cta[1])
print(cta[2])
print(cta[3])

#Check length
#lengthValidate = False
#if len(cea) == len(cta) and len(cea) == len(cpa):
#    lengthValidate = True




numberOfDf = len(cpa)
listDf = list()
for i in range(0,numberOfDf,1):
    df = pd.DataFrame(data=cea[i],
                      columns = cpa[i],
                      dtype=str)
    df = df.iloc[1: , :]
    print(tabulate(df, headers='keys', tablefmt='psql'))
    listDf.append(df)
    # df.to_csv(r'File Name.csv',index=False)
    # df.to_excel(r'File Name.xlsx', index=False)

listCTASubject = cta[1]
listCTATarget = cta[2]


common_element = set(listCTASubject[1]).intersection(listCTATarget[1])
print("Types for the first list: "+str(listCTASubject[1]))
print("Types for the second list: "+str(listCTATarget[1]))
print("Number of Common elements: "+str(len(common_element)))
print("Common elements :")
print(common_element)


if len(common_element) == len(listCTASubject[1]):
    print("Tous les types de la liste sujet se retrouvent dans la liste cible. Nous suggérons donc de choisir le premier choix d'intégration de dataset.")
    #DF1
    df1 = listDf[1]
    #Remove duplicate columns
    df1 = df1.loc[:,~df1.columns.duplicated()]
    #DF2
    df2 = listDf[2]
    #Remove duplicate columns
    df2 = df2.loc[:,~df2.columns.duplicated()]
    df1.reset_index(drop=True)
    df2.reset_index(drop=True)
    df = df1.append(df2, ignore_index=True, sort=False)
    print(tabulate(df, headers='keys', tablefmt='psql'))
elif len(common_element) > 0:
    print("Tous les types de la liste sujet ne se retrouvent pas dans la liste cible. Nous suggérons donc de choisir le deuxième choix d'intégration de dataset.")
else :
    print("Aucun type n'est retrouvé dans la liste cible. Le deuxième choix d'intégration sera utilisé.")