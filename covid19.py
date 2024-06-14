import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

# Função para formatar os valores do eixo Y
def millions(x, pos):
    return '%1.0fM' % (x * 1e-6) if x >= 1e6 else '%1.0fK' % (x * 1e-3) if x >= 1e3 else '%1.0f' % x

# Carregar dados
caminho_arquivo = "biweekly-confirmed-covid-19-cases.csv"
dados_covid = pd.read_csv(caminho_arquivo)

# Exibir as primeiras linhas do DataFrame para verificar a estrutura dos dados
st.write("Primeiras linhas do DataFrame:")
st.write(dados_covid.head())

# Lista de países disponíveis
paises = dados_covid['Entity'].unique()

# Interface do usuário com Streamlit
st.title("Evolução dos Casos de COVID-19")
st.sidebar.header("Escolha o país")

# Selecionar o país
pais_selecionado = st.sidebar.selectbox("Selecione o país", paises)

# Filtrar dados pelo país selecionado
dados_pais = dados_covid[dados_covid['Entity'] == pais_selecionado]

# Exibir as primeiras linhas do DataFrame filtrado para verificar a estrutura dos dados
st.write(f"Primeiras linhas dos dados do país selecionado ({pais_selecionado}):")
st.write(dados_pais.head())

# Converter 'Day' para datetime, usando o formato específico 'AAAA-MM-DD'
dados_pais['Day'] = pd.to_datetime(dados_pais['Day'], format='%Y-%m-%d', errors='coerce')

# Remover linhas com datas inválidas
dados_pais = dados_pais.dropna(subset=['Day'])

# Verificar se a conversão de datas foi bem-sucedida
st.write("Datas após a conversão:")
st.write(dados_pais[['Day']].head())

# Ordenar os dados por data
dados_pais = dados_pais.sort_values('Day').reset_index(drop=True)

# Calcular a diferença diária de casos (como os dados são bissemanal, dividimos por 14)
dados_pais['daily_cases'] = dados_pais['Biweekly cases'] / 14

# Selecionar amostra dos dados para plotagem
sample = dados_pais.sample(50).sort_values('Day')

# Plotar o gráfico de evolução diária
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(sample['Day'], sample['daily_cases'], marker='o', linestyle='-')
ax.set_title(f'Evolução diária dos casos de COVID-19 em {pais_selecionado}')
ax.set_xlabel("Data")
ax.set_ylabel("Novos Casos Diários")
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %Y'))  # Formatar o eixo X para mostrar mês e ano
ax.yaxis.set_major_formatter(FuncFormatter(millions))  # Formatar o eixo Y para números mais legíveis
plt.xticks(rotation=45)
plt.grid(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Mostrar o gráfico no Streamlit
st.pyplot(fig)

