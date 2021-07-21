# -----------------------------------------------------------------
#                           MAIN
# -----------------------------------------------------------------


from MtabAnnotationApi import MtabAnnotationApi
from tabulate import tabulate
import pandas as pd

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
for i in range(0,numberOfDf,1):
    df = pd.DataFrame(data=cea[i],
                      columns = cpa[i],
                      dtype=str)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    # df.to_csv(r'File Name.csv',index=False)
    # df.to_excel(r'File Name.xlsx', index=False)
