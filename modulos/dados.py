import json # Módulo nativo do Python para codificar e decodificar dados JSON.
from os import path # Módulo nativo usado para interagir com o sistema, "path" especificamente para manipular caminhos (paths).

'''Este módulo lida com o armazenamento e carregamento de dados nos arquivos JSON.'''


# CONSTANTES #

ROOT_DIR = path.abspath(path.join(path.dirname(__file__), '..'))
PACIENTES_PATH = path.join(ROOT_DIR, "dados", "pacientes.json")
PROFISSIONAIS_PATH = path.join(ROOT_DIR, "dados", "profissionais.json")
CONSULTAS_PATH = path.join(ROOT_DIR, "dados", "consultas.json")


# FUNCOES #

def carregar_dados(arquivo_json):
    """Carrega os dados do arquivo JSON ou cria um novo se não existir."""
    # Verifica se o arquivo existe antes de tentar abri-lo.
    if path.exists(arquivo_json):
        # Abre o arquivo no modo de leitura ('r') com a codificação correta ('utf-8').
        with open(arquivo_json, "r", encoding="utf-8") as f: # usa 'f' como pseudonimo
            # lê o conteúdo do arquivo e o converte de JSON para Python.
            return json.load(f)
    
    return [] # Se o arquivo não existir, retorna uma lista vazia.


def salvar_dados(dados, arquivo_json):
    """Salva os dados no arquivo JSON."""
    # Abre o arquivo no modo de escrita ('w'). 
    # O modo 'w' cria o arquivo se não existir ou apaga o conteúdo existente se já existir.
    with open(arquivo_json, "w", encoding="utf-8") as f: # usa 'f' como pseudonimo

        # transforma o objeto Python ('dados') para o formato JSON e o grava no arquivo.
        json.dump(dados, f, indent=4, ensure_ascii=False)

        # Parâmetros adicionais para formatação:
        # 1. indent=4: Formata o JSON com 4 espaços de indentação, tornando-o legível por humanos.
        # 2. ensure_ascii=False: Garante que caracteres especiais (como acentos) sejam 
        #    salvos como são, sem usar sequências de escape \uXXXX.


def buscar_por_valor(valor, chave, lista: list):
    '''Retorna o primeiro objeto dentro da lista com o valor e a chave especificada no input.'''

    # faz um loop em todos os itens da lista
    for item in lista:
        # se o item tem, associado a chave especificada, o valor especificado.
        if item[chave] == valor:
            return item # retorna o item

    return None # se chegar ate aqui depois de varrer a lista, retornar None