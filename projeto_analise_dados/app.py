import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para layout amplo
st.set_page_config(page_title="Análise de Vendas", layout="wide")

st.title(' Análise de Vendas - (Alemanha 2019)') 

# Função com cache para otimizar o carregamento dos dados
@st.cache_data
def load_data():
    df = pd.read_csv('processed/query_valida.csv')
    return df

# Feedback visual de carregamento na tela
data_load_state = st.text('Carregando dados...')
df = load_data()
data_load_state.text('Carregando dados... pronto!')

# Transformação da coluna 'DATA' em formato de data
df['data'] = pd.to_datetime(df['DATA']) 

# --- BARRA LATERAL DE FILTROS ---
st.sidebar.header("Filtros do Dashboard")

canal = st.sidebar.selectbox(
    'Selecione o Canal:', df['ID_CANAL'].unique()
)

data_minima = df['data'].min()
data_selecionada = st.sidebar.date_input('Data ', data_minima)

# Filtrando os dados com base no canal e na data selecionados pelo usuário
df_filtrado = df[  
    (df['ID_CANAL'] == canal) &
    (df['data'] >= pd.Timestamp(data_selecionada))
]

# Exibindo métrica rápida de registros na barra lateral
st.sidebar.markdown("---")
st.sidebar.metric(label="Total de Registros Filtrados", value=len(df_filtrado))

# --- CORPO PRINCIPAL: OPÇÕES GRÁFICAS ---
st.subheader('Painel de Análise Gráfica')

# Seletor para o usuário escolher qual gráfico deseja visualizar
tipo_grafico = st.selectbox(
    'Escolha a perspectiva de visualização:',
    [
        'Evolução Temporal (Linha)', 
        'Distribuição por Mês (Barras)', 
        'Análise de Outliers e Dispersão (Boxplot)'
    ]
)

st.markdown("---")

# Opção 1: Gráfico de Linha (Evolução Temporal)
if tipo_grafico == 'Evolução Temporal (Linha)':
    st.markdown("### 📈 Evolução de Vendas ao Longo do Tempo")
    fig = px.line(
        df_filtrado, 
        x='data', 
        y='VALOR_VENDIDO', 
        title=f'Evolução Diária - Canal {canal}',
        labels={'data': 'Data', 'VALOR_VENDIDO': 'Valor Vendido (€)'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Opção 2: Gráfico de Barras por Mês
elif tipo_grafico == 'Distribuição por Mês (Barras)':
    st.markdown("### 📊 Volume Total de Vendas Agrupado por Mês")
    df_filtrado['mes_ano'] = df_filtrado['data'].dt.to_period('M').astype(str)
    df_mes = df_filtrado.groupby('mes_ano')['VALOR_VENDIDO'].sum().reset_index()
    
    fig = px.bar(
        df_mes, 
        x='mes_ano', 
        y='VALOR_VENDIDO', 
        title=f'Faturamento Mensal - Canal {canal}',
        labels={'mes_ano': 'Mês/Ano', 'VALOR_VENDIDO': 'Total Vendido (€)'},
        color='VALOR_VENDIDO',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)

# Opção 3: Boxplot (Análise de Outliers)
elif tipo_grafico == 'Análise de Outliers e Dispersão (Boxplot)':
    st.markdown("### 📦 Identificação de Outliers (Boxplot)")
    fig = px.box(
        df_filtrado, 
        y='VALOR_VENDIDO', 
        title=f'Distribuição e Dispersão dos Valores - Canal {canal}',
        labels={'VALOR_VENDIDO': 'Valor Vendido (€)'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Exibição opcional da tabela detalhada com os dados brutos filtrados
with st.expander("Visualizar dados brutos filtrados"):
    st.dataframe(df_filtrado)