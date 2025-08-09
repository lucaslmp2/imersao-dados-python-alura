# 📊 Dashboard de Análise de Salários na Área de Dados

Este projeto é um dashboard interativo desenvolvido com Streamlit para a análise de salários na área de dados. Ele permite a visualização e filtragem de dados salariais, oferecendo insights sobre remuneração em diferentes cargos, senioridades e localidades.

O dashboard foi criado como parte da **Imersão de Dados da Alura**.

 
*(https://github.com/lucaslmp2/imersao-dados-python-alura/blob/main/Dash.png)*

---

## ✨ Funcionalidades

- **Dashboard Interativo:** Interface amigável e responsiva para explorar os dados.
- **Filtros Dinâmicos:** Filtre os dados por:
  - Ano
  - Nível de Senioridade
  - Tipo de Contrato
  - Tamanho da Empresa
- **Métricas Chave (KPIs):** Visualização rápida do salário médio, salário máximo, total de registros e o cargo mais frequente com base nos filtros aplicados.
- **Gráficos Detalhados:**
  - **Top 10 Cargos por Salário Médio:** Gráfico de barras horizontais mostrando os cargos com maior remuneração média.
  - **Distribuição de Salários Anuais:** Histograma que exibe a frequência das faixas salariais.
  - **Proporção de Tipos de Trabalho:** Gráfico de pizza (donut) que mostra a distribuição entre trabalho remoto e presencial.
  - **Mapa de Salários por País:** Mapa coroplético que exibe o salário médio para um cargo selecionado em diferentes países.
- **Tabela de Dados:** Explore os dados brutos filtrados diretamente na aplicação.

---

## 🛠️ Tecnologias Utilizadas

O projeto foi construído utilizando as seguintes tecnologias:

- **Python:** Linguagem de programação principal.
- **Streamlit:** Framework para a criação do dashboard web.
- **Pandas:** Para manipulação e análise dos dados.
- **Plotly Express:** Para a criação dos gráficos interativos.

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para executar o projeto localmente.

### Pré-requisitos

É necessário ter o **Python 3.8** (ou superior) instalado em sua máquina.

### Instalação

1.  Clone o repositório:
    ```bash
    git clone https://github.com/lucaslmp2/imersao-dados-python-alura
    cd imersao-dados-python-alura
    ```

2.  (Opcional, mas recomendado) Crie e ative um ambiente virtual:
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    
    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  Instale as dependências do projeto:
    ```bash
    pip install -r requirements.txt
    ```

### Execução

Para iniciar a aplicação Streamlit, execute o seguinte comando no terminal:
```bash
streamlit run app.py
```

A aplicação será aberta automaticamente em seu navegador padrão.

---

## 📄 Fonte dos Dados

Os dados utilizados neste projeto foram obtidos a partir do arquivo `imersao-dados-final.csv`, disponibilizado no repositório lucaslmp2/imersao-dados-python-alura. O dashboard carrega os dados diretamente da URL do arquivo bruto no GitHub.