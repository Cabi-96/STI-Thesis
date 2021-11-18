import csv

import pandas as pd
f=pd.read_csv(r"C:\Users\ANTHONY\Desktop\caseTest\File_2.csv")
print(f.columns.values)
keep_col = ['Title','Year','Media Type','Length', 'Matting']
new_f = f[keep_col]
new_f.to_csv(r"C:\Users\ANTHONY\Desktop\caseTest\File_3.csv", index=False, quoting=csv.QUOTE_ALL)