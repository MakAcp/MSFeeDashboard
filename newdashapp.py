import dash
import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies as dd
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from regionwiseGrapher import regionwise
df = pd.read_excel('universities3.xlsx')
def world_data_preparer():
    mapdf = pd.read_excel('mapdf.xlsx')
    df2 = pd.DataFrame(df['country'].value_counts())
    df2['Country'] = df2.index
    merged = pd.merge(left = df2, right = mapdf, left_on='Country',right_on='COUNTRY')

    del merged['Unnamed: 0']
    merged = merged.rename(columns={'country':'annual_fees','Country':'country','COUNTRY':'a','CODE':'CODE'})
    del merged['a']
    return merged

def cont_data_preparer(country):
    merged = pd.DataFrame()
    usa_codes = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')
    usa_codes = usa_codes[['code','state']].set_index('state')['code'].to_dict()
    row_dict = {}
    tempdf = df.loc[df['country']==country] #All colleges in USA
    fee_avg = tempdf['average_annual_fee'].mean()
    state_set = list(set(tempdf['state']))
    for state in state_set:
        string = ''
        temp = df.loc[df['state']== state]
        state_avg = round(temp['average_annual_fee'].mean(),1)
        temp.dropna(subset=['global_rank'], inplace=True)
        try:
            temp.sort_values(temp['global_rank'])
        except Exception:
            pass
        for idx, row in temp.iloc[0:5].iterrows():
            string = string + ' <br> ' + row['name'] + ', ' + row['state']+', '+str(row['average_annual_fee'])+ '(' +str(state_avg-round(row['average_annual_fee'],1))+')'

        if not state in usa_codes.keys():
                continue
        row_dict = {'state':state ,'code':usa_codes[state],'state_avg': state_avg ,'topfive':string}
        merged = merged.append(row_dict,ignore_index=True)


    return merged








external_stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css",'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)


app.layout = html.Div(className='container-lg', children=[

    html.H1('College Visulaizer'),



    html.Div(className = 'card',children = [dcc.Dropdown( id = 'graphChooser',
    options=[
        {'label': 'World Map', 'value': 'WLD'},
        {'label': 'USA', 'value': 'USA'},


    ],value = 'WLD'),
    html.Div(id = 'graphContainer',className='card-body')])]+regionwise())



@app.callback(
    dd.Output('graphContainer','children'),
    [dd.Input('graphChooser', 'value')])

def update_graph(value):
    if value == 'WLD':
        i = 0
        merged = world_data_preparer()
        for country in merged['country']:

            df3 = df.loc[df['country'] == country]
            df3.dropna(subset=['global_rank'], inplace=True)
            try:
                df3.sort_values(df3['global_rank'])
            except Exception as e:
                pass
            string = ''
            c = 1

            for idx, row in df3.iloc[0:5].iterrows():
                string = string + ' <br> ' + row['name'] + ', ' + row['state']

                c += 1

            merged.loc[i, 'TopTen'] = str(string)

            i += 1

        fig = go.Figure(data=go.Choropleth(
            locations=merged['CODE'],
            z=merged['annual_fees'],
            text=merged['country'] + '<br>' + merged['TopTen'],

            colorscale=[[0, 'rgb(255, 224, 46)'], [0.5, 'rgb(93, 2, 184)'], [1, 'rgb(255, 21, 0)']],
            reversescale=False,

            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title='Distribution of Popular Colleges for MS',
        ))

        fig.update_layout(
            width=1500,
            title_text='Distribution of College Data',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),

        )

    if value == 'USA':
        merged = cont_data_preparer('United States')
        fig = go.Figure(data=go.Choropleth(
            locations=merged['code'],  # Spatial coordinates
            z=merged['state_avg'],
            text =merged['topfive'],
            locationmode='USA-states',  # set of locations match entries in `locations`
            colorscale='Reds',
            colorbar_title="Millions USD",
        ))

        fig.update_layout(
            title_text='Statewise Variation of from Average Fees',
            geo_scope='usa',
        )




    return (dcc.Graph(figure=fig))







if __name__ == '__main__':
    app.run_server(debug=True)




