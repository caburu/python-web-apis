'''
Programa para demonstrar a utilização do Python para obter dados
disponíveis na Web.

O usuário digita um termo a ser buscado na Wikipedia em Português e,
caso seja encontrado, a seção de introdução da página na Wikipedia é
exibida (em formato texto simples).

Obs1: para exibir todo o conteúdo da página na Wikipedia basta retirar
a chave "exintro" do dicionario 'consulta' na função 'montar_endereco'

Obs2: para buscar na Wikipedia em outros idiomas basta trocar o endereço
na variavel 'endereco_base' da função 'montar_endereco'. Exemplo: em
inglês o endereço é: "https://en.wikipedia.org/w/api.php?"

Fontes:
https://www.mediawiki.org/wiki/API:Main_page
https://en.wikipedia.org/w/api.php?action=help&modules=query%2Bextracts

@author: Julio Cesar Alves (DCC/UFLA)
@date: 2017-03
'''

import urllib.parse, urllib.request, json

def montar_endereco(palavra):
	endereco_api = "https://pt.wikipedia.org/w/api.php?"
	consulta = {"action":"query","titles":palavra, "prop":"extracts", "exintro":1, "explaintext":1, "format":"json"}
	endereco_final = endereco_api + urllib.parse.urlencode(consulta)
	return endereco_final
	
def carregar_dados(endereco):
	dados_crus = urllib.request.urlopen(endereco).read().decode()
	dicionario = json.loads(dados_crus)
	return dicionario
	
def retornou_dados(dados):
	chaves = list(dados["query"]["pages"].keys())
	codigo = chaves[0] 
	return codigo != "-1"

def exibir_conteudo(dados):
	if retornou_dados(dados):		
		chaves = list(dados["query"]["pages"].keys())
		codigo = chaves[0] 
		print(dados["query"]["pages"][codigo]["title"])
		conteudo = dados["query"]["pages"][codigo]["extract"]
		if conteudo != "":
			print(conteudo)
		else:
			print("Conteúdo vazio (talvez seja uma página de redirecionamento)")
			print("Verifique acentuação ou tente um sinônimo")
	else:
		print("Termo não encontrado na Wikipedia!")

def exibir_dados_formatados(dados):
	print(json.dumps(dados, indent=4, sort_keys=True))

# Subprograma Principal

print("\t\tConsulta WIKIPEDIA (Português)\n\n")

pesquisa = input("Digite um termo a buscar: ")
while pesquisa != "":
	endereco = montar_endereco(pesquisa)
	dados = carregar_dados(endereco)
	#exibir_dados_formatados(dados)
	exibir_conteudo(dados)	
	pesquisa = input("\nDigite um termo a buscar: ")






