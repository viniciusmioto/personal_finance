import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64

# Configuração da página - Aesthetic Fintech (Profissional, Limpo, Confiável)
st.set_page_config(
    page_title="Personal Finance Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilização Fintech com CSS (Cores: Slate, Navy, Green/Red for values)
st.markdown("""
    <style>
    .main {
        background-color: #F8FAFC;
    }
    .metric-card {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.1);
        border: 1px solid #E2E8F0;
        margin-bottom: 16px;
    }
    .invoice-card {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
    }
    .invoice-info {
        display: flex;
        flex-direction: column;
    }
    .invoice-value {
        font-size: 2.5em; /* Matches stMetricValue */
        font-weight: 700;
        color: #0F172A;
        margin: 8px 0;
    }
    .invoice-label {
        font-size: 0.875rem; /* Matches stMetricLabel (14px) */
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .invoice-period {
        font-size: 0.85em;
        color: #94A3B8;
    }
    /* Mobile First Adjustments */
    @media (max-width: 640px) {
        .invoice-card {
            flex-direction: column;
            align-items: flex-start;
        }
        .invoice-logo {
            margin-top: 16px;
            align-self: flex-end;
        }
    }
    .stTable {
        background-color: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.1);
    }
    h1, h2, h3 {
        color: #0F172A;
        font-weight: 600;
    }
    p {
        color: #334155;
    }
    .stMetric {
        background-color: white !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.1) !important;
        border: 1px solid #E2E8F0;
    }
    [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 2.5em !important;
    }
    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        border-bottom-color: #1D4ED8;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

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
    # Only 1 row expected
    configs = pd.read_csv('data/finance_2026 - CONFIGS.csv').iloc[0]
    return {
        'open_td': pd.to_datetime(configs['open_td'], format='%d/%m/%Y'),
        'close_td': pd.to_datetime(configs['close_td'], format='%d/%m/%Y'),
        'open_rbc': pd.to_datetime(configs['open_rbc'], format='%d/%m/%Y'),
        'close_rbc': pd.to_datetime(configs['close_rbc'], format='%d/%m/%Y'),
    }

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    df = load_data()
    configs = load_configs()
except FileNotFoundError as e:
    st.error(f"Arquivo de dados não encontrado: {e}")
    st.stop()

# --- HEADER ---
st.title("🏦 Dashboard Financeiro Principal")
st.markdown("Gestão consolidada de despesas.")

# Filtros Globais (Mês e Banco afetam a Visão Geral)
col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    meses_disponiveis = sorted(df['MES_STR'].unique().tolist(), reverse=True)
    mesos_opcoes = ["Todos"] + meses_disponiveis
    mes_selecionado = st.selectbox("Selecione o Mês:", mesos_opcoes)

with col_filter2:
    bancos_disponiveis = df['BANCO'].dropna().unique().tolist()
    bancos_opcoes = ["Todos"] + sorted(bancos_disponiveis)
    banco_selecionado = st.selectbox("Filtro por Banco:", bancos_opcoes)


# Aplicar filtros apenas nas views da aba "Visão Geral"
df_filtered = df.copy()
if mes_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered['MES_STR'] == mes_selecionado]
if banco_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered['BANCO'] == banco_selecionado]

# TABS
tab_overview, tab_invoices = st.tabs(["📊 Visão Geral", "💳 Faturas Atuais"])

# ==============================================================================
# ABA: VISÃO GERAL
# ==============================================================================
with tab_overview:
    # --- KPIs ---
    total_expense = df_filtered['VALOR'].sum()
    transaction_count = len(df_filtered)
    total_credit = df_filtered[df_filtered['PAGAMENTO'] == 'Crédito']['VALOR'].sum()
    total_debit = df_filtered[df_filtered['PAGAMENTO'] == 'Débito']['VALOR'].sum()
    
    col1, col2, col3, = st.columns(3)
    
    with col1:
        st.metric(label="Gasto Total", value=f"$ {total_expense:,.2f}")
    
    with col2:
        st.metric(label="Total Crédito", value=f"$ {total_credit:,.2f}")
    
    with col3:
        st.metric(label="Total Débito", value=f"$ {total_debit:,.2f}")
        
    st.divider()
    
    # Banking Styling
    CHART_COLOR_PRIMARY = '#1D4ED8' # Blue
    CHART_COLOR_SECONDARY = '#0EA5E9' # Light Blue
    CHART_COLOR_TERTIARY = '#10B981' # Green
    FONT_FAMILY = "sans-serif"
    
    # 1. Resumo
    st.markdown("#### Resumo")
    if not df_filtered.empty:
        summary_cat = df_filtered.groupby('CATEGORIA').agg(
            Valor=('VALOR', 'sum'),
            Transações=('VALOR', 'count')
        )
        
        credito_s = df_filtered[df_filtered['PAGAMENTO'] == 'Crédito'].groupby('CATEGORIA')['VALOR'].sum()
        debito_s = df_filtered[df_filtered['PAGAMENTO'] == 'Débito'].groupby('CATEGORIA')['VALOR'].sum()
        
        summary_cat['Crédito'] = credito_s
        summary_cat['Débito'] = debito_s
        summary_cat = summary_cat.fillna(0).sort_values('Valor', ascending=False)
        
        st.dataframe(
            summary_cat.style.format({
                "Valor": "$ {:,.2f}", 
                "Transações": "{:.0f}",
                "Crédito": "$ {:,.2f}", 
                "Débito": "$ {:,.2f}"
            }), 
            width='stretch'
        )
    else:
        st.info("Nenhuma transação encontrada com os filtros selecionados.")
    
    # 2. Side-by-Side: Subcategoria x Valor AND Transações x Subcategoria
    col_subcat_1, col_subcat_2 = st.columns(2)
    
    with col_subcat_1:
        # Bar Chart: Subcategoria x Valor
        if not df_filtered.empty:
            subcat_val_df = df_filtered.groupby('SUBCATEGORIA')['VALOR'].sum().reset_index().sort_values('VALOR', ascending=False)
            fig_subcat_val = px.bar(subcat_val_df, x='SUBCATEGORIA', y='VALOR', 
                                    title="Valor por Subcategoria", 
                                    color_discrete_sequence=[CHART_COLOR_SECONDARY])
            fig_subcat_val.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                         xaxis_title="", yaxis_title="$", font=dict(family=FONT_FAMILY, size=13))
            fig_subcat_val.update_traces(texttemplate='$ %{y:,.0f}', marker_line_width=0, opacity=0.9, textposition="outside", cliponaxis=False)
            st.plotly_chart(fig_subcat_val, width='stretch')
    
    with col_subcat_2:
        # Bar Chart: Transações x Subcategoria (Count)
        if not df_filtered.empty:
            subcat_count_df = df_filtered.groupby('SUBCATEGORIA').size().reset_index(name='TRANSACOES').sort_values('TRANSACOES', ascending=False)
            fig_subcat_count = px.bar(subcat_count_df, x='SUBCATEGORIA', y='TRANSACOES', 
                                      title="Qtd. de Transações por Subcategoria", 
                                      color_discrete_sequence=[CHART_COLOR_TERTIARY])
            fig_subcat_count.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                           xaxis_title="", yaxis_title="Qtd.", font=dict(family=FONT_FAMILY, size=13))
            fig_subcat_count.update_traces(texttemplate='%{y}', marker_line_width=0, opacity=0.9, textposition="outside", cliponaxis=False)
            st.plotly_chart(fig_subcat_count, width='stretch')
    
    st.divider()
    
    # --- TEMPORAL SECTION ---
    st.subheader("Análise Temporal")
    
    # Toggle Diário / Semanal
    visao_temporal = st.radio("Selecione a granularidade:", options=['Diário', 'Semanal'], horizontal=True)
    
    # Configurar coluna de tempo de acordo com o Toggle
    if visao_temporal == 'Diário':
        col_tempo = 'DATA'
        label_tempo = 'Data'
        dt_tickformat = "%d %b %Y"
    else:
        col_tempo = 'SEMANA'
        label_tempo = 'Semana do Ano'
        dt_tickformat = "" # Use default int formatting for week numbers
    
    # 3. Gráficos de Tempo (Line e Hist) baseados no Toggle
    col_time_1, col_time_2 = st.columns(2)
    
    with col_time_1:
        # Line Chart: Tendência (Apenas não 'Fixas')
        st.markdown(f"#### Tendência de Gastos Variáveis e Eventuais ({visao_temporal})")
        df_var = df_filtered[df_filtered['CATEGORIA'] != 'Fixas'].copy()
        if not df_var.empty:
            line_df = df_var.groupby([col_tempo, 'SUBCATEGORIA'])['VALOR'].sum().reset_index()
            fig_line = px.line(line_df, x=col_tempo, y='VALOR', color='SUBCATEGORIA', markers=True,
                               color_discrete_sequence=px.colors.qualitative.Prism)
            fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                   xaxis_title=label_tempo, yaxis_title="$", font=dict(family=FONT_FAMILY, size=13),
                                   legend_title_text='Subcategoria')
            fig_line.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9')
            if visao_temporal == 'Diário': fig_line.update_xaxes(tickformat=dt_tickformat)
            fig_line.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9')
            st.plotly_chart(fig_line, width='stretch')
        else:
            st.info("Nenhum dado das categorias variáveis e eventuais para exibir.")
    
    with col_time_2:
        # Histogram: Valor x Data (Sem distinção)
        st.markdown(f"#### Histograma de Gastos Total ({visao_temporal})")
        if not df_filtered.empty:
            hist_df = df_filtered.groupby(col_tempo)['VALOR'].sum().reset_index()
            fig_hist = px.bar(hist_df, x=col_tempo, y='VALOR',
                              color_discrete_sequence=['#475569']) # Slate 600
            fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', bargap=0.1,
                                   xaxis_title=label_tempo, yaxis_title="$", font=dict(family=FONT_FAMILY, size=13))
            fig_hist.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9', type='category' if visao_temporal == 'Semanal' else '-')
            if visao_temporal == 'Diário': fig_hist.update_xaxes(tickformat=dt_tickformat)
            fig_hist.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9')
            st.plotly_chart(fig_hist, width='stretch')
    
    # 4. Gráfico Barra: Média de Valor por Dia da Semana
    st.markdown("#### Média de Gastos por Dia da Semana")
    
    ordem_dias = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
    
    if not df_filtered.empty:
        # Calcular o gasto total gasto por data para depois achar a média desse valor por dia da semana
        daily_totals = df_filtered.groupby(['DATA', 'DIA_SEMANA'])['VALOR'].sum().reset_index()
        dia_semana_df = daily_totals.groupby('DIA_SEMANA')['VALOR'].mean().reset_index()
        
        # Garantir que todos os dias apareçam na ordem correta, mesmo que não tenham dados nulos
        dia_semana_df['DIA_SEMANA'] = pd.Categorical(dia_semana_df['DIA_SEMANA'], categories=ordem_dias, ordered=True)
        dia_semana_df = dia_semana_df.sort_values('DIA_SEMANA')
        
        fig_dia = px.bar(dia_semana_df, x='DIA_SEMANA', y='VALOR', 
                         color_discrete_sequence=[CHART_COLOR_PRIMARY])
        fig_dia.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                              xaxis_title="", yaxis_title="$", font=dict(family=FONT_FAMILY, size=14))
        fig_dia.update_traces(texttemplate='$ %{y:,.0f}', marker_line_width=0, opacity=0.9, textposition="outside", cliponaxis=False)
        
        st.plotly_chart(fig_dia, width='stretch')
    
    st.divider()
    
    # --- DETAILS ---
    st.subheader("Top 3 Maiores Despesas")
    
    if len(df_filtered) > 0:
        top3 = df_filtered.nlargest(3, 'VALOR')
        cols_top = st.columns(3)
        
        for i, (idx, row) in enumerate(top3.iterrows()):
            with cols_top[i]:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🏆 #{i+1} Despesa</h3>
                    <p><strong>Despesa:</strong> {row['DESPESA']}</p>
                    <p><strong>Valor:</strong> <span style="color:#B91C1C; font-weight:700; font-size:1.3em;">$ {row['VALOR']:,.2f}</span></p>
                    <p><strong>Categoria:</strong> {row['CATEGORIA']}</p>
                    <p><strong>Subcategoria:</strong> {row['SUBCATEGORIA']}</p>
                    <p><strong>Data:</strong> {row['DATA'].strftime('%d/%m/%Y')}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma despesa para exibir.")


# ==============================================================================
# ABA: FATURAS ATUAIS
# ==============================================================================
with tab_invoices:
    st.markdown("### Fechamento de Faturas Atuais")
    st.markdown(f"Cálculos baseados no período aberto de fatura.")
    
    # Fatura TD Calculation: Using the raw DataFrame `df` (not filtered by month widget)
    td_invoice_mask = (df['PAGAMENTO'] == 'Crédito') & (df['BANCO'] == 'TD') & \
                      (df['DATA'] >= configs['open_td']) & (df['DATA'] < configs['close_td'])
    total_fatura_td = df[td_invoice_mask]['VALOR'].sum()
    
    # Fatura RBC Calculation: Using the raw DataFrame `df` (not filtered by month widget)
    rbc_invoice_mask = (df['PAGAMENTO'] == 'Crédito') & (df['BANCO'] == 'RBC') & \
                       (df['DATA'] >= configs['open_rbc']) & (df['DATA'] < configs['close_rbc'])
    total_fatura_rbc = df[rbc_invoice_mask]['VALOR'].sum()
    total_consolidado = total_fatura_td + total_fatura_rbc
    
    # Consolidated Total Card
    st.markdown(f"""
    <div class="metric-card" style="margin-bottom: 24px;">
        <span class="invoice-label">Soma Total das Faturas</span>
        <div class="invoice-value" style="color: #1D4ED8;">$ {total_consolidado:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        td_logo_base64 = get_base64_of_bin_file('imgs/td_logo.svg')
        td_logo_html = f'<img class="invoice-logo" src="data:image/svg+xml;base64,{td_logo_base64}" height="48" alt="TD Logo"/>'
    except Exception:
        td_logo_html = '<h3>TD</h3>'
        
    try:
        rbc_logo_base64 = get_base64_of_bin_file('imgs/rbc_logo.svg')
        rbc_logo_html = f'<img class="invoice-logo" src="data:image/svg+xml;base64,{rbc_logo_base64}" height="48" alt="RBC Logo"/>'
    except Exception:
        rbc_logo_html = '<h3>RBC</h3>'

    col_inv1, col_inv2 = st.columns(2)
    
    with col_inv1:
        st.markdown(f"""
        <div class="invoice-card">
            <div class="invoice-info">
                <span class="invoice-label">Fatura Atual - TD</span>
                <span class="invoice-value">$ {total_fatura_td:,.2f}</span>
                <span class="invoice-period">Período: {configs['open_td'].strftime('%d/%m/%Y')} a {configs['close_td'].strftime('%d/%m/%Y')}</span>
            </div>
            {td_logo_html}
        </div>
        """, unsafe_allow_html=True)
        
    with col_inv2:
        st.markdown(f"""
        <div class="invoice-card">
            <div class="invoice-info">
                <span class="invoice-label">Fatura Atual - RBC</span>
                <span class="invoice-value">$ {total_fatura_rbc:,.2f}</span>
                <span class="invoice-period">Período: {configs['open_rbc'].strftime('%d/%m/%Y')} a {configs['close_rbc'].strftime('%d/%m/%Y')}</span>
            </div>
            {rbc_logo_html}
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.markdown("<p style='text-align:center; color:#94A3B8; font-size:0.9em;'>Desenvolvido com padrão de segurança e design corporativo.</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748B; font-size:0.8em; margin-top:-10px'>* Valores em Dólar Canadense</p>", unsafe_allow_html=True)

