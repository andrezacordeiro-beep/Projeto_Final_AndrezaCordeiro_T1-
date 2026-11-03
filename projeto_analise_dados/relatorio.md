
Relatório de Projeto: Análise de Vendas Empresa Desconhecida- Alemanha (2019)

Este relatório sintetiza o desenvolvimento, a implementação técnica e a documentação do projeto final de análise de dados, integrando um pipeline robusto de ETL, um painel interativo em Streamlit e diretrizes profissionais de documentação.

1. Resumo Executivo
   Domínio dos Dados: Análise de vendas de um conjunto de dados da Alemanha referente ao ano de 2019, com valores padronizados em Euros (€).

Objetivo: Fornecer uma ferramenta interativa e reprodutível para a exploração de faturamento, comportamento de canais de venda e identificação de outliers.

Stack Tecnológico: Python, Pandas, NumPy, Plotly, Streamlit e Git/Markdown.

2. Arquitetura de ETL e Tratamento de Dados
   O processo de extração, transformação e carga (ETL), implementado no script de saneamento, garantiu a integridade analítica da base através de:

Mesclagem de Bases: Combinação da tabela de vendas com a tabela de canais (CHANNEL_ID) para enriquecer o contexto analítico.

Limpeza e Saneamento:

Tratamento de valores nulos e remoção de registos inválidos com base na coluna de validação de clientes (CUST_VALID).

Eliminação de duplicatas parciais (compras duplicadas do mesmo cliente, produto e data).

Padronização Temporal: Conversão rigorosa da coluna de datas (TIME_ID para DATA) utilizando o formato europeu (dayfirst=True) e normalização para evitar conflitos de tipos no front-end.

3. Painel Interativo (Streamlit)
   O aplicativo web (app.py) foi desenvolvido seguindo boas práticas de usabilidade e performance:

Otimização de Carregamento: Utilização de @st.cache_data para assegurar uma performance fluida no carregamento da base tratada (query_valida.csv).

Filtros Dinâmicos: Barra lateral interativa contendo seleção de canais de venda e data inicial com suporte a objetos de data nativos.

Perspectivas Gráficas (Plotly):

Evolução Temporal (Linha): Acompanhamento diário das vendas por canal.

Distribuição Mensal (Barras): Agrupamento do faturamento total por mês/ano.

Análise de Dispersão (Boxplot): Identificação visual de outliers e comportamento estatístico dos valores vendidos.

4. Documentação e Boas Práticas do Repositório
   Documentação Visual (README.md): Estruturação completa com introdução, instruções de execução, arquitetura e incorporação correta de recursos visuais (utilizando caminhos relativos e formatação Markdown/HTML).

Controle de Versão (.gitignore): Configuração para exclusão de ficheiros brutos locais, bases processadas pesadas e diretórios de saída de imagens temporárias (output/), garantindo um repositório limpo e focado no código-fonte.
