"""

'ALB_1_silver_peak_nevada.csv'
'ALB_2_salar_de_atacama_chile.csv'
'LAC_1_jujuy_province_argentia.csv'
'LAC_2_salta_province_argentina.csv'
'SQM_1_salar_de_atacama_chile.csv'
'SQM_2_salar_del_carmen_chile.csv'


"""

import pandas as pd



r1 = pd.read_csv('ALB_1_silver_peak_nevada.csv')
r2 = pd.read_csv('ALB_2_salar_de_atacama_chile.csv')
r3 = pd.read_csv('LAC_1_jujuy_province_argentia.csv')
r4 = pd.read_csv('LAC_2_salta_province_argentina.csv')
r5 = pd.read_csv('SQM_1_salar_de_atacama_chile.csv')
r6 = pd.read_csv('SQM_2_salar_del_carmen_chile.csv')

print(r1.shape)
print(r2.shape)
print(r3.shape)
print(r4.shape)
print(r5.shape)
print(r6.shape)

#df_merged = pd.merge(r1, r2, r3, r4, r5, r6)
output1 = pd.merge(r1, r2, on='datetime', how='inner')
output2 = pd.merge(output1, r3, on='datetime', how='inner')
output3 = pd.merge(output2, r4, on='datetime', how='inner')
output4 = pd.merge(output3, r5, on='datetime', how='inner')
output5 = pd.merge(output4, r6, on='datetime', how='inner')
output5.to_csv('merged_weather.csv', index=False)
print(output5)
