import pandas as pd
import re

data = pd.read_csv(r"traindata1.csv", encoding="ANSI")
sdata = pd.DataFrame(data, columns=['사용자명','댓글'])
print(sdata.iloc[1])
kdata = pd.DataFrame({"사용자명":[], "댓글":[]})
traindata = pd.DataFrame({"사용자명":[], "댓글":[]})


for i in range(1, len(sdata)):
    if ([] != re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', str(sdata.loc[i][0]))) or ([] != re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', str(sdata.loc[i][1]))):
        kdata = kdata.append(sdata.loc[i])

print(kdata)


'''
kdata.to_csv('trainset3.csv')
'''