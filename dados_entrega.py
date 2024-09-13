import pandas as pd
from sqlalchemy import create_engine

# Caminho completo para o arquivo
file_path = "C:/Users/Luiz/Desktop/Estudos/Sistema-web-entrega/CONTROLE_ENTREGA_JULHO_2024_MOTORISTAS.xlsx"

# Cabeçalho personalizado para o DataFrame
cabecalho = ['motorista','tipo_veiculo','placa','data_entrega','hora_saida','km_inicial',
             'quantidade_notas_fiscais','quantidade_coletas','km_final','total_dia','regiao']

# Verifica se o arquivo existe no caminho especificado
try:
    df = pd.read_excel(file_path,skiprows=1, header=None, names=cabecalho)
except FileNotFoundError as e:
    print(f"Erro: {e}")
    df = pd.DataFrame()  # cria um DataFrame vazio para evitar erros subsequentes

# Adicionando uma nova coluna na posição desejada
df.insert(0, 'numero_entrega', range(1, len(df) + 1))

# Formatar a data para outro formato ( 08/11/2018 - 2018/11/08)
df['data_entrega'] = pd.to_datetime(df['data_entrega'], format='%d/%m/%Y').dt.strftime('%Y/%m/%d')
df['data_entrega'] = pd.to_datetime(df['data_entrega'])

# Extrair apenas a data (sem a parte do tempo)
df['data_entrega'] = df['data_entrega'].dt.date

# Preenchemos o valor NA por ( 0 )
# inplace = True / para altera o proprio DataFrame
dado = 0
df['quantidade_coletas'] = df['quantidade_coletas'].fillna(value = dado)

# Convertendo uma única coluna para inteiro
df['quantidade_coletas'] = df['quantidade_coletas'].astype(int)

df['quantidade_notas_fiscais'] = df['quantidade_notas_fiscais'].fillna(value = dado)

# Convertendo uma única coluna para inteiro
df['quantidade_notas_fiscais'] = df['quantidade_notas_fiscais'].astype(int)


# Substituindo nomes das regiões
df['regiao'] = df['regiao'].str.replace('SOB', 'SOBRADINHO')
df['regiao'] = df['regiao'].str.replace('PLANA-DF', 'PLANALTINA-DF')
df['regiao'] = df['regiao'].str.replace('VICENTE P', 'VICENTE PIRES')
df['regiao'] = df['regiao'].str.replace('CEI', 'CEILANDIA')
df['regiao'] = df['regiao'].str.replace('PARQUE W', 'PARK WAY')
df['regiao'] = df['regiao'].str.replace('CIDADE O', 'CIDADE OCIDENTAL')
df['regiao'] = df['regiao'].str.replace('TAGUA-SUL', 'TAGUATINGA-SUL')
df['regiao'] = df['regiao'].str.replace('S SEB', 'SAO SEBASTIAO')
df['regiao'] = df['regiao'].str.replace('SAI', 'SIA')
df['regiao'] = df['regiao'].str.replace('SANTA M', 'SANTA MARIA')
df['regiao'] = df['regiao'].str.replace('RIACHO F', 'RIACHO FUNDO')
df['regiao'] = df['regiao'].str.replace('PLANA-GO', 'PLANALTINA-GO')
df['regiao'] = df['regiao'].str.replace('BRASLÂNDIA', 'BRAZLANDIA')
df['regiao'] = df['regiao'].str.replace('TAGUA-NORTE', 'TAGUATINGA-NORTE')
df['regiao'] = df['regiao'].str.replace('V PIRES', 'VICENTE PIRES')
df['regiao'] = df['regiao'].str.replace('A LINDAS', 'AGUAS LINDAS')
df['regiao'] = df['regiao'].str.replace('TAGUA NORTE', 'TAGUATINGA-NORTE')
df['regiao'] = df['regiao'].str.replace('PLANALTINA-DF-GO', 'PLANALTINA-DF/PLANALTINA-GO')
df['regiao'] = df['regiao'].str.replace('CANDANGO', 'CANDANGOLANDIA')
df['regiao'] = df['regiao'].str.replace('CANDANGA', 'CANDANGOLANDIA')
df['regiao'] = df['regiao'].str.replace('SICIA', 'SCIA')
df['regiao'] = df['regiao'].str.replace('VAL', 'VALPARAISO-GO')
df['regiao'] = df['regiao'].str.replace('SOF-NORTE-SUL', 'SOF-NORTE/SOF-SUL')
df['regiao'] = df['regiao'].str.replace('TAGUATINGA-NORTE-SUL', 'TAGUATINGA-NORTE/TAGUATINGA-SUL')
df['regiao'] = df['regiao'].str.replace('CIDADE A', 'CIDADE DO AUTOMOVEL')
df['regiao'] = df['regiao'].str.replace('GUARÁ', 'GUARA')
df['regiao'] = df['regiao'].str.replace('SOF SUL', 'SOF-SUL')
df['regiao'] = df['regiao'].str.replace('ITAPOÃ', 'ITAPOA')
df['regiao'] = df['regiao'].str.replace('SUDEOSTE', 'SUDOESTE')
#df['regiao'] = df['regiao'].str.replace('NUCLEO', 'NUCLEO BANDEIRANTE')
df['regiao'] = df['regiao'].str.replace('NUCLEO B', 'NUCLEO BANDEIRANTE')

# Obtendo os valores únicos
#unique_names = df['regiao'].unique()

#print(unique_names)

# Divida a Coluna em Listas
df['regiao'] = df['regiao'].str.split('/')

# Transformar Listas em Linhas Separadas
df_exploded = df.explode('regiao')

# Remova Espaços em Branco Extras
df_exploded['regiao'] = df_exploded['regiao'].str.strip()

try:
    # Criar uma conexão com o banco de dados PostgreSQL
    engine = create_engine('postgresql://postgres:1234@localhost:5432/trabalho_extensao')

    # Importar dados para a tabela
    df_exploded.to_sql('dados', engine, if_exists='append', index=False)
    print("Dados importados com sucesso.")

except Exception as e:
    print(f"Erro ao conectar ao banco de dados ou importar dados: {e}")