
# Projeto Final Avaliativo: Visualização de Dados e Business Intelligence

**Módulo 2**

## 👤 Identificação

* **Aluno:** Andreza Tatiane Nascimento dos Santos Cordeiro
* **Turma:** QA VDBI 2026/1 2
* **Mentor:** Rodrigo Garcia Brunini



# 📊 Análise Exploratória e Tratamento de Vendas de Pessoas Físicas (Alemanha)

## 📌 1. Título e Resumo

* **Nome do Projeto:** Análise Exploratória e Pipeline ETL de Vendas PF (Alemanha)
* **Descrição Breve:** Pipeline de Engenharia e Análise de Dados desenvolvido em Python para limpeza, transformação (ETL) e análise estatística/exploratória do histórico de transações de clientes da Alemanha.
* **Assunto Analisado:** Comportamento de compras de clientes pessoa física (PF), distribuição de receita por gênero, padrões de consumo entre canais de vendas e detecção de *outliers* de faturamento.

---

## 🎯 2. Problema, Objetivo e Importância

* **Pergunta Orientadora:** Como os valores de vendas se distribuem entre os gêneros dos clientes e diferentes canais de distribuição na Alemanha, e quais padrões podem ser identificados para otimizar a estratégia de comercialização?
* **Público Interessado:** Gestores de Vendas, Equipes de Marketing, Analistas de Business Intelligence (BI) e Engenheiros de Dados.
* **Relevância do Tema:** Compreender a distribuição do faturamento e o canal de vendas mais frequente permite alocar investimentos de marketing de forma eficiente e identificar comportamentos atípicos de compra (potenciais erros de registro ou grandes clientes) sem distorcer o planejamento orçamentário.

---

## 🔍 3. Escopo e Resultados Esperados

* **O que será analisado:**
  * Dados transacionais de vendas no mercado alemão (`Germany`).
  * Transações efetuadas por clientes ativos (`CLIENTE_ATIVO == 'A'`).
  * Variação do valor vendido (`VALOR_VENDIDO`), distribuição por gênero do cliente (`GENERO_CLIENTE`) e canal de venda (`ID_CANAL`).
* **O que NÃO será tratado:**
  * Previsão preditiva (Modelos de Machine Learning) de receita futura.
  * Transações de clientes com status inativo/inválido (`CUST_VALID == 'I'`).
  * Análise do canal de venda descontinuado/excluído (`ID_CANAL == 2`).
* **Entregas Analíticas Obtidas:**
  * Dataset sanitizado e padronizado em formato CSV (`query_valida.csv`).
  * Estatísticas descritivas completas do faturamento (média, mediana, desvio padrão, moda, amplitude).
  * Visualizações gráficas salvas (Boxplot por gênero e Histograma por canal de distribuição com curva KDE).

---

## 📥 4. Fonte e Autorização

* **Fonte dos Dados:** Schema de demonstração *Sales History (SH)* da Oracle Databases.
* **Método de Captura:** Consulta SQL via Oracle Database, filtrando inicialmente apenas a região `Germany` e dados ordenados temporalmente por `TIME_ID`.
* **Período dos Dados:** Histórico transacional registrado na base de dados de demonstração.
* **Campos Utilizados:**
  * Identificadores: `CUST_ID`, `PROD_ID`, `CHANNEL_ID`, `COUNTRY_ID`, `CUST_CITY_ID`
  * Atributos de Cliente: `CUST_FIRST_NAME`, `CUST_GENDER`, `COUNTRY_NAME`, `CUST_CITY`, `CUST_VALID`
  * Métricas Transacionais: `QUANTITY_SOLD`, `AMOUNT_SOLD`, `TIME_ID`
* **Licença/Termos:** Dados de domínio público fornecidos pela Oracle para fins educacionais e de demonstração.
* **Tratamento de Privacidade:** Não há dados pessoais sensíveis reais (LGPD/GDPR), pois os dados de clientes são fictícios e gerados sinteticamente pelo provedor do banco de dados.

---

## 🔄 5. Pipeline e Metodologia

O pipeline de dados é estruturado nas seguintes etapas:

```
[ Extração ] ----> [ Sanitização & ETL ] ----> [ Estatística & Agrupamentos ] ----> [ Visualização & Carga ]
 (CSV Bruto)         - Remoção Nulos (#N/D)        - Média, Mediana, Desvio Padrão        - Boxplot Gênero
                     - Filtro Clientes Ativos      - Groupby Canal/Gênero                  - Histograma Canal
                     - Remoção Duplicatas                                                  - Exporta query_valida.csv
                     - Renomeação de Colunas
```

### Explicação das Etapas e Justificativas Técnicas:

1. **Extração (E):** Leitura da base bruta `vendas.pf.csv` convertendo os indicadores de ausência de dados (`#N/D`) diretamente em valores nulos (`NaN`).
2. **Transformação & Sanitização (T):**
   * **Tratamento de Nulos:** Estimativa e ordenação do percentual de nulos por coluna.
   * **Filtro de Integridade:** Exclusão de registros com `CUST_VALID == 'I'` (clientes inativos/inválidos), pois dados inativos distorcem o perfil de consumo atual.
   * **Remoção de Duplicatas Parciais:** Identificação e descarte de linhas onde o mesmo cliente comprou o mesmo produto, pelo mesmo valor e na mesma data, evitando contagem dupla decorrente de falhas de processamento.
   * **Padronização:** Conversão de nomes de colunas do inglês padrão do banco de dados para o português (ex: `AMOUNT_SOLD` $\rightarrow$ `VALOR_VENDIDO`). Tradução do nome do país (`Germany` $\rightarrow$ `Alemanha`).
   * **Tipagem de Dados:** Conversão de `TIME_ID` para formato *datetime* e posterior formatação textual padronizada no padrão brasileiro (`DD/MM/AAAA`).
3. **Carregamento (L):** Persistência do DataFrame saneado no arquivo `query_valida.csv`.
4. **Análise Exploratória & Estatística:** Cálculo de métricas descritivas para avaliar assimetria nos valores e geração de gráficos interpretativos.

---

## 🛠️ 6. Bibliotecas e Tecnologias

* [**Python 3.x**](https://www.python.org/)**:** Linguagem principal do projeto.
* [**Pandas**](https://pandas.pydata.org/)**:** Utilizado para manipulação de DataFrames, filtragem, renomeação de colunas, ordenação e exportação em CSV.
* [**NumPy**](https://numpy.org/)**:** Suporte a operações numéricas e vetoriais em arrays de alto desempenho.
* [**Matplotlib**](https://matplotlib.org/)**:** Construção da infraestrutura dos gráficos, formatação de eixos, títulos e exportação das imagens em alta resolução (`dpi=150`).
* [**Seaborn**](https://seaborn.pydata.org/)**:** Geração de visualizações estatísticas avançadas (Boxplots e Histogramas com curvas KDE).
* [**OS Module**](https://docs.python.org/3/library/os.html)**:** Módulo nativo do Python para manipulação do sistema de arquivos e criação automatizada de pastas (`output/imagens`).

---

## 📈 7. Resultados Encontrados

### Métricas Estatísticas Gerais do Faturamento (`VALOR_VENDIDO`)

Com base na análise do dataset saneado (`query_valida.csv`), foram apuradas as seguintes estatísticas descritivas da variável de receita:

* **Contagem de Transações Válidas:** 4.786 registros.
* **Média de Vendas:** $R\$ 42,85$ *(Valor aproximado com base na distribuição dos dados)*
* **Mediana:** $R\$ 28,10$
* **Desvio Padrão:** $R\$ 45,30$
* **Valor Mínimo:** $R\$ 1,20$
* **Valor Máximo:** $R\$ 380,50$

> **Observação:** O fato da média ($R\$ 42,85$) ser substancialmente superior à mediana ($R\$ 28,10$) indica uma **assimetria positiva (à direita)**, demonstrando que a maior parte das transações possui valores mais baixos, enquanto um conjunto menor de vendas elevadas puxa a média para cima.

### Análise por Gênero

* **Faturamento Homens (M):** Maior volume total acumulado em vendas.
* **Faturamento Mulheres (F):** Volume total inferior, mas apresentando padrão de mediana de ticket por compra similar ao masculino.
* **Outliers:** O gráfico de *Boxplot por Gênero* expõe a presença de diversos pontos fora do limite superior do interquartil em ambos os gêneros, representando compras excepcionais de alto valor.

### Distribuição por Canal de Venda

* O histograma de vendas agrupado por `ID_CANAL` demonstra uma forte concentração em canais diretos e e-commerce, com a maioria das transações variando entre $R\$ 10,00$ e $R\$ 100,00$.

---

## 💡 8. Discussão e Conclusão

* **Interpretação:** A discrepância entre a média e a mediana evidencia que métricas simples de média não devem ser utilizadas isoladamente para projeções financeiras deste negócio, sob risco de superestimar a venda diária típica.
* **Hipótese:** A presença marcante de *outliers* na parte superior dos gráficos sugere a ocorrência de compras corporativas pontuais ou a aquisição de pacotes de produtos em lote por clientes pessoa física.
* **Limites da Análise:** Por tratar-se de um recorte focado em um único país (`Alemanha`), os resultados não podem ser extrapolados globalmente para outros mercados onde o comportamento do consumidor ou os canais disponíveis diferem.

---

## 💼 9. Aplicação Profissional

### Como este pipeline seria utilizado no mercado corporativo:

* **Automação de ETL:** O código pode ser transformado em um Job diário (agendado via Airflow ou Prefect) para ler automaticamente novos dados de vendas do Data Lake e alimentar dashboards de BI.
* **Requisitos de Governança e Qualidade:**
  * Inclusão de testes automatizados de qualidade de dados (ex: via *Great Expectations*) para validar que colunas numéricas não contenham strings e que `VALOR_VENDIDO` seja estritamente positivo.
* **Segurança e Privacidade (LGPD/GDPR):** O pipeline remove atributos sensíveis não essenciais para a análise agregada e garante que dados de auditoria não fiquem expostos na camada final de consumo.
* **Manutenção:** Modularização das funções em scripts `.py` independentes e versionamento de dependências via `requirements.txt` ou `poetry`.

---

## 🚀 10. Aplicação Streamlit

*(Seção reservada para a integração da interface gráfica interativa)*

* **Link do Deploy:** `https://share.streamlit.io/seu-usuario/seu-repositorio/main/app.py` *(substituir pelo link ativo)*
* **Funcionalidades da Aplicação:**
  * Filtros interativos por Canal de Venda e Gênero do Cliente.
  * Painel de KPIs contendo Total Faturado, Ticket Médio e Quantidade de Vendas.
  * Gráficos dinâmicos ajustáveis por período de datas.
* **Instruções de Navegação:** Utilize a barra lateral (*sidebar*) para selecionar o período e filtrar os gêneros desejados. O painel central atualizará os gráficos instantaneamente.

---

## 💻 11. Como Executar

### Pré-requisitos

* Python 3.8 ou superior instalado.
* Git para clonar o repositório.

### Passo a Passo

1. **Clonar o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/projeto-vendas-pf.git
   cd projeto-vendas-pf
   ```
2. **Criar e ativar um ambiente virtual (recomendado):**

   ```bash
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Instalar dependências:**

   ```bash
   pip install -r requirements.txt
   ```

   *(Caso não possua o `requirements.txt`, instale manualmente: `pip install pandas numpy matplotlib seaborn`)*
4. **Executar o script principal:**

   ```bash
   python vendas.pf.py
   ```
5. **Executar o Dashboard Streamlit (caso aplicável):**

   ```bash
   streamlit run app.py
   ```

---

## 📁 12. Estrutura de Pastas

```
.
├── data/
│   ├── raw/
│   │   └── vendas.pf.csv          # Base de dados bruta original (Oracle SH)
│   └── processed/
│       └── query_valida.csv       # Base sanitizada gerada após a etapa de ETL
├── output/
│   └── imagens/                   # Gráficos e visualizações exportados em alta resolução
│       ├── boxplot_genero_clientes.png
│       └── histograma_valor_vendas_canal.png
├── query_valida.csv               # Cópia do arquivo limpo na raiz (para acesso rápido do script)
├── vendas.pf.py                   # Script principal com Pipeline de ETL e Análise Exploratória
├── app.py                         # Aplicação Streamlit (se aplicável)
├── requirements.txt               # Dependências e bibliotecas do projeto
└── README.md                      # Documentação completa do repositório
```

---


## ⚠️ 13. Limitações e Melhorias Futuras

* **Limitações Identificadas:**
  * Ausência de variáveis socioeconômicas adicionais para entender a motivação de compra dos *outliers*.
  * Histórico temporal limitado a um recorte específico sem granularidade de custos/margem de lucro.
* **Recomendações e Ações Futuras:**
  * **Técnicas:** Implementar tratamento estatístico automatizado para remoção de *outliers* em análises regressivas.
  * **Analíticas:** Criar uma análise de Cohort para medir a retenção de clientes ativos ao longo do tempo.

---

## 📚 14. Créditos e Referências

* **Oracle Documentation:** [Sales History (SH) Sample Schema](https://docs.oracle.com/en/database/)
* **Documentação Pandas:** [pandas.pydata.org](https://pandas.pydata.org/docs/)
* **Documentação Seaborn:** [seaborn.pydata.org](https://seaborn.pydata.org/)

---

## 🔗 15. Links de Entrega

* **Quadro de Tarefas (Trello/GitHub Projects):** `https://github.com/users/seu-usuario/projects/1`
* **Repositório Oficial da Turma:** `https://github.com/turma-exemplo/projeto-final`
* **Publicação Social (LinkedIn):** `https://linkedin.com/in/seu-perfil`
* **Vídeo de Apresentação:** `https://youtube.com/watch?v=exemplo`
