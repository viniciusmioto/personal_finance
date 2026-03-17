import streamlit as st

from src.data_loader import get_base64_of_bin_file


def render_credit_cards(df, configs_df):
    """Render the 'Cartões de Crédito' tab."""

    st.markdown("### Fechamento de Faturas")
    
    # Filtro de Mês Referência
    meses_ref_disponiveis = sorted(configs_df['mes_ref'].unique().tolist(), reverse=True)
    col_ref, _ = st.columns(2)
    with col_ref:
        mes_ref_selecionado = st.selectbox("Selecione o Mês de Referência:", meses_ref_disponiveis)
    
    # Pegar as datas do mês selecionado
    config_row = configs_df[configs_df['mes_ref'] == mes_ref_selecionado].iloc[0]
    
    st.markdown(f"Cálculos baseados no período de fatura do mês {mes_ref_selecionado}.")
    
    # Fatura TD Calculation
    td_invoice_mask = (df['PAGAMENTO'] == 'Crédito') & (df['BANCO'] == 'TD') & \
                      (df['DATA'] >= config_row['open_td']) & (df['DATA'] < config_row['close_td'])
    total_fatura_td = df[td_invoice_mask]['VALOR'].sum()
    
    # Fatura RBC Calculation
    rbc_invoice_mask = (df['PAGAMENTO'] == 'Crédito') & (df['BANCO'] == 'RBC') & \
                       (df['DATA'] >= config_row['open_rbc']) & (df['DATA'] < config_row['close_rbc'])
    total_fatura_rbc = df[rbc_invoice_mask]['VALOR'].sum()
    total_consolidado = total_fatura_td + total_fatura_rbc
    
    # Consolidated Total Card
    st.markdown(f"""
    <div class="metric-card" style="margin-bottom: 24px;">
        <span class="invoice-label">Soma Total das Faturas</span>
        <div class="invoice-value" style="color: #1D4ED8;">$ {total_consolidado:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Bank logos
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
                <span class="invoice-label">Fatura - TD</span>
                <span class="invoice-value">$ {total_fatura_td:,.2f}</span>
                <span class="invoice-period">Período: {config_row['open_td'].strftime('%d/%m/%Y')} a {config_row['close_td'].strftime('%d/%m/%Y')}</span>
            </div>
            {td_logo_html}
        </div>
        """, unsafe_allow_html=True)
        
    with col_inv2:
        st.markdown(f"""
        <div class="invoice-card">
            <div class="invoice-info">
                <span class="invoice-label">Fatura - RBC</span>
                <span class="invoice-value">$ {total_fatura_rbc:,.2f}</span>
                <span class="invoice-period">Período: {config_row['open_rbc'].strftime('%d/%m/%Y')} a {config_row['close_rbc'].strftime('%d/%m/%Y')}</span>
            </div>
            {rbc_logo_html}
        </div>
        """, unsafe_allow_html=True)
