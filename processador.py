import pandas as pd
import folium
from folium.plugins import DualMap, Fullscreen, LocateControl
from folium.plugins import MeasureControl

# Ler os arquivos CSV com as informações das antenas
df1 = pd.read_csv('raw_data/ribeirao.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz'])
df2 = pd.read_csv('raw_data/perdoes.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz'])
df3 = pd.read_csv('raw_data/canaverde.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz'])
df4 = pd.read_csv('raw_data/nepomuceno.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz'])
df5 = pd.read_csv('raw_data/lavras.csv', sep=',', encoding='iso-8859-1', usecols=['NomeEntidade', 'EnderecoEstacao', 'Latitude', 'Longitude', 'AlturaAntena', 'Tecnologia', 'FreqTxMHz'])
df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)


operadoras_validas = ['CLARO S.A.', 'TIM S A                                                                                                                 ',
                       'TIM S/A', 'TELEFONICA BRASIL S.A.']
filtro = df['NomeEntidade'].isin(operadoras_validas)
df_filtrado = df[filtro]


# Criar um mapa centrado no Brasil
mapa = folium.Map(location=[-15.788497, -47.879873], zoom_start=4, name='Satelite', tiles='http://mt1.google.com/vt/lyrs=y&z={z}&x={x}&y={y}', attr='Google')

# Adiciona uma camada de relevo usando OpenStreetMap
folium.TileLayer('https://tile.opentopomap.org/{z}/{x}/{y}.png', attr='OpenStreetMap', name='Relevo').add_to(mapa)

# Adiciona o controle de camadas ao mapa
folium.LayerControl().add_to(mapa)
LocateControl().add_to(mapa)


endereco_tecnologias_frequencias = {}
df_filtrado.loc[df_filtrado['Tecnologia'].isna(), 'Tecnologia'] = "Indefinido"
df_filtrado.loc[:, 'Tecnologia'] = df_filtrado['Tecnologia'].replace({'LTE': 'LTE (4G)'})
df_filtrado.loc[:, 'Tecnologia'] = df_filtrado['Tecnologia'].replace({'GSM': 'GSM (2G)'})
df_filtrado.loc[:, 'Tecnologia'] = df_filtrado['Tecnologia'].replace({'WCDMA': 'WCDMA (3G)'})

# Percorre o DataFrame e monta os pontos das torres no mapa
for index, row in df_filtrado.iterrows():

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
    elif operadora_label == 'TIM S A' or operadora_label == 'TIM S A                                                                                                                 ' or operadora_label == 'TIM S/A':
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

    # Filtra as linhas com o mesmo endereço e operadora
    df_unico = df_filtrado[(df_filtrado['NomeEntidade'] == operadora_label) & (df_filtrado['EnderecoEstacao'] == row['EnderecoEstacao'])].copy()

    # Agrupa por tecnologia e frequência e cria uma lista de alturas
    agrupado = df_unico.groupby(['Tecnologia', 'FreqTxMHz']).agg({'AlturaAntena': list}).reset_index()

    # Ordena os dados por 'FreqTxMHz'
    agrupado = agrupado.sort_values(by='FreqTxMHz')

    # Adiciona as informações da tabela
    for tecnologia, frequencia, alturas in zip(agrupado['Tecnologia'], agrupado['FreqTxMHz'], agrupado['AlturaAntena']):
        if isinstance(frequencia, list):
            #html += f"<tr><td>{str(tecnologia)}</td><td>{', '.join(str(freq) for freq in frequencia)}</td><td>{', '.join(str(altura) for altura in alturas)}</td></tr>"
            html += f"<tr><td>{str(tecnologia)}</td><td>{', '.join(str(freq) for freq in frequencia)}</td><td>{', '.join(str(altura) for altura in alturas)}</td></tr>"
        else:
            html += f"<tr><td>{str(tecnologia)}</td><td>{frequencia}</td><td>{altura}</td></tr>"

    html += "</table>"
    html += f"<p>{latitude},{longitude}</p>"

    folium.Marker(location=[latitude, longitude], tooltip=operadora,  icon=icone, popup=html).add_to(mapa)


# Icone Cowboy
icon_url = 'doc/emoji_chapeu.png'
cowboy = folium.features.CustomIcon(icon_url, icon_size=(35, 35))

# Sua geolocalização
coord = [-21.15194196941009, -45.092157664716275]

# Coloca você no mapa
folium.Marker(location=[coord[0], coord[1]], tooltip="Você",  icon=cowboy, popup="Fazenda Açude").add_to(mapa)

# Salvar o mapa em um arquivo HTML
mapa.save('mapa_antenas.html')