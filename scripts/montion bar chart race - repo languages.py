import pandas as pd
import numpy as np
import bar_chart_race as bcr
import warnings
warnings.filterwarnings('ignore')

# Carregar os dados
repos_data = pd.read_csv('repos_data.csv')

repos_data = repos_data[~repos_data['language'].isin(['HTML', 'CSS'])]

def gerar_bar_chart_race_repos(repos_data):
    # Converter datas para datetime
    repos_data['created_at'] = pd.to_datetime(repos_data['created_at'], errors='coerce')
    
    # Extrair o ano
    repos_data['ano'] = repos_data['created_at'].dt.year
    
    # Agrupar por ano e linguagem, contando quantos repositórios existem em cada grupo
    df_agrupado = (
        repos_data
        .groupby(['ano', 'language'])
        .size()  # Contagem de repositórios
        .reset_index(name='total_repos')
    )
    
    # Criar tabela pivô (linhas=ano, colunas=linguagem, valores=quantidade de repositórios)
    df_pivot = df_agrupado.pivot(index='ano', columns='language', values='total_repos')
    
    # Preencher valores ausentes com 0
    df_pivot.fillna(0, inplace=True)
    
    # Calcular valor acumulado (para não "zerar" ao longo dos anos, se desejado)
    df_pivot = df_pivot.cumsum()
    
    # Substituir zeros por NaN para evitar exibir barras com valor zero
    df_pivot.replace(0, np.nan, inplace=True)
    
    # Remover colunas que estejam completamente vazias (se alguma linguagem não aparece em nenhum ano)
    df_pivot.dropna(axis=1, how='all', inplace=True)
    
    # Converter índice (anos) para inteiro, para não exibi-los como float
    df_pivot.index = df_pivot.index.astype(int)
    
    # Gerar o bar chart race
    bcr.bar_chart_race(
        df=df_pivot,
        filename='repos_bar_chart_race2.gif',
        orientation='h',
        sort='desc',
        n_bars=10,
        fixed_order=False,
        fixed_max=True,
        steps_per_period=30,   # Movimentos mais suaves
        period_length=2000,    # Tempo maior para melhor visualização
        period_label={'x': 0.95, 'y': 0.1, 'ha': 'right', 'va': 'center', 'size': 14, 'color': 'black'},
        title='Linguagens Mais Usadas ao Longo dos Anos',
        bar_label_size=10,
        tick_label_size=12,
        figsize=(6, 4),        # Formato mais compacto
        cmap='dark24',         # Paleta de cores
        dpi=144                # Melhor resolução
    )
    print("Bar chart race criado com sucesso!")

# Executar a função
gerar_bar_chart_race_repos(repos_data)
