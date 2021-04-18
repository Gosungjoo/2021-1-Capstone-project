import pandas as pd
import re

data1 = pd.read_csv(r"trainset1.csv")
data2 = pd.read_csv(r"trainset2.csv")

merged = pd.concat([data1,data2], ignore_index=True)

print(len(merged))

merged.to_csv('traindata.csv', encoding='UTF-8')