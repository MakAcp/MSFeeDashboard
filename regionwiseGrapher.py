import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import csv
import pandas as pd


def regionwise():
    reader = csv.DictReader(open('cleaned.csv', 'r', encoding='utf-8'))
    dict_list = []
    United_Private_sum=0
    United_Private_count=0
    United_Private_Average=0
    United_Average=0
    United_Sum=0
    United_Count=0
    United_Public_count=0
    United_Public_sum=0
    United_Public_Average=0
    Canada_Sum=0
    Canada_Average=0
    Canada_Count=0
    Canada_Private_sum=0
    Canada_Private_count=0
    Canada_Public_sum=0
    Canada_Public_count=0

    for line in reader:
        dict_list.append(line)
    for i in range(0,len(dict_list)):
        if "United States" in dict_list[i]['Country']:
            United_Sum = United_Sum + int(float(dict_list[i]['Fees']))
            United_Count = United_Count+1
            if "Private" in dict_list[i]['Type']:
                United_Private_sum = United_Private_sum + int(float(dict_list[i]['Fees']))
                United_Private_count = United_Private_count+1
            if "Public" in dict_list[i]['Type']:
                United_Public_sum = United_Public_sum + int(float(dict_list[i]['Fees']))
                United_Public_count = United_Public_count + 1
        if "Canada" in dict_list[i]['Country']:
            Canada_Sum = Canada_Average + int(float(dict_list[i]['Fees']))
            Canada_Count = Canada_Count+1
            if "Private" in dict_list[i]['Type']:
                Canada_Private_sum = Canada_Private_sum + int(float(dict_list[i]['Fees']))
                Canada_Private_count = Canada_Private_count + 1
            if "Public" in dict_list[i]['Type']:
                Canada_Public_sum = Canada_Public_sum + int(float(dict_list[i]['Fees']))
                Canada_Public_count = Canada_Public_count + 1





    United_Average=(United_Sum/United_Count)
    Canada_Average=(Canada_Sum/Canada_Count)
    United_Private_Average=(United_Private_sum/United_Private_count)
    United_Public_Average=(United_Public_sum/United_Public_count)
    Canada_Private_Average=(Canada_Private_sum/Canada_Private_count)
    Canada_Public_Average=(Canada_Public_sum/Canada_Public_count)

    Region_list_USA=[]
    Region_list_Canada=[]
    for i in range(0,len(dict_list)):
        if "United States" in dict_list[i]['Country']:
            if dict_list[i]['Region'] not in Region_list_USA:
                Region_list_USA.append(dict_list[i]['Region'])
        if "Canada" in dict_list[i]['Country']:
            if dict_list[i]['Region'] not in Region_list_Canada:
                Region_list_Canada.append(dict_list[i]['Region'])


    Average_dict={}
    Average_dict1={}
    for z in Region_list_USA:
        temp_sum = 0
        count=0
        temp_avg=0
        for i in range(0, len(dict_list)):
           if z in dict_list[i]['Region']:
                temp_sum=temp_sum+int(float(dict_list[i]['Fees']))
                count=count+1
        temp_avg=int(temp_sum/count)
        Average_dict[z]=temp_avg
    for z in Region_list_Canada:
        temp_sum = 0
        count=0
        temp_avg=0
        for i in range(0, len(dict_list)):
           if (z in dict_list[i]['Region']) and ("Canada" in dict_list[i]['Country']):
                temp_sum=temp_sum+int(float(dict_list[i]['Fees']))
                count=count+1
        temp_avg=int(temp_sum/count)
        Average_dict1[z]=temp_avg



    All_Canada_regions=list(Average_dict1.keys())
    All_Canada_regions_fees=list(Average_dict1.values())


    #print(Average_dict)
    All_USA_regions=list(Average_dict.keys())
    All_USA_regions_fees=list(Average_dict.values())



    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


    colors = {
        'background': '#000000',
        'text': '#7FDBFF'
    }

    colors1 = {
        'background': '#00FFFF',
        'text': '#7FDBFF'
    }


    df =pd.DataFrame({
        "Region": All_Canada_regions,
        "Amount": All_Canada_regions_fees
    })

    df1 = pd.DataFrame({
        "Region": All_USA_regions,
        "Amount": All_USA_regions_fees
    })

    fig = px.bar(df, x="Region", y="Amount", color="Region",width=800, height=650)
    fig1 = px.bar(df1,x="Region",y="Amount",color="Region",width=800,height=650)
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    fig1.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color=colors['text']
    )
    x = [html.Div([
        html.Div(style={'backgroundColor': 'white'}, children=[

            html.Div([
                html.H3(
                    children='\n \t \t Canada Region-wise Breakdown',
                    style={'color': colors['text'],
                            'white-space':'pre'
                           }
                ),
                dcc.Graph(id='g1', figure=fig)
            ], className="six columns"),

            html.Div([
                html.H3(
                    children='\n \t \t  USA Region-wise Breakdown',
                    style={'color': colors['text'],
                              'white-space':'pre'
                           }
                ),
                dcc.Graph(id='g2', figure=fig1)
            ], className="six columns"),
        ], className="row")
    ])]
    return x


