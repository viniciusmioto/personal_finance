import streamlit as st

from src.data_loader import get_base64_of_bin_file


def _get_bar_color(pct: float) -> str:
    """Return a color based on limit usage percentage."""
    if pct <= 50:
        return "#10B981"  # green
    elif pct <= 75:
        return "#F59E0B"  # amber
    else:
        return "#EF4444"  # red


def _build_card_html(
    label: str,
    logo_html: str,
    fatura: float,
    total_spent: float,
    payments: float,
    period_str: str,
) -> str:
    """Build the HTML for a single credit-card invoice card."""
    current_fatura = max(fatura, 0)
    return f"""<div class="invoice-card" style="position:relative;">
<div class="invoice-info" style="flex:1;">
<span class="invoice-label">{label}</span>
<span class="invoice-value">$ {current_fatura:,.2f}</span>
<span class="invoice-period">{period_str}</span>
</div>
{logo_html}
<div class="tooltip-content">
<span>Total Gasto: <strong>$ {total_spent:,.2f}</strong></span>
<span>Pagamentos: <strong>$ {payments:,.2f}</strong></span>
</div>
</div>"""


def _build_limit_bar_html(
    bank_name: str,
    limit: float,
    global_spent: float,
    global_paid: float,
) -> str:
    """Build the standalone HTML for the global limit usage."""
    used = max(global_spent - global_paid, 0)
    available = max(limit - used, 0)
    
    limit_pct = min((used / limit) * 100, 100) if limit > 0 else 0
    bar_color = _get_bar_color(limit_pct)

    return f"""<div class="global-limit-card">
<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px;">
    <span class="limit-label">Limite Atual - {bank_name}</span>
    <span class="limit-value" style="color: {bar_color};">{limit_pct:.0f}% em uso</span>
</div>
<div class="limit-bar-container-global">
    <div class="limit-bar-fill" style="width:{limit_pct:.1f}%; background:{bar_color};"></div>
</div>
<span class="limit-available">$ {available:,.2f} disponíveis</span>
</div>"""


def render_credit_cards(df, configs_df, payments_df):
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

    import pandas as pd
    if 'mes_ref_calculated' not in payments_df.columns:
        def get_mes_ref(row):
            bank = row['BANCO']
            date = row['DATA']
            col_due = 'due_td' if bank == 'TD' else 'due_rbc'
            future_configs = configs_df[configs_df[col_due] >= date].sort_values(by='mes_ref')
            if not future_configs.empty:
                base_ref = future_configs.iloc[0]['mes_ref']
                if 'DESCONTADA' in row and str(row['DESCONTADA']).strip().lower() == 'proxima':
                    return base_ref + 1
                return base_ref
            return None
        payments_df['mes_ref_calculated'] = payments_df.apply(get_mes_ref, axis=1)

    # --- TD ---
    td_invoice_mask = (
        (df['PAGAMENTO'] == 'Crédito')
        & (df['BANCO'] == 'TD')
        & (df['DATA'] >= config_row['open_td'])
        & (df['DATA'] < config_row['close_td'])
    )
    total_spent_td = df[td_invoice_mask]['VALOR'].sum()

    td_pay_mask = (
        (payments_df['BANCO'] == 'TD')
        & (payments_df['mes_ref_calculated'] == mes_ref_selecionado)
    )
    payments_td = payments_df[td_pay_mask]['VALOR'].sum()

    fatura_td = total_spent_td - payments_td
    limit_td = config_row['limit_td']

    # --- RBC ---
    rbc_invoice_mask = (
        (df['PAGAMENTO'] == 'Crédito')
        & (df['BANCO'] == 'RBC')
        & (df['DATA'] >= config_row['open_rbc'])
        & (df['DATA'] < config_row['close_rbc'])
    )
    total_spent_rbc = df[rbc_invoice_mask]['VALOR'].sum()

    rbc_pay_mask = (
        (payments_df['BANCO'] == 'RBC')
        & (payments_df['mes_ref_calculated'] == mes_ref_selecionado)
    )
    payments_rbc = payments_df[rbc_pay_mask]['VALOR'].sum()

    fatura_rbc = total_spent_rbc - payments_rbc
    limit_rbc = config_row['limit_rbc']

    # --- Consolidated KPIs ---
    total_gasto = total_spent_td + total_spent_rbc
    total_pago = payments_td + payments_rbc
    total_a_pagar = max(fatura_td, 0) + max(fatura_rbc, 0)

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    
    with col_kpi1:
        st.markdown(f"""<div class="metric-card" style="margin-bottom: 24px;">
<span class="invoice-label">Total Gasto</span>
<div class="invoice-value" style="color: #0F172A;">$ {total_gasto:,.2f}</div>
</div>""", unsafe_allow_html=True)

    with col_kpi2:
        st.markdown(f"""<div class="metric-card" style="margin-bottom: 24px;">
<span class="invoice-label">Pago</span>
<div class="invoice-value" style="color: #0F172A;">$ {total_pago:,.2f}</div>
</div>""", unsafe_allow_html=True)

    with col_kpi3:
        st.markdown(f"""<div class="metric-card" style="margin-bottom: 24px;">
<span class="invoice-label">A Pagar</span>
<div class="invoice-value" style="color: #1D4ED8;">$ {total_a_pagar:,.2f}</div>
</div>""", unsafe_allow_html=True)

    # --- Bank logos ---
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

    # --- Render Invoice Cards ---
    col_inv1, col_inv2 = st.columns(2)

    period_td = f"Período: {config_row['open_td'].strftime('%d/%m/%Y')} a {config_row['close_td'].strftime('%d/%m/%Y')}"
    period_rbc = f"Período: {config_row['open_rbc'].strftime('%d/%m/%Y')} a {config_row['close_rbc'].strftime('%d/%m/%Y')}"

    with col_inv1:
        st.markdown(
            _build_card_html("Fatura Atual - TD", td_logo_html, fatura_td, total_spent_td, payments_td, period_td),
            unsafe_allow_html=True,
        )

    with col_inv2:
        st.markdown(
            _build_card_html("Fatura Atual - RBC", rbc_logo_html, fatura_rbc, total_spent_rbc, payments_rbc, period_rbc),
            unsafe_allow_html=True,
        )

    # --- Global Limit Calculation ---
    global_spent_td = df[(df['PAGAMENTO'] == 'Crédito') & (df['BANCO'] == 'TD')]['VALOR'].sum()
    global_paid_td = payments_df[payments_df['BANCO'] == 'TD']['VALOR'].sum()
    
    global_spent_rbc = df[(df['PAGAMENTO'] == 'Crédito') & (df['BANCO'] == 'RBC')]['VALOR'].sum()
    global_paid_rbc = payments_df[payments_df['BANCO'] == 'RBC']['VALOR'].sum()

    # --- Render Global Limit Cards ---
    col_lim1, col_lim2 = st.columns(2)
    with col_lim1:
        st.markdown(
            _build_limit_bar_html("TD", config_row['limit_td'], global_spent_td, global_paid_td),
            unsafe_allow_html=True
        )
    with col_lim2:
        st.markdown(
            _build_limit_bar_html("RBC", config_row['limit_rbc'], global_spent_rbc, global_paid_rbc),
            unsafe_allow_html=True
        )
