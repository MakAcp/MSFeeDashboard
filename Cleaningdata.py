import pandas as pd
import numpy as np

df_csv = pd.read_csv(r'C:\Users\nihar\PycharmProjects\MSinUS\Uni.csv', header=0)
df_filtered = df_csv.dropna()
df_filtered = df_filtered[df_filtered['Fees'] != 'N.A']
df_filtered = df_filtered.reset_index(drop=True)


# CONVERTING TO USD AND SOME MINOR CORRECTIONS


def clean_currency(x):
    if isinstance(x, str):
        return (x.replace('$', '').replace('Fr', '').replace('kr', '').replace('£', '').replace('¥', '').replace('NZ',
                                                                                                                 '').replace(
            'S', '').replace('A', '').replace('A$', '').replace('C$', '').replace('€', '').replace('â‚¬', '').replace(
            ',', '').replace('C', ''))
    return (x)


df_filtered['Fees'] = df_filtered['Fees'].apply(clean_currency).astype('float')
df_filtered['Fees'] = df_filtered['Fees'].apply(pd.to_numeric)
df_filtered['Country'] = df_filtered['Country'].astype('str')

df_filtered.loc[df_filtered.Country.str.contains('Singapore', case=False), 'Fees'] = df_filtered['Fees'] * 0.73
df_filtered.loc[df_filtered.Country.str.contains('Canada', case=False), 'Fees'] = df_filtered['Fees'] * 0.75
df_filtered.loc[df_filtered.Country.str.contains('Australia', case=False), 'Fees'] = df_filtered['Fees'] * 0.72
df_filtered.loc[df_filtered.Country.str.contains('France', case=False), 'Fees'] = df_filtered['Fees'] * 1.18
df_filtered.loc[df_filtered.Country.str.contains('Germany', case=False), 'Fees'] = df_filtered['Fees'] * 0.60
df_filtered.loc[df_filtered.Country.str.contains('Switzerland', case=False), 'Fees'] = df_filtered['Fees'] * 1.09
df_filtered.loc[df_filtered.Country.str.contains('New Zealand', case=False), 'Fees'] = df_filtered['Fees'] * 0.66
df_filtered.loc[df_filtered.Country.str.contains('Japan', case=False), 'Fees'] = df_filtered['Fees'] * 0.0094
df_filtered.loc[df_filtered.Country.str.contains('Netherlands', case=False), 'Fees'] = df_filtered['Fees'] * 1.18
df_filtered.loc[df_filtered.Country.str.contains('Sweden', case=False), 'Fees'] = df_filtered['Fees'] * 0.11
df_filtered.loc[df_filtered.Country.str.contains('Ireland', case=False), 'Fees'] = df_filtered['Fees'] * 1.18
df_filtered.loc[df_filtered.Country.str.contains('United Kingdom', case=False), 'Fees'] = df_filtered['Fees'] * 1.31
df_filtered.loc[df_filtered.Type.str.contains('private', case=False), 'Type'] = 'Private University'
df_filtered.loc[df_filtered.Type.str.contains('Provate', case=False), 'Type'] = 'Private University'
df_filtered.loc[df_filtered.Type.str.contains('public', case=False), 'Type'] = 'Public University'

# PUTTING CLEANED VERSION INTO CSV

df_filtered.to_csv(r'C:/Users/nihar/PycharmProjects/MSinUS/cleaned.csv', encoding='utf-8')
