import pandas as pd
from sqlalchemy import create_engine

# Caminho completo para o arquivo
file_path = "C:/Users/Luiz/Desktop/Estudos/Sistema-web-entrega/Abastecimentos.xlsx"

# Cabeçalho personalizado para o DataFrame
cabecalho = ['placa','data_abastecimento','tipo_combustivel','quantidade_combustivel','valor_abastecido']

# Verifica se o arquivo existe no caminho especificado
try:
    df = pd.read_excel(file_path,skiprows=1, header=None, names=cabecalho)
except FileNotFoundError as e:
    print(f"Erro: {e}")
    df = pd.DataFrame()  # cria um DataFrame vazio para evitar erros subsequentes

# Formatar a data para outro formato ( 08/11/2018 - 2018/11/08)
df['data_abastecimento'] = pd.to_datetime(df['data_abastecimento'], format='%d/%m/%Y').dt.strftime('%Y/%m/%d')
df['data_abastecimento'] = pd.to_datetime(df['data_abastecimento'])

# Extrair apenas a data (sem a parte do tempo)
df['data_abastecimento'] = df['data_abastecimento'].dt.date

# Substituindo nomes das regiões
df['tipo_combustivel'] = df['tipo_combustivel'].str.replace('GASOLINA C COMUM', 'GASOLINA')
df['tipo_combustivel'] = df['tipo_combustivel'].str.replace('GASOLINA ADIT GRID', 'GASOLINA')
df['tipo_combustivel'] = df['tipo_combustivel'].str.replace('GASOLINA ADITIVADA', 'GASOLINA')
df['tipo_combustivel'] = df['tipo_combustivel'].str.replace('DIESEL S10 GRID.', 'DIESEL')

# Obtendo os valores únicos
#unique_names = df['tipo_combustivel'].unique()

#print(unique_names)

try:
    # Criar uma conexão com o banco de dados PostgreSQL
    engine = create_engine('postgresql://postgres:1234@localhost:5432/trabalho_extensao')

    # Importar dados para a tabela
    df.to_sql('dados', engine, if_exists='append', index=False)
    print("Dados importados com sucesso.")

except Exception as e:
    print(f"Erro ao conectar ao banco de dados ou importar dados: {e}")