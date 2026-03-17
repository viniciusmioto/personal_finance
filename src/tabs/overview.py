import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_loader import (
    CHART_COLOR_PRIMARY,
    CHART_COLOR_SECONDARY,
    CHART_COLOR_TERTIARY,
    FONT_FAMILY,
)


def render_overview(df):
    """Render the 'Visão Geral' tab."""

    # Filtro de Mês
    col_filter, _ = st.columns(2)
    with col_filter:
        meses_disponiveis = sorted(df['MES_STR'].unique().tolist(), reverse=True)
        mes_selecionado = st.selectbox("Selecione o Mês:", meses_disponiveis)

    # Aplicar filtro
    df_filtered = df[df['MES_STR'] == mes_selecionado].copy()

    # --- KPIs ---
    total_expense = df_filtered['VALOR'].sum()
    total_credit = df_filtered[df_filtered['PAGAMENTO'] == 'Crédito']['VALOR'].sum()
    total_debit = df_filtered[df_filtered['PAGAMENTO'] == 'Débito']['VALOR'].sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Gasto Total", value=f"$ {total_expense:,.2f}")
    with col2:
        st.metric(label="Total Crédito", value=f"$ {total_credit:,.2f}")
    with col3:
        st.metric(label="Total Débito", value=f"$ {total_debit:,.2f}")
        
    st.divider()

    # --- RESUMO ---
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
    
    # --- SUBCATEGORIA CHARTS (side by side) ---
    col_subcat_1, col_subcat_2 = st.columns(2)
    
    with col_subcat_1:
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
    
    visao_temporal = st.radio("Selecione a granularidade:", options=['Diário', 'Semanal'], horizontal=True)
    
    if visao_temporal == 'Diário':
        col_tempo = 'DATA'
        label_tempo = 'Data'
        dt_tickformat = "%d %b %Y"
    else:
        col_tempo = 'SEMANA'
        label_tempo = 'Semana do Ano'
        dt_tickformat = ""
    
    col_time_1, col_time_2 = st.columns(2)
    
    with col_time_1:
        st.markdown(f"#### Tendência de Gastos Variáveis ({visao_temporal})")
        df_var = df_filtered[df_filtered['CATEGORIA'] == 'Variáveis'].copy()
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
            st.info("Nenhum dado da categoria variáveis para exibir.")
    
    with col_time_2:
        st.markdown(f"#### Histograma de Gastos Eventuais ({visao_temporal})")
        df_eventual = df_filtered[df_filtered['CATEGORIA'] == 'Eventual'].copy()
        if not df_eventual.empty:
            hist_df = df_eventual.groupby([col_tempo, 'SUBCATEGORIA'])['VALOR'].sum().reset_index()
            fig_hist = px.bar(hist_df, x=col_tempo, y='VALOR', color='SUBCATEGORIA',
                              color_discrete_sequence=px.colors.qualitative.Prism)
            fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', bargap=0.1,
                                   xaxis_title=label_tempo, yaxis_title="$", font=dict(family=FONT_FAMILY, size=13),
                                   legend_title_text='Categorias')
            fig_hist.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9', type='category' if visao_temporal == 'Semanal' else '-')
            if visao_temporal == 'Diário': fig_hist.update_xaxes(tickformat=dt_tickformat)
            fig_hist.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9')
            st.plotly_chart(fig_hist, width='stretch')
        else:
            st.info("Nenhum dado na categoria eventual para exibir.")
    
    # --- MÉDIA POR DIA DA SEMANA ---
    st.markdown("#### Média de Gastos por Dia da Semana")
    
    ordem_dias = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
    
    if not df_filtered.empty:
        daily_totals = df_filtered.groupby(['DATA', 'DIA_SEMANA'])['VALOR'].sum().reset_index()
        dia_semana_df = daily_totals.groupby('DIA_SEMANA')['VALOR'].mean().reset_index()
        
        dia_semana_df['DIA_SEMANA'] = pd.Categorical(dia_semana_df['DIA_SEMANA'], categories=ordem_dias, ordered=True)
        dia_semana_df = dia_semana_df.sort_values('DIA_SEMANA')
        
        fig_dia = px.bar(dia_semana_df, x='DIA_SEMANA', y='VALOR', 
                         color_discrete_sequence=[CHART_COLOR_PRIMARY])
        fig_dia.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                              xaxis_title="", yaxis_title="$", font=dict(family=FONT_FAMILY, size=14))
        fig_dia.update_traces(texttemplate='$ %{y:,.0f}', marker_line_width=0, opacity=0.9, textposition="outside", cliponaxis=False)
        
        st.plotly_chart(fig_dia, width='stretch')
    
    st.divider()
    
    # --- TOP 3 DESPESAS ---
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
