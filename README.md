## Mapa de sinais de operadoras de celular
Mapa interativo que mostra informações de transmissão de sinais de redes de celular

[Ver mapa online (CLIQUE AQUI)](https://wesleyabreu.github.io/mapa-sinais-operadoras)

Ele vem carregado com o processamento de dados de planilhas baixadas no site da ANATEL com infomações sobre licenciamento de radiofrequência das cidades de Perdões, Cana Verde, Lavras, Ribeirão Vermelho e Nepomuceno, todas cidades localizadas em Minas Gerais, o objetivo principal desse projeto é consultar disponibilidade de internet movél para zona rural dessa região.

Porém qualquer um pode modificar e colocar a cidade que queira fazer a ilustração das torres obtendo no site https://sistemas.anatel.gov.br/se/public/view/b/licenciamento.php?view=licenciamento
o download do arquivo CSV filtrando sua localidade e colocando no código e executando o programa que gerara um arquivo HTML para abrir no navegador

<img width="100%" src="doc/printscreen.png">

## Bibliotecas do Python usadas
- Pandas (Leitura e manipulação de arquivos CSV)
- Folium (Implementação do mapa)


Ao executar o processador.py ele demora um tempinho e aparece alguns warning, mas tudo bem só aguardar e depois abrir o HTML gerado.

## Documentação do código:

### Leitura dos dados:
O código lê dados de antenas de diferentes localidades a partir de arquivos CSV e os armazena em dataframes do Pandas.

### Limpeza e filtragem:
São removidos espaços em branco à direita do nome das operadoras e se filtram somente as operadoras válidas.

### Criação do Mapa:
É criado um objeto mapa usando a biblioteca Folium, centrado em coordenadas do Brasil e é adicionada uma camada de relevo do Google Maps.

### Controle de Camadas e Localização: 
É adicionado um controle de camadas e um controle de localização. 

### Descrição de Tecnologias:
As tecnologias das antenas são padronizadas e dados ausentes são preenchidos.

### Adição de Pontos ao Mapa:
São adicionados marcadores pra cada antena. Cada marcador é personalizado com um ícone específico para a operadora e contém informações como endereço, tecnologia, frequência, altura e data de licenciamento.


## Cellular operator signal map

Interactive map showing cellular network signal transmission information

[View online map (CLICK HERE)](https://wesleyabreu.github.io/mapa-sinais-operadoras)

It comes loaded with data processing from spreadsheets downloaded from the ANATEL website with information about radio frequency licensing in the cities of Perdões, Cana Verde, Lavras, Ribeirão Vermelho and Nepomuceno, all cities located in Minas Gerais, the main objective of this project is to consult availability of mobile internet for rural areas in this region.

However, anyone can modify and add the city they want to illustrate the towers on the website https://sistemas.anatel.gov.br/se/public/view/b/licenciamento.php?view=licenciamento
downloading the CSV file by filtering its location and placing it in the code and running the program that will generate an HTML file to open in the browser

<img width="100%" src="doc/printscreen.png">


## Python libraries used
- Pandas (Reading and manipulating CSV files)
- Folium (Map implementation)

When running processor.py it takes a while and some warnings appear, but it's okay to just wait and then open the generated HTML.


## Code documentation:

### Data reading:
The code reads antenna data from different locations from CSV files and stores it in Pandas dataframes.

### Cleaning and filtering:
Blank spaces to the right of the operator names are removed and only valid operators are filtered.

### Map Creation:
A map object is created using the Folium library, centered on Brazil coordinates and a Google Maps relief layer is added.

### Layer and Location Control:
A layer control and a location control are added.

### Description of Technologies:
Antenna technologies are standardized and missing data is filled in.

### Adding Points to the Map:
Markers are added for each antenna. Each marker is personalized with a carrier-specific icon and contains information such as address, technology, frequency, height, and licensing date.