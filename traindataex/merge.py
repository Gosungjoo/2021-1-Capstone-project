import pandas as pd
import re

data1 = pd.read_csv(r"traindata.csv")
data1 = data1[:5500]
data2 = pd.read_csv(r"smallset.csv")

merged = pd.concat([data1,data2], ignore_index=True)

print(len(merged))

merged.to_csv('traindata1.csv', encoding='ANSI')