import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv('processed/query_valida.csv')
st.dataframe(df.head(10))
st.write(f'Total de registros: {len(df)}')

df['data'] = pd.to_datetime(df['DATA'])

canal = st.selectbox(
    'Canal:', df['ID_CANAL'].unique())
data = st.date_input('DATA:')

df_filtrado = df[
    (df['ID_CANAL'] == canal) &
    (df['data'] >= pd.Timestamp(data))
]


fig = px.line(df_filtrado, x='data', y='VALOR_VENDIDO')
st.plotly_chart(fig)


