import random 
import pandas as pd
import folium
import numpy as np
from folium.plugins import LocateControl, MarkerCluster

# Read csv files with the antennas information
df1 = pd.read_csv('raw_data/ribeirao.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz', 'DataLicenciamento'])
df2 = pd.read_csv('raw_data/perdoes.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz', 'DataLicenciamento'])
df3 = pd.read_csv('raw_data/canaverde.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz', 'DataLicenciamento'])
df4 = pd.read_csv('raw_data/nepomuceno.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz', 'DataLicenciamento'])
df5 = pd.read_csv('raw_data/lavras.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz', 'DataLicenciamento'])
df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

# Remove blank spaces on operators names
df['NomeEntidade'] = df['NomeEntidade'].str.rstrip()

# Filter per valid operator
valid_operators = ['CLARO S.A.', 'TIM S A', 'TIM S/A', 'TELEFONICA BRASIL S.A.']
filter = df['NomeEntidade'].isin(valid_operators)
df_filtered = df[filter]


# Create a map centralized in Brazil
map_br = folium.Map(location=[-15.788497, -47.879873], zoom_start=4, tiles='http://mt1.google.com/vt/lyrs=y&z={z}&x={x}&y={y}', attr='Google', name='Satelite')

# Add a layer of terrain
folium.TileLayer('https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}&hl=en&gl=en&x={x}&y={y}&z={z}&s=Ga', attr='Google', name='Relevo').add_to(map_br)

# Adiciona o controle de camadas ao map_br
folium.LayerControl().add_to(map_br)
LocateControl().add_to(map_br)

# Descreve as tecnoogias
df_filtered.loc[df_filtered['Tecnologia'].isna(), 'Tecnologia'] = "Indefinido"
df_filtered['Tecnologia'] = df_filtered['Tecnologia'].replace({'NR': 'NR (5G)', 'LTE': 'LTE (4G)', 'WCDMA': 'WCDMA (3G)', 'GSM': 'GSM (2G)'})

# Cria um conjunto de coordenadas já adicionadas ao map_br
added_coordinates = set()

# Percorre o DataFrame e monta os pontos das torres no map_br
for index, row in df_filtered.iterrows():
    if (row['Latitude'], row['Longitude']) not in added_coordinates and not np.isnan(row['Latitude']) and not np.isnan(row['Longitude']):
        operator_label = row['NomeEntidade']

        if operator_label == 'TELEFONICA BRASIL S.A.':
            vivo_url = 'doc/vivo.png'
            vivo_ico = folium.features.CustomIcon(vivo_url, icon_size=(30, 34))
            operator = 'VIVO'
            icon = vivo_ico
        elif operator_label == 'CLARO S.A.':
            operator = 'CLARO'
            claro_url = 'doc/claro.png'
            claro_ico = folium.features.CustomIcon(claro_url, icon_size=(30, 34))
            icon = claro_ico
        elif operator_label == 'TIM S A' or operator_label == 'TIM S/A':
            operator = 'TIM'
            tim_url = 'doc/tim.png'
            tim_ico = folium.features.CustomIcon(tim_url, icon_size=(30, 34))
            icon = tim_ico

        latitude = row['Latitude']
        longitude = row['Longitude']
        altura = row['AlturaAntena']
        
        html = f"<p><strong>operator:</strong> {operator_label}</p>"
        html += f"<p><strong>Endereço:</strong> {row['EnderecoEstacao']} </p>"
        html += "<table><tr style='background-color: gray; color: white;'><th style='width: 200px; padding: 10px;'>Tecnologia</th><th style='width: 200px; padding: 10px;'>Frequência</th><th style='width: 200px; padding: 10px;'>Altura</th><th style='width: 200px; padding: 10px;'>Licenciamento</th></tr>"

        # Filtra as linhas com as mesmas coordenadas e operator
        df_unique = df_filtered[(df_filtered['NomeEntidade'] == row['NomeEntidade']) & (df_filtered['Latitude'] == row['Latitude']) & (df_filtered['Longitude'] == row['Longitude'])].copy()

        # Agrupa por tecnologia e frequência e pega a altura da antena
        group = df_unique.groupby(['Tecnologia', 'FreqTxMHz', 'DataLicenciamento']).agg({'AlturaAntena': 'max'}).reset_index()

        # Ordena os dados por 'FreqTxMHz'
        group = group.sort_values(by='FreqTxMHz')

        # Adiciona as informações da tabela
        for technology, frequency, heights, data in zip(group['Tecnologia'], group['FreqTxMHz'], group['AlturaAntena'], group['DataLicenciamento']):
            html += f"<tr><td style='text-align: left;'>{technology}</td><td style='text-align: left;'>{frequency} Mhz</td><td style='text-align: center;'>{heights} m</td><td style='text-align: center;'>{data}</td></tr>"

        html += "</table>"
        html += f"<p><strong>Localização: </strong> {latitude},{longitude}</p>"
        added_coordinates.add((latitude, longitude))

        # Adiciona um pouco de aleatoriedade nas coordenadas para evitar que os pontos fiquem sobrepostos
        latitude += random.uniform(-0.0002, 0.0002)
        longitude += random.uniform(-0.0002, 0.0002)

        folium.Marker(location=[latitude, longitude], tooltip=operator,  icon=icon, popup=html).add_to(map_br)

# Salvar o map_br em um arquivo HTML
map_br.save('index.html')
