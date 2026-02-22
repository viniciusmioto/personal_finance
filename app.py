import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    }
    .stTable {
        background-color: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.1);
    }
    h1, h2, h3 {
        color: #0F172A;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-weight: 600;
    }
    p {
        color: #334155;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
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
    }
    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('data/fev.csv')
    df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y')
    # Clean the VALOR column: remove $, and convert to float
    if df['VALOR'].dtype == 'O':
        df['VALOR'] = df['VALOR'].replace('[\$,]', '', regex=True).astype(float)
        
    # Extração de dias da semana e semanas para gráficos temporais
    df['SEMANA'] = df['DATA'].dt.isocalendar().week
    # Pandas dayofweek is 0-Monday, 6-Sunday
    dias = {0: 'Seg', 1: 'Ter', 2: 'Qua', 3: 'Qui', 4: 'Sex', 5: 'Sáb', 6: 'Dom'}
    df['DIA_SEMANA'] = df['DATA'].dt.dayofweek.map(dias)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Arquivo de dados não encontrado (data/fev.csv).")
    st.stop()

# --- HEADER ---
st.title("🏦 Dashboard Financeiro Principal")
st.markdown("Gestão consolidada de despesas.")
st.divider()

# --- KPIs ---
total_expense = df['VALOR'].sum()
transaction_count = len(df)
total_credit = df[df['PAGAMENTO'] == 'Crédito']['VALOR'].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Gasto Total", value=f"$ {total_expense:,.2f}")

with col2:
    st.metric(label="Número de Transações", value=f"{transaction_count}")

with col3:
    st.metric(label="Total no Crédito", value=f"$ {total_credit:,.2f}")
    
st.divider()

# --- CHARTS ---
st.subheader("Análise Gráfica")

# Banking Styling
CHART_COLOR_PRIMARY = '#1D4ED8' # Blue
CHART_COLOR_SECONDARY = '#0EA5E9' # Light Blue
CHART_COLOR_TERTIARY = '#10B981' # Green
FONT_FAMILY = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'

# 1. Resumo por Categoria (Moved to top from details)
st.markdown("#### Resumo por Categoria")
summary_cat = df.groupby('CATEGORIA').agg(
    Total=('VALOR', 'sum'),
    Transações=('VALOR', 'count')
).sort_values('Total', ascending=False)
st.dataframe(summary_cat.style.format({"Total": "$ {:,.2f}"}), width='stretch')

# 2. Side-by-Side: Subcategoria x Valor AND Transações x Subcategoria
col_subcat_1, col_subcat_2 = st.columns(2)

with col_subcat_1:
    # Bar Chart: Subcategoria x Valor
    subcat_val_df = df.groupby('SUBCATEGORIA')['VALOR'].sum().reset_index().sort_values('VALOR', ascending=False)
    fig_subcat_val = px.bar(subcat_val_df, x='SUBCATEGORIA', y='VALOR', 
                            title="Valor por Subcategoria", 
                            color_discrete_sequence=[CHART_COLOR_SECONDARY])
    fig_subcat_val.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                 xaxis_title="", yaxis_title="$", font=dict(family=FONT_FAMILY, size=13))
    fig_subcat_val.update_traces(texttemplate='$ %{y:,.0f}', marker_line_width=0, opacity=0.9, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig_subcat_val, width='stretch')

with col_subcat_2:
    # Bar Chart: Transações x Subcategoria (Count)
    subcat_count_df = df.groupby('SUBCATEGORIA').size().reset_index(name='TRANSACOES').sort_values('TRANSACOES', ascending=False)
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
    df_var = df[df['CATEGORIA'] != 'Fixas'].copy()
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
    hist_df = df.groupby(col_tempo)['VALOR'].sum().reset_index()
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

# Calcular o gasto total gasto por data para depois achar a média desse valor por dia da semana
daily_totals = df.groupby(['DATA', 'DIA_SEMANA'])['VALOR'].sum().reset_index()
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

top3 = df.nlargest(3, 'VALOR')
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
        
st.divider()
st.markdown("<p style='text-align:center; color:#94A3B8; font-size:0.9em;'>Desenvolvido com padrão de segurança e design corporativo.</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748B; font-size:0.8em; margin-top:-10px'>* Valores em Dólar Canadense</p>", unsafe_allow_html=True)
