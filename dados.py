# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:48:15 2026

@author: gustavo.araujo
"""

# =============================================================================
# Importando Bibliotecas
# =============================================================================

print("Importando Bibliotecas")

import pandas as pd
import numpy as np

print("Bibliotecas importadas com sucesso!")

# =============================================================================
# Coletando dados
# =============================================================================

# Dados compilados anteriormente via código

print("Iniciando coleta de dados da INFRA S.A")

infra = pd.read_csv(filepath_or_buffer = "infra.csv", sep = ",")
print("Dados de projeções base carregadas!")
print(infra.head(5))

infra_transf = pd.read_csv(filepath_or_buffer = "infra_transf.csv", sep = ",")
print("Dados de projeções transformadoras carregadas!")
print(infra_transf.head(5))

dicionario = pd.read_excel("dicionario_bases_dados.xlsx", sheet_name="Códigos IBGE")
print("Códigos do IBGE carregados!")
print(dicionario.head(5))


# =============================================================================
# Tratamento dos dados
# =============================================================================

print("Tratamento dos dados")

infra['cenario'] = "base"

infra = pd.merge(
    infra,
    dicionario,
    left_on='mun_origem',
    right_on='Código IBGE',
    how='left'
)

infra = infra.rename(columns={
    'Nome do município': 'nome_mun_origem',
    'Nome da UF': 'nome_uf_origem'
}).drop(columns=['Código IBGE'])

infra = pd.merge(
    infra,                
    dicionario,                      
    left_on='mun_destino',           
    right_on='Código IBGE',
    how='left'
)

infra_tratado = infra.rename(columns={
    'Nome do município': 'nome_mun_destino',
    'Nome da UF': 'nome_uf_destino'
}).drop(columns=['Código IBGE'])

print(infra_tratado.head(10))

infra_transf['cenario'] = "transformador"

infra_transf = pd.merge(
    infra_transf,
    dicionario,
    left_on='mun_origem',
    right_on='Código IBGE',
    how='left'
)

infra_transf = infra_transf.rename(columns={
    'Nome do município': 'nome_mun_origem',
    'Nome da UF': 'nome_uf_origem'
}).drop(columns=['Código IBGE'])

infra_transf = pd.merge(
    infra_transf,                
    dicionario,                      
    left_on='mun_destino',           
    right_on='Código IBGE',
    how='left'
)

infra_transf_tratado = infra_transf.rename(columns={
    'Nome do município': 'nome_mun_destino',
    'Nome da UF': 'nome_uf_destino'
}).drop(columns=['Código IBGE'])

print(infra_transf_tratado.head(10))

print('Juntando datasets...')
infra_final = pd.concat([infra_tratado, infra_transf_tratado], ignore_index = True)
infra_final = infra_final.drop(columns = ['mun_origem', 'mun_destino'])


# 1. Criamos o dicionário de "Tradução" (Estado -> Região)
dicionario_regioes = {
    'Acre': 'Norte', 'Amapá': 'Norte', 'Amazonas': 'Norte', 'Pará': 'Norte', 'Rondônia': 'Norte', 'Roraima': 'Norte', 'Tocantins': 'Norte',
    'Alagoas': 'Nordeste', 'Bahia': 'Nordeste', 'Ceará': 'Nordeste', 'Maranhão': 'Nordeste', 'Paraíba': 'Nordeste', 'Pernambuco': 'Nordeste', 'Piauí': 'Nordeste', 'Rio Grande do Norte': 'Nordeste', 'Sergipe': 'Nordeste',
    'Distrito Federal': 'Centro-Oeste', 'Goiás': 'Centro-Oeste', 'Mato Grosso': 'Centro-Oeste', 'Mato Grosso do Sul': 'Centro-Oeste',
    'Espírito Santo': 'Sudeste', 'Minas Gerais': 'Sudeste', 'Rio de Janeiro': 'Sudeste', 'São Paulo': 'Sudeste',
    'Paraná': 'Sul', 'Rio Grande do Sul': 'Sul', 'Santa Catarina': 'Sul'
}

# 2. Usamos o .map() para criar a coluna de Região da Origem
# (Substitua 'nome_uf_origem' pelo nome exato da sua coluna de estado)
infra_final['regiao_origem'] = infra_final['nome_uf_origem'].map(dicionario_regioes)

# 3. Opcional: Fazer o mesmo para o Destino, se você quiser!
infra_final['regiao_destino'] = infra_final['nome_uf_destino'].map(dicionario_regioes)

print(infra_final.head(15))

print("Salvando dataset final")
infra_final.to_csv('infra_final.csv', index= False)

print("Dataset Salvo!")