# 🏦 Personal Finance Analytics Dashboard

Dashboard financeiro moderno e intuitivo construído com **Streamlit**, projetado para fornecer uma visão consolidada e clara das despesas pessoais, com foco em gestão de faturas e análise de gastos.

## 🚀 Funcionalidades

- **📊 Visão Geral**: KPIs em tempo real (Gasto Total, Crédito, Débito) e resumos por categoria.
- **📈 Análise Temporal**: Gráficos de tendência diária e semanal para acompanhar gastos variáveis e eventuais.
- **💳 Faturas Atuais**: Controle específico para faturas de cartões de crédito (TD e RBC), com cálculo automático baseado em períodos de fechamento configuráveis.
- **🔍 Filtros Globais**: Filtragem dinâmica por mês e por banco em todas as visualizações.
- **🎨 Design Premium**: Interface limpa com estética de fintech, incluindo logos das instituições e visualização otimizada para web.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: [Python](https://www.python.org/)
- **Framework Web**: [Streamlit](https://streamlit.io/)
- **Processamento de Dados**: [Pandas](https://pandas.pydata.org/)
- **Visualização**: [Plotly](https://plotly.com/python/)
- **Estilização**: CSS Customizado (Fintech Aesthetic)

## ⚙️ Configuração e Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Pip (gerenciador de pacotes)

### Passo a Passo

1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd personal_finance
   ```

2. **Crie e ative um ambiente virtual (recomendado)**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No macOS/Linux
   ```

3. **Instale as dependências**:
   ```bash
   pip install streamlit pandas plotly
   ```

4. **Prepare os arquivos de dados**:
   Certifique-se de que os arquivos CSV estão na pasta `data/`:
   - `finance_2026 - TRANSACTIONS.csv`: Registro de todas as transações.
   - `finance_2026 - CONFIGS.csv`: Configurações de datas de abertura/fechamento de faturas.

5. **Execute a aplicação**:
   ```bash
   streamlit run app.py
   ```

## 📂 Estrutura do Projeto

```
personal_finance/
├── app.py                      # Entrypoint da aplicação Streamlit
├── src/
│   ├── styles.py               # Constantes de CSS (estética fintech)
│   ├── data_loader.py          # Carregamento de dados, constantes de gráficos
│   └── tabs/
│       ├── overview.py         # Aba "Visão Geral" (KPIs, resumos, gráficos)
│       └── credit_cards.py     # Aba "Cartões de Crédito" (faturas TD e RBC)
├── data/                       # Arquivos CSV de transações e configurações
├── imgs/                       # Assets visuais (logos TD e RBC)
└── .venv/                      # Ambiente virtual do Python
```