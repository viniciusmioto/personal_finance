import streamlit as st
import pandas as pd
import base64

# Chart color constants
CHART_COLOR_PRIMARY = '#1D4ED8'    # Blue
CHART_COLOR_SECONDARY = '#0EA5E9'  # Light Blue
CHART_COLOR_TERTIARY = '#10B981'   # Green
FONT_FAMILY = "sans-serif"


@st.cache_data
def load_data():
    df = pd.read_csv('data/finance_2026 - TRANSACTIONS.csv')
    df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y')
    # Clean the VALOR column: remove $, and convert to float
    if df['VALOR'].dtype == 'O':
        df['VALOR'] = df['VALOR'].replace(r'[\$,]', '', regex=True).astype(float)
        
    # Extração de dias da semana e semanas para gráficos temporais
    df['SEMANA'] = df['DATA'].dt.isocalendar().week
    # Pandas dayofweek is 0-Monday, 6-Sunday
    dias = {0: 'Seg', 1: 'Ter', 2: 'Qua', 3: 'Qui', 4: 'Sex', 5: 'Sáb', 6: 'Dom'}
    df['DIA_SEMANA'] = df['DATA'].dt.dayofweek.map(dias)
    
    # Extração do Mês p/ filtro (ex: '2026-02')
    df['MES_STR'] = df['DATA'].dt.strftime('%m/%Y')
    
    return df


@st.cache_data
def load_configs():
    configs = pd.read_csv('data/finance_2026 - CONFIGS.csv')
    # Convert dates
    date_cols = ['open_td', 'close_td', 'due_td', 'open_rbc', 'close_rbc', 'due_rbc']
    for col in date_cols:
        configs[col] = pd.to_datetime(configs[col], format='%d/%m/%Y')
    # Ensure limits are numeric (handling currency symbols if present)
    for col in ['limit_td', 'limit_rbc']:
        if configs[col].dtype == 'O':
            configs[col] = configs[col].replace(r'[\$,]', '', regex=True).astype(float)
        configs[col] = pd.to_numeric(configs[col])
    return configs


@st.cache_data
def load_payments():
    payments = pd.read_csv('data/finance_2026 - PAYMENTS.csv')
    payments['DATA'] = pd.to_datetime(payments['DATA'], format='%d/%m/%Y')
    if payments['VALOR'].dtype == 'O':
        payments['VALOR'] = payments['VALOR'].replace(r'[\$,]', '', regex=True).astype(float)
    return payments


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
