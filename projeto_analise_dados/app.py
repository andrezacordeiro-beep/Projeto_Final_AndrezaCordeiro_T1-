import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da página (deve ser sempre o primeiro comando do Streamlit)
st.set_page_config(page_title="Análise de Vendas", layout="wide")

st.title('📊 Análise de Vendas - (Alemanha 2019)') 

# 2. Função com cache para otimizar e carregar os dados de forma limpa
@st.cache_data
def load_data():
    # Carrega o arquivo CSV processado
    df = pd.read_csv('data/processed/query_valida.csv')
    
    # Converte a coluna 'DATA' para o formato datetime (padrão brasileiro DD/MM/AAAA)
    # errors='coerce' transforma eventuais datas inválidas em valores nulos para não quebrar o app
    df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True, errors='coerce')
    
    # Remove o horário (zera as horas para 00:00:00), mantendo o tipo datetime puro ideal para filtros
    df['DATA'] = df['DATA'].dt.normalize()
    
    return df

# Feedback visual de carregamento na tela
data_load_state = st.text('Carregando dados...')
df = load_data()
data_load_state.text('Carregando dados... pronto!')

# --- 3. BARRA LATERAL DE FILTROS ---
st.sidebar.header("Filtros do Dashboard")

# Seletor de Canal de Vendas
canal = st.sidebar.selectbox(
    'Selecione o Canal:', df['CANAL'].unique()
)

# Filtro de Data Inicial baseado na menor data disponível na base
data_minima = df['DATA'].min().date() # Converte para o formato date do Python para o Streamlit
data_selecionada = st.sidebar.date_input('Data Inicial:', data_minima)

# --- 4. APLICAÇÃO DOS FILTROS NOS DADOS ---
# Filtra o DataFrame considerando o canal escolhido e a data selecionada
df_filtrado = df[  
    (df['CANAL'] == canal) &
    (df['DATA'] >= pd.to_datetime(data_selecionada))
]

# Exibindo métrica rápida de registros na barra lateral
st.sidebar.markdown("---")
st.sidebar.metric(label="Total de Registros Filtrados", value=len(df_filtrado))

# --- 5. CORPO PRINCIPAL: OPÇÕES GRÁFICAS ---
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
        x='DATA', 
        y='VALOR_VENDIDO', 
        title=f'Evolução Diária - Canal {canal}',
        labels={'DATA': 'Data', 'VALOR_VENDIDO': 'Valor Vendido (€)'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Opção 2: Gráfico de Barras por Mês
elif tipo_grafico == 'Distribuição por Mês (Barras)':
    st.markdown("### 📊 Volume Total de Vendas Agrupado por Mês")
    
    # Cria uma cópia ou coluna temporária formatada como ano-mês para agrupamento
    df_filtrado_copia = df_filtrado.copy()
    df_filtrado_copia['mes_ano'] = df_filtrado_copia['DATA'].dt.to_period('M').astype(str)
    df_mes = df_filtrado_copia.groupby('mes_ano')['VALOR_VENDIDO'].sum().reset_index()
    
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