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

print("Iniciando coleta de dados da INFRA S.A")

infra = pd.read_csv(filepath_or_buffer="infra.csv", sep=",")
print("Dados de projeções base carregadas!")
print(infra.head(5))

infra_transf = pd.read_csv(filepath_or_buffer="infra_transf.csv", sep=",")
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
    'Nome da UF':        'nome_uf_origem'
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
    'Nome da UF':        'nome_uf_destino'
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
    'Nome da UF':        'nome_uf_origem'
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
    'Nome da UF':        'nome_uf_destino'
}).drop(columns=['Código IBGE'])

print(infra_transf_tratado.head(10))

print('Juntando datasets...')
infra_final = pd.concat([infra_tratado, infra_transf_tratado], ignore_index=True)
infra_final = infra_final.drop(columns=['mun_origem', 'mun_destino'])

# Dicionário de regiões
dicionario_regioes = {
    'Acre': 'Norte', 'Amapá': 'Norte', 'Amazonas': 'Norte', 'Pará': 'Norte',
    'Rondônia': 'Norte', 'Roraima': 'Norte', 'Tocantins': 'Norte',
    'Alagoas': 'Nordeste', 'Bahia': 'Nordeste', 'Ceará': 'Nordeste',
    'Maranhão': 'Nordeste', 'Paraíba': 'Nordeste', 'Pernambuco': 'Nordeste',
    'Piauí': 'Nordeste', 'Rio Grande do Norte': 'Nordeste', 'Sergipe': 'Nordeste',
    'Distrito Federal': 'Centro-Oeste', 'Goiás': 'Centro-Oeste',
    'Mato Grosso': 'Centro-Oeste', 'Mato Grosso do Sul': 'Centro-Oeste',
    'Espírito Santo': 'Sudeste', 'Minas Gerais': 'Sudeste',
    'Rio de Janeiro': 'Sudeste', 'São Paulo': 'Sudeste',
    'Paraná': 'Sul', 'Rio Grande do Sul': 'Sul', 'Santa Catarina': 'Sul'
}

infra_final['regiao_origem']  = infra_final['nome_uf_origem'].map(dicionario_regioes)
infra_final['regiao_destino'] = infra_final['nome_uf_destino'].map(dicionario_regioes)

print(infra_final.head(15))

# =============================================================================
# ✅ Otimizações de tamanho
# =============================================================================

print("\n--- Antes das otimizações ---")
print(f"Colunas:  {list(infra_final.columns)}")
print(f"Linhas:   {len(infra_final):,}")
print(f"Memória:  {infra_final.memory_usage(deep=True).sum() / 1024**2:.1f} MB")


# 2. Tipos numéricos menores
infra_final['toneladas'] = pd.to_numeric(infra_final['toneladas'], downcast='integer')
infra_final['Ano']       = infra_final['Ano'].astype('int16')

# 3. Texto repetitivo como category
for col in ['cenario', 'macro_produto', 'regiao_origem', 'regiao_destino']:
    if col in infra_final.columns:
        infra_final[col] = infra_final[col].astype('category')

print("\n--- Depois das otimizações ---")
print(f"Colunas:  {list(infra_final.columns)}")
print(f"Linhas:   {len(infra_final):,}")
print(f"Memória:  {infra_final.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

# =============================================================================
# Salvando dataset final
# =============================================================================

print("\nSalvando dataset final compactado...")
infra_final.to_csv('infra_final.csv.gz', compression='gzip', index=False)
print("Dataset salvo como infra_final.csv.gz ✅")