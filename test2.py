import plotly.graph_objects as go
import pandas as pd

df = pd.read_excel('universities3.xlsx')
mapdf = pd.read_excel('mapdf.xlsx')
df2 = pd.DataFrame(df['country'].value_counts())
df2['Country'] = df2.index
merged = pd.merge(left = df2, right = mapdf, left_on='Country',right_on='COUNTRY')
#del merged['Country']
merged.rename(index ={1:'annual_fees'})
#\print("YAHO")
del merged['Unnamed: 0']
merged = merged.rename(columns={'country':'annual_fees','Country':'country','COUNTRY':'a','CODE':'CODE'})
del merged['a']
for country in merged['country']:
    df3 =  df.loc[df['country']  == country]
    df3.dropna(subset = ['global_rank'],inplace = True)

    print("Yay")
