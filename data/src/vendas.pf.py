# BIBLIOTECAS ESSENCIAIS

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

"""Modulos necessários do Python
- Pandas
- Numpy
- Matplotlib
- Seaborn
- Os

"""

"""SCRIPT DE ETL E LIMPEZA DE DADOS 
Objetivo: Análise Exploratória da base vendas.pf seguindo etapas claras, documentadas e reproduzíveis.

- Renomear colunas para nomes mais amigáveis (ex.: "CUST_ID" para "ID_CLIENTE", "CUST_FIRST_NAME" para "NOME_CLIENTE", "CUST_GENDER" para "GENERO_CLIENTE", "COUNTRY_ID" para "ID_PAIS", " COUNTRY_NAME" para "PAIS", "CUST_CITY" para "CIDADE", "CUST_CITY_ID" para "ID_CIDADE", "CUST_VALID" para "CLIENTE_ATIVO", "PROD_ID" para "ID_PRODUTO", "CHANNEL_ID" para "ID_CANAL", "QUANTITY_SOLD" para "QUANTIDADE_VENDIDA", "AMOUNT_SOLD" para "VALOR_VENDIDO", "TIME_ID" para "DATA");
- Eliminar clientes inválidos/inativos, sendo • A: Significa Ativo (Active) ou Aprovado./• I: Significa Inativo (Inactive) ou Inválido,
determinado pela coluna "CUST_VALID";
- Eliminar duplicatas relevantes, considerando duplicatas quando o mesmo cliente comprou na mesma data, o mesmo produto (ex.: mesmo cliente comprando o mesmo produto no mesmo dia, indicando possível erro de digitação ou registro duplicado, o que pode distorcer análises de vendas e comportamento do consumidor);
- Ajustar tipos de dados (ex.: converter coluna DATA para datetime).
- Gerar estatísticas descritivas básicas para coluna de número de valor vendido (média; mediana; desvio padrão; moda; máximo; mínimo e contagem).
- Explorar padrões de agrupamento com pelo menos dois agrupamentos (por exemplo: gênero com mais vendas, compras), usando groupby().
- Salvar o DataFrame limpo ('query_valida') como CSV."""
 
print("Carregamento de dados(extração)")

# ============================================================
# 1. CARREGAMENTO DOS DADOS (EXTRATAÇÃO)
#    Objetivo: Importar a base bruta (raw) e informações iniciais sobre os dados.
# ============================================================
 
caminho_entrada = r"C:\Users\ANDREZA\Desktop\Projeto_Final_AndrezaCordeiro_QA VDBI 20261 2\data\raw\vendas.pf.csv"

# Ignorar esse texto '#N/D' e transformá-lo em um valor nulo/em branco (representado por NaN)
vendas_csv = pd.read_csv(caminho_entrada, na_values=['#N/D'])

print("Informações sobre os dados:")

# Mostrar quantos registros foram exportados
print("Quantidade de registros exportados:", len(vendas_csv))
# Verificar o número de linhas e colunas
print(vendas_csv.shape)
# Verificar os tipos de dados
print(vendas_csv.dtypes)
# Mostrar as primeiras linhas do DataFrame
print(vendas_csv.head())
# Mostrar informações gerais sobre o DataFrame
print(vendas_csv.info())
# Exibe o cabeçalho de cada coluna
print(vendas_csv.columns)


# ============================================================
# 2. SANEAMENTO FILTRAGEM E IMPUTAÇÃO DE DADOS
# ============================================================

print("[Etapa 2] Estimando porcentagem de valores nulos, remoção de duplicatas, ajustando tipos de dados e renomear colunas.")
# Percentual de nulos por coluna


def calcular_percentual_nulos(vendas_csv):
    percentual_nulos = vendas_csv.isnull().mean() * 100
    return percentual_nulos


percentual_nulos = calcular_percentual_nulos(vendas_csv)
print("Percentual de valores nulos por coluna:")
print(percentual_nulos)

# Ordenando do maior para o menor
percentual_nulos = percentual_nulos.sort_values(ascending=False)
print("Percentual de valores ausentes por coluna:")
print(percentual_nulos.round())

print("Nulos restantes:", vendas_csv.isnull().sum())

# Remoção de duplicatas parcial e inativos: mesmo cliente "comprando o mesmo produto no mesmo dia, indicando possível erro de digitação ou registro duplicado, o que pode distorcer análises de vendas e comportamento do consumidor)"*******************

def print_duplicatas(vendas_csv):
    print(f"Linhas antes: {len(vendas_csv)}")
    vendas_csv_sem_dup_parcial = vendas_csv.drop_duplicates(
        subset=["CUST_ID", "CUST_FIRST_NAME", "CUST_GENDER", "COUNTRY_ID", "COUNTRY_NAME", "CUST_CITY", "CUST_CITY_ID", "CUST_VALID", "PROD_ID", "CHANNEL_ID", "QUANTITY_SOLD", "AMOUNT_SOLD", "TIME_ID"],
        keep="first"
    )
    print(f"Linhas depois: {len(vendas_csv_sem_dup_parcial)}")
    return vendas_csv_sem_dup_parcial  

    vendas_csv_sem_dup_parcial = print_duplicatas('vendas_csv')


# Converte a coluna 'Data' para formato datetime considerando dia primeiro
vendas_csv['TIME_ID'] = pd.to_datetime(vendas_csv['TIME_ID'], errors='coerce')                            

# Converte para o formato de texto brasileiro (DD/MM/AAAA)
vendas_csv['TIME_ID'] = vendas_csv['TIME_ID'].dt.strftime('%d/%m/%Y')

# Exibir para conferir como ficou
print(vendas_csv[['TIME_ID']].head())

print("Tipos de dados após ajuste:")
print(vendas_csv.dtypes)

# Filtrar para manter apenas os clientes onde CUST_VALID é diferente de 'I' (inválido/inativo). Isso garante que apenas clientes ativos sejam considerados na análise.
df_filtrado = vendas_csv[vendas_csv['CUST_VALID'] != 'I']

# Exibir quantas linhas restaram
print(f"Linhas restantes: {len(df_filtrado)}")

df_filtrado.columns= df_filtrado.columns.str.strip()

# Renomear colunas específicas usando um dicionário
df= df_filtrado.rename(columns={
    'CUST_ID': 'ID_CLIENTE',
    'CUST_FIRST_NAME': 'NOME_CLIENTE',
    'CUST_GENDER': 'GENERO_CLIENTE',
    'COUNTRY_ID': 'ID_PAIS',
    'COUNTRY_NAME': 'PAIS',
    'CUST_CITY': 'CIDADE',
    'CUST_CITY_ID': 'ID_CIDADE',
    'CUST_VALID': 'CLIENTE_ATIVO',
    'PROD_ID': 'ID_PRODUTO',
    'CHANNEL_ID': 'ID_CANAL',
    'QUANTITY_SOLD': 'QUANTIDADE_VENDIDA',
    'AMOUNT_SOLD': 'VALOR_VENDIDO',
    'TIME_ID': 'DATA'
})



# Exibir os novos nomes das colunas
print("Colunas atualizadas com sucesso:", df.columns.tolist())

df = df.replace('Germany', 'Alemanha')

# Salvar o resultado em um novo arquivo CSV
df.to_csv('query_valida.csv', index=False)

"""
SCRIPT E ORGANIZAÇÃO PARA ANÁLISE DE DADOS
Objetivo:
- Identificar qual genero tem maior valor de vendas;
- Identificar possíveis outliers no valor de vendas por gênero;
- Analisar a distribuição de vendas entre os canais de venda.

 Imputar dados para análise de distribuição de vendas.
    - Dados extraídos no Oracle por consulta SQL, utilizando o arquivo Sales History (SH) de domínio público.
    - Já limitando a extração para dados de um país específico "Germany" (Alemanha);
    - Dados ordenados por data de venda "time_id" de forma ascendente;
    - Retirando o canal de venda "channel_id" = 2, devido não fazer parte da análise.
"""

# ============================================================
# 3. ESTATÍSTICAS DESCRITIVAS 
# ============================================================

print("[Etapa 3] Estatísticas descritivas para a coluna 'VALOR_VENDIDO':")


# Renomeia a coluna original 'AMOUNT_SOLD' para 'VALOR_VENDIDO' para manter consistência com o restante do código.
vendas_csv = vendas_csv.rename(columns={'AMOUNT_SOLD': 'VALOR_VENDIDO'})


print("Média:", vendas_csv['VALOR_VENDIDO'].mean())
print("Mediana:", vendas_csv['VALOR_VENDIDO'].median())
print("Desvio Padrão:", vendas_csv['VALOR_VENDIDO'].std())
print("Moda:", vendas_csv['VALOR_VENDIDO'].mode()[0]if not vendas_csv['VALOR_VENDIDO'].mode().empty else "Sem moda")   # A moda pode retornar mais de um valor, pegamos o primeiro
print("Máximo:", vendas_csv['VALOR_VENDIDO'].max())
print("Mínimo:", vendas_csv['VALOR_VENDIDO'].min())
print("Contagem:", vendas_csv['VALOR_VENDIDO'].count())  # Contagem de valores não nulos


# Total de número de vendas por genero.
print("Total em valor vendido por gênero:")

# Vendas por gênero

def contar_vendas_por_genero(df):
    vendas_por_genero = df.groupby('GENERO_CLIENTE')['VALOR_VENDIDO'].sum()
    return vendas_por_genero

resultado_genero = contar_vendas_por_genero(df)
print(resultado_genero)
print("-" * 40)


# Função de vendas por canal (corrigido para agrupar por 'ID_CANAL')
def contar_vendas_por_canal(df):
    # Agrupa pelo canal e conta os registros, ordenando do maior para o menor
    vendas_por_canal = df.groupby('ID_CANAL')['VALOR_VENDIDO'].count().sort_values(ascending=False)
    return vendas_por_canal

vendas_por_canal = contar_vendas_por_canal(df)
print("Quantidade de vendas por canal:")
print(vendas_por_canal)
print("-" * 40)


# Função de variações de canal por data (corrigida a ordem do sort e nome da variável)
def contar_variacoes_de_canal_por_datas(df):
    # Primeiro ordena do maior para o menor, depois pega os 10 primeiros (.head(10))
    variacoes_de_canal_por_datas = df.groupby('DATA')['ID_CANAL'].count().sort_values(ascending=False).head(10)
    return variacoes_de_canal_por_datas

# Salvando o resultado em uma variável com nome diferente da função
resultado_canal_datas = contar_variacoes_de_canal_por_datas(df)
print("Total de variações de canal por datas:")
print(resultado_canal_datas)


# ============================================================
# 4. CARREGAMENTO DOS DADOS (EXTRATAÇÃO) E ANÁLISE GRÁFICA
#    Objetivo: Importar a base query_valida.
# ============================================================

print("Iniciando o processo de análise dados da query_valida.")

caminho_entrada = "query_valida.csv"
query_valida = pd.read_csv(caminho_entrada)


# Executa diagnóstico estrutural inicial simplificado
print("\n--- Estrutura Inicial da Base ---")
query_valida.info()

print("\n--- Shape da Base - Quantidade de Linhas e Colunas ---")
print(query_valida.shape)

print("\n--- Visualização das primeiras linhas ---")
print(query_valida.head(5))

print("\n--- Calcular medidas estatísticas básicas ---")
print(query_valida.describe())

# Garante que a pasta de imagens existe
os.makedirs(r"output\\imagens", exist_ok=True)


# =======================================
# BOXPLOT — Análise de Valor de Vendas por Gênero de Clientes
# =======================================
plt.figure(figsize=(8, 5))

sns.boxplot(data = query_valida, y ="GENERO_CLIENTE", x="VALOR_VENDIDO", color="lightblue")

plt.title("Boxplot do genero de clientes")
plt.ylabel("Gênero do Cliente")
plt.tight_layout()

plt.savefig(
    r"output\\imagens\\boxplot_genero_clientes.png",
    dpi=150, bbox_inches="tight"
)
plt.show()
plt.close()



# ==========================================
# HISTOGRAMA — Distribuição do valor de vendas por canal de venda
# ==========================================
plt.figure(figsize=(8, 5))

sns.histplot(data=query_valida, x="VALOR_VENDIDO", hue="ID_CANAL", kde=True, element="step", # Mantém apenas a borda, reduzindo a poluição visual
    palette="Set2", multiple="layer",
    alpha=0.3     # Transparência para ver onde as distribuições se cruzam
)
plt.title("Distribuição do Valor vendido por Canal")
plt.xlabel("Valor Vendido")
plt.ylabel("Quantidade de Vendas por Canal")
plt.tight_layout()

plt.savefig(
    r"output\\imagens\\histograma_valor_vendas_canal.png",
    dpi=150, bbox_inches="tight"
)
plt.show()
plt.close()

# ==========================================
# DICIONÁRIO DE MAPEAMENTO E ETL
# ==========================================

plt.savefig(
    r"output\\imagens\\dicionario_mapeamento_etl.png",
    dpi=150, bbox_inches="tight"
)
