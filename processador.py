import random
import pandas as pd
import folium
import numpy as np
from folium.plugins import LocateControl, MarkerCluster

# Ler os arquivos CSV com as informações das antenas
df1 = pd.read_csv('raw_data/ribeirao.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz'])
df2 = pd.read_csv('raw_data/perdoes.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz'])
df3 = pd.read_csv('raw_data/canaverde.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz'])
df4 = pd.read_csv('raw_data/nepomuceno.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz'])
df5 = pd.read_csv('raw_data/lavras.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz'])
df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

# Remove espaços a direita do nome das operadoras
df['NomeEntidade'] = df['NomeEntidade'].str.rstrip()

# Filtra apenas as operadoras validas
operadoras_validas = ['CLARO S.A.', 'TIM S A', 'TIM S/A', 'TELEFONICA BRASIL S.A.']
filtro = df['NomeEntidade'].isin(operadoras_validas)
df_filtrado = df[filtro]


# Criar um mapa centrado no Brasil
mapa = folium.Map(location=[-15.788497, -47.879873], zoom_start=4, tiles='http://mt1.google.com/vt/lyrs=y&z={z}&x={x}&y={y}', attr='Google', name='Satelite')

# Adiciona uma camada de relevo
folium.TileLayer('https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}&hl=en&gl=en&x={x}&y={y}&z={z}&s=Ga', attr='Google', name='Relevo').add_to(mapa)

# Adiciona o controle de camadas ao mapa
folium.LayerControl().add_to(mapa)
LocateControl().add_to(mapa)

# Descreve as tecnoogias
df_filtrado.loc[df_filtrado['Tecnologia'].isna(), 'Tecnologia'] = "Indefinido"
df_filtrado['Tecnologia'] = df_filtrado['Tecnologia'].replace({'NR': 'NR (5G)', 'LTE': 'LTE (4G)', 'WCDMA': 'WCDMA (3G)', 'GSM': 'GSM (2G)'})

# Cria um conjunto de coordenadas já adicionadas ao mapa
coordenadas_adicionadas = set()

# Percorre o DataFrame e monta os pontos das torres no mapa
for index, row in df_filtrado.iterrows():
    if (row['Latitude'], row['Longitude']) not in coordenadas_adicionadas and not np.isnan(row['Latitude']) and not np.isnan(row['Longitude']):
        operadora_label = row['NomeEntidade']

        if operadora_label == 'TELEFONICA BRASIL S.A.':
            vivo_url = 'doc/vivo.png'
            vivo_ico = folium.features.CustomIcon(vivo_url, icon_size=(30, 34))
            operadora = 'VIVO'
            icone = vivo_ico
        elif operadora_label == 'CLARO S.A.':
            operadora = 'CLARO'
            claro_url = 'doc/claro.png'
            claro_ico = folium.features.CustomIcon(claro_url, icon_size=(30, 34))
            icone = claro_ico
        elif operadora_label == 'TIM S A' or operadora_label == 'TIM S/A':
            operadora = 'TIM'
            tim_url = 'doc/tim.png'
            tim_ico = folium.features.CustomIcon(tim_url, icon_size=(30, 34))
            icone = tim_ico

        latitude = row['Latitude']
        longitude = row['Longitude']
        altura = row['AlturaAntena']
        
        html = f"<p>{operadora_label}</p>"
        html += f"<p>{row['EnderecoEstacao']} </p>"
        html += "<table><tr><th>Tecnologia</th><th>Frequência</th><th>Altura</th></tr>"

        # Filtra as linhas com as mesmas coordenadas e operadora
        df_unico = df_filtrado[(df_filtrado['NomeEntidade'] == row['NomeEntidade']) & (df_filtrado['Latitude'] == row['Latitude']) & (df_filtrado['Longitude'] == row['Longitude'])].copy()

        # Agrupa por tecnologia e frequência e pega a altura da antena
        agrupado = df_unico.groupby(['Tecnologia', 'FreqTxMHz']).agg({'AlturaAntena': 'max'}).reset_index()

        # Ordena os dados por 'FreqTxMHz'
        agrupado = agrupado.sort_values(by='FreqTxMHz')

        # Adiciona as informações da tabela
        for tecnologia, frequencia, alturas in zip(agrupado['Tecnologia'], agrupado['FreqTxMHz'], agrupado['AlturaAntena']):
            html += f"<tr><td>{str(tecnologia)}</td><td>{frequencia}</td><td>{altura}</td></tr>"

        html += "</table>"
        html += f"<p>{latitude},{longitude}</p>"
        coordenadas_adicionadas.add((latitude, longitude))

        # Adiciona um pouco de aleatoriedade nas coordenadas para evitar que os pontos fiquem sobrepostos
        latitude += random.uniform(-0.0002, 0.0002)
        longitude += random.uniform(-0.0002, 0.0002)

        folium.Marker(location=[latitude, longitude], tooltip=operadora,  icon=icone, popup=html).add_to(mapa)

# Salvar o mapa em um arquivo HTML
mapa.save('index.html')