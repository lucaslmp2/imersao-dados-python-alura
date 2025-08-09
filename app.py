import streamlit as st
import pandas as pd
import plotly.express as px

import os

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# --- Funções ---

@st.cache_data
def carregar_dados():
    """Carrega os dados de salários a partir de uma URL e os retorna como um DataFrame."""
    df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")
    return df

def carregar_estilos():
    """Carrega e injeta o CSS customizado."""
    style_path = os.path.join("styles", "style.css")
    if os.path.exists(style_path):
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def configurar_sidebar(df):
    """Configura a barra lateral com os filtros e retorna os valores selecionados."""
    st.sidebar.header("🔍 Filtros")
    
    anos_disponiveis = sorted(df['ano'].unique())
    anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

    senioridades_disponiveis = sorted(df['senioridade'].unique())
    senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

    contratos_disponiveis = sorted(df['contrato'].unique())
    contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

    tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
    tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)
    
    return anos_selecionados, senioridades_selecionadas, contratos_selecionados, tamanhos_selecionados

def exibir_kpis(df_filtrado):
    """Exibe os KPIs principais em colunas."""
    with st.container():
        st.subheader("Métricas Gerais (Salário Anual em USD)")
        if not df_filtrado.empty:
            salario_medio = df_filtrado['usd'].mean()
            salario_maximo = df_filtrado['usd'].max()
            total_registros = df_filtrado.shape[0]
            cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
        else:
            salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, "N/A"

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Salário Médio", f"${salario_medio:,.0f}")
        col2.metric("Salário Máximo", f"${salario_maximo:,.0f}")
        col3.metric("Total de Registros", f"{total_registros:,}")
        col4.metric("Cargo Mais Frequente", cargo_mais_frequente)

def exibir_graficos(df_filtrado):
    """Exibe os gráficos de análise em colunas."""
    st.subheader("Análises Visuais")
    
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        with st.container():
            if not df_filtrado.empty:
                top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
                grafico_cargos = px.bar(
                    top_cargos, x='usd', y='cargo', orientation='h',
                    title="Top 10 Cargos por Salário Médio",
                    labels={'usd': 'Média Salarial Anual (USD)', 'cargo': ''},
                    template="plotly_dark"
                )
                grafico_cargos.update_layout(
                    title_x=0.5, yaxis={'categoryorder':'total ascending'},
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(grafico_cargos, use_container_width=True)
            else:
                st.warning("Nenhum dado para exibir no gráfico de cargos.")

    with col_graf2:
        with st.container():
            if not df_filtrado.empty:
                grafico_hist = px.histogram(
                    df_filtrado, x='usd', nbins=30,
                    title="Distribuição de Salários Anuais",
                    labels={'usd': 'Faixa Salarial (USD)', 'count': ''},
                    template="plotly_dark"
                )
                grafico_hist.update_layout(
                    title_x=0.5, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(grafico_hist, use_container_width=True)
            else:
                st.warning("Nenhum dado para exibir no gráfico de distribuição.")

    col_graf3, col_graf4 = st.columns(2)

    with col_graf3:
        with st.container():
            if not df_filtrado.empty:
                remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
                remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
                grafico_remoto = px.pie(
                    remoto_contagem, names='tipo_trabalho', values='quantidade',
                    title='Proporção dos Tipos de Trabalho', hole=0.5,
                    template="plotly_dark"
                )
                grafico_remoto.update_traces(textinfo='percent+label')
                grafico_remoto.update_layout(
                    title_x=0.5, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(grafico_remoto, use_container_width=True)
            else:
                st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

    with col_graf4:
        with st.container():
            if not df_filtrado.empty:
                cargos_populares = df_filtrado['cargo'].value_counts().nlargest(10).index.tolist()
                cargo_selecionado = st.selectbox(
                    "Selecione um cargo para ver o mapa de salários:",
                    cargos_populares,
                    index=cargos_populares.index('Data Scientist') if 'Data Scientist' in cargos_populares else 0
                )
                
                df_cargo = df_filtrado[df_filtrado['cargo'] == cargo_selecionado]
                media_cargo_pais = df_cargo.groupby('residencia_iso3')['usd'].mean().reset_index()
                
                grafico_paises = px.choropleth(
                    media_cargo_pais, locations='residencia_iso3', color='usd',
                    color_continuous_scale='ylgnbu',
                    title=f'Salário Médio de {cargo_selecionado} por País',
                    labels={'usd': 'Salário Médio (USD)', 'residencia_iso3': 'País'},
                    template="plotly_dark"
                )
                grafico_paises.update_layout(
                    title_x=0.5, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(grafico_paises, use_container_width=True)
            else:
                st.warning("Nenhum dado para exibir no gráfico de países.")

def main():
    """Função principal que executa o aplicativo Streamlit."""
    carregar_estilos()
    
    df = carregar_dados()
    
    anos, senioridades, contratos, tamanhos = configurar_sidebar(df)

    # Filtragem do DataFrame
    df_filtrado = df[
        (df['ano'].isin(anos)) &
        (df['senioridade'].isin(senioridades)) &
        (df['contrato'].isin(contratos)) &
        (df['tamanho_empresa'].isin(tamanhos))
    ]

    # --- Conteúdo Principal ---
    st.title("📈 Dashboard de Análise de Salários na Área de Dados")
    st.markdown("Explore os dados salariais na área de dados. Utilize os filtros à esquerda para refinar sua análise.")
    st.markdown("---")

    exibir_kpis(df_filtrado)
    st.markdown("---")
    exibir_graficos(df_filtrado)
    st.markdown("---")

    # Tabela de Dados Detalhados
    with st.container():
        st.subheader("Dados Detalhados")
        st.dataframe(df_filtrado, use_container_width=True)

if __name__ == "__main__":
    main()