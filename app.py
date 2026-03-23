import streamlit as st

from src.styles import APP_CSS
from src.data_loader import load_data, load_configs, load_payments
from src.tabs.overview import render_overview
from src.tabs.credit_cards import render_credit_cards

# Configuração da página
st.set_page_config(
    page_title="Personal Finance Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Aplicar estilos
st.markdown(APP_CSS, unsafe_allow_html=True)

# Carregar dados
try:
    df = load_data()
    configs_df = load_configs()
    payments_df = load_payments()
except FileNotFoundError as e:
    st.error(f"Arquivo de dados não encontrado: {e}")
    st.stop()

# --- HEADER ---
st.title("🏦 Dashboard Financeiro Principal")
st.markdown("Gestão consolidada de despesas.")

# --- TABS ---
tab_overview, tab_cards = st.tabs(["📊 Visão Geral", "💳 Cartões de Crédito"])

with tab_overview:
    render_overview(df)

with tab_cards:
    render_credit_cards(df, configs_df, payments_df)

# --- FOOTER ---
st.divider()
st.markdown("<p style='text-align:center; color:#64748B; font-size:0.8em; margin-top:-10px'>* Valores em Dólar Canadense</p>", unsafe_allow_html=True)
