'''
Programa para demonstrar a utilização do Python para obter dados
disponíveis na Web.

O usuário digita uma localidade a ser buscado no Yahoo Weather e, caso 
seja encontrado, são exibidos dados deo tempo daquele local.

Descomente a chamada da função exibir_dados_formatados para ver todos
os dados que são retornados. Assim você poderá alterar o programa para
exibir diversas outras informações, como umidade, pressão, velocidade do
vento, etc.

Obs: a licença do Yahoo diz que aplicações que acessam a API devem
exibir a logo da Yahoo com link para o site. Como o programa é em
linha de comando, para seguir a licença, está sendo mostrada a
frase "Powered by Yahoo!" e o link.

Referência:
https://developer.yahoo.com/weather/

@author: Julio Cesar Alves (DCC/UFLA)
@date: 2017-03
'''

import urllib.parse, urllib.request, json

def montar_endereco(local):	
	endereco_base = "https://query.yahooapis.com/v1/public/yql?"
	consulta_yql = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='%s') and u='c'" % (local)
	consulta = {"q":consulta_yql, "format":"json"}
	endereco_final = endereco_base + urllib.parse.urlencode(consulta)
	return endereco_final
	
def carregar_dados(endereco):
	dados_crus = urllib.request.urlopen(endereco).read()
	dicionario = json.loads(dados_crus.decode())
	return dicionario

def exibir_dados_yahoo():
	print("\tPowered by Yahoo!\thttps://www.yahoo.com/?ilc=401")

def retornou_dados(dados):
	return dados["query"]["results"] != None

def exibir_cidade(dados):
	lugar = dados["query"]["results"]["channel"]["location"]
	print("Cidade:", lugar["city"], "(" + lugar["region"] + " ) -", lugar["country"])

def exibir_tempo_agora(dados):
	tempo_agora = dados["query"]["results"]["channel"]["item"]["condition"]
	print("Atual:", tempo_agora["temp"], "ºC -", tempo_agora["text"])	
	
def exibir_previsoes(dados):
	print("Previsões:")
	previsoes = dados["query"]["results"]["channel"]["item"]["forecast"]
	for previsao in previsoes:
		print("\tDia ", previsao["date"] + ":", previsao["low"], "a", previsao["high"], "ºC -", previsao["text"])	

def exibir_dados(dados):
	if retornou_dados(dados):
		print()
		exibir_cidade(dados)		
		exibir_dados_yahoo()
		print()
		exibir_tempo_agora(dados)
		print()
		exibir_previsoes(dados)
	else:
		print("Cidade não encontrada no Yahoo Weather")

def exibir_dados_formatados(dados):
	print(json.dumps(dados, indent=4, sort_keys=True))

# Subprograma Principal

print("\t\tConsulta Previsao do Tempo\n")
exibir_dados_yahoo()

pesquisa = input("\nDigite a cidade: ")
while pesquisa != "":
	endereco = montar_endereco(pesquisa)
	dados = carregar_dados(endereco)
	#exibir_dados_formatados(dados)
	exibir_dados(dados)			
	pesquisa = input("\nDigite a cidade: ")
