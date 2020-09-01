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
i=0
for country in merged['country']:

    df3 = df.loc[df['country'] == country]
    df3.dropna(subset=['global_rank'], inplace=True)
    try:
        df3.sort_values(df3['global_rank'])
    except Exception as e:
        pass
    string = ''
    c=1

    for idx,row in df3.iloc[0:5].iterrows():
        string = string + ' \n ' + row['name'] + ', '+ row['state']

        c+=1


    merged.loc[i,'TopTen'] = str(string)
    print(string)
    i+=1


print(merged)
fig = go.Figure(data=go.Choropleth(
    locations = merged['CODE'],
    z = merged['annual_fees'],
    text = merged['country'] + '\n' + merged['TopTen'] ,

    colorscale = [[0,'rgb(255, 224, 46)'],[0.5,'rgb(93, 2, 184)'],[1,'rgb(255, 21, 0)']],
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = 'Distribution of Popular Colleges for MS',
))

fig.update_layout(
    title_text='2014 Global GDP',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',

        showarrow = False
    )]
)

fig.show()
