import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

# Função para formatar os valores do eixo Y
def millions(x, pos):
    return '%1.0fM' % (x * 1e-6) if x >= 1e6 else '%1.0fK' % (x * 1e3) if x >= 1e3 else '%1.0f' % x

# Carregar dados
caminho_arquivo = "biweekly-confirmed-covid-19-cases.csv"
dados_covid = pd.read_csv(caminho_arquivo)

# Lista de países disponíveis
paises = dados_covid['Entity'].unique()

# Interface do usuário com Streamlit
st.title("Evolução dos Casos de COVID-19")
pais_selecionado = st.selectbox("Escolha seu país:", (paises))

# Barra lateral do site 
with st.sidebar:
    st.subheader('COVID-19 Tracker')
    st.write('O programa tem como objetivo a visualização e análise dos casos de COVID-19 ao redor do mundo. Desenvolvido para fornecer insights claros e atualizados sobre a evolução da pandemia, nosso aplicativo utiliza dados precisos e confiáveis do Our World in Data para oferecer uma visão abrangente da situação global.')
    st.caption('Projeto desenvolvido por Manuela Muniz')
    st.caption('FGV ECMI')

# Filtrar dados pelo país selecionado
dados_pais = dados_covid[dados_covid['Entity'] == pais_selecionado]

# Converter 'Day' para datetime, usando o formato específico 'AAAA-MM-DD'
dados_pais['Day'] = pd.to_datetime(dados_pais['Day'], format='%Y-%m-%d', errors='coerce')

# Remover linhas com datas inválidas
dados_pais = dados_pais.dropna(subset=['Day'])

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




