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

