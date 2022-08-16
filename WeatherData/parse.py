import pandas as pd

#ALB 
r1 = pd.read_csv('silver_peak_nevada.csv', usecols = ['datetime','temp','humidity','conditions','windspeed']) #alb
r2 = pd.read_csv('salar_de_atacama_chile.csv', usecols = ['datetime','temp','humidity','conditions','windspeed']) #alb
#LAC
r3 = pd.read_csv('jujuy_province_argentia.csv', usecols = ['datetime','temp','humidity','conditions','windspeed']) #lac
r4 = pd.read_csv('salta_province_argentina.csv', usecols = ['datetime','temp','humidity','conditions','windspeed']) #lac
#SQM
r5 = pd.read_csv('salar_de_atacama_chile.csv', usecols = ['datetime','temp','humidity','conditions','windspeed']) #sqm
r6 = pd.read_csv('salar_del_carmen_chile.csv', usecols = ['datetime','temp','humidity','conditions','windspeed'])  #sqm
recs=['r1', 'r2', 'r3', 'r4', 'r5']

print("Number of lines present in record r1 : ",len(r1))
print("Number of lines present in record r2 : ",len(r2))
print("Number of lines present in record r3 : ",len(r3))
print("Number of lines present in record r4 : ",len(r4))
print("Number of lines present in record r5 : ",len(r5))
print("Number of lines present in record r5 : ",len(r6))
"""
print(r1['conditions'].unique())
print(r2['conditions'].unique())
print(r3['conditions'].unique())
print(r4['conditions'].unique())
print(r5['conditions'].unique())
"""

uConditions = []
for index, row in r1.iterrows():
    strn=row['conditions']
    if strn not in uConditions:
    	uConditions.append(strn)

for index, row in r2.iterrows():
    strn=row['conditions']
    if strn not in uConditions:
    	uConditions.append(strn)

for index, row in r3.iterrows():
    strn=row['conditions']
    if strn not in uConditions:
    	uConditions.append(strn)

for index, row in r4.iterrows():
    strn=row['conditions']
    if strn not in uConditions:
    	uConditions.append(strn)

for index, row in r5.iterrows():
    strn=row['conditions']
    if strn not in uConditions:
    	uConditions.append(strn)

for index, row in r6.iterrows():
    strn=row['conditions']
    if strn not in uConditions:
    	uConditions.append(strn)

uConditions.sort()
print(uConditions)


for index, row in r1.iterrows():
    strn=row['conditions']
    idx = uConditions.index(strn)
    r1.at[index,'conditions'] = idx

for index, row in r2.iterrows():
    strn=row['conditions']
    idx = uConditions.index(strn)
    r2.at[index,'conditions'] = idx

for index, row in r3.iterrows():
    strn=row['conditions']
    idx = uConditions.index(strn)
    r3.at[index,'conditions'] = idx

for index, row in r4.iterrows():
    strn=row['conditions']
    idx = uConditions.index(strn)
    r4.at[index,'conditions'] = idx

for index, row in r5.iterrows():
    strn=row['conditions']
    idx = uConditions.index(strn)
    r5.at[index,'conditions'] = idx

for index, row in r6.iterrows():
    strn=row['conditions']
    idx = uConditions.index(strn)
    r6.at[index,'conditions'] = idx


columns = ['datetime','temp','humidity','conditions','windspeed']
r1.rename({'temp': 'ALB_1_temp', 'humidity': 'ALB_1_humidity', 'conditions': 'ALB_1_conditions', 'windspeed': 'ALB_1_windspeed'}, axis=1, inplace=True)

r2.rename({'temp': 'ALB_2_temp', 'humidity': 'ALB_2_humidity', 'conditions': 'ALB_2_conditions', 'windspeed': 'ALB_2_windspeed'}, axis=1, inplace=True)

r3.rename({'temp': 'LAC_1_temp', 'humidity': 'LAC_1_humidity', 'conditions': 'LAC_1_conditions', 'windspeed': 'LAC_1_windspeed'}, axis=1, inplace=True)

r4.rename({'temp': 'LAC_2_temp', 'humidity': 'LAC_2_humidity', 'conditions': 'LAC_2_conditions', 'windspeed': 'LAC_2_windspeed'}, axis=1, inplace=True)

r5.rename({'temp': 'SQM_1_temp', 'humidity': 'SQM_1_humidity', 'conditions': 'SQM_1_conditions', 'windspeed': 'SQM_1_windspeed'}, axis=1, inplace=True)

r6.rename({'temp': 'SQM_2_temp', 'humidity': 'SQM_2_humidity', 'conditions': 'SQM_2_conditions', 'windspeed': 'SQM_2_windspeed'}, axis=1, inplace=True)

#ALB
r1.to_csv('ALB_1_silver_peak_nevada.csv', index=False) #alb
r2.to_csv('ALB_2_salar_de_atacama_chile.csv', index=False) #alb
#LAC
r3.to_csv('LAC_1_jujuy_province_argentia.csv', index=False) #lac
r4.to_csv('LAC_2_salta_province_argentina.csv', index=False) #lac
#SQM
r5.to_csv('SQM_1_salar_de_atacama_chile.csv', index=False) #sqm
r6.to_csv('SQM_2_salar_del_carmen_chile.csv', index=False)  #sqm