import json 
from os import path 



ROOT_DIR = path.abspath(path.join(path.dirname(__file__), '..'))
PACIENTES_PATH = path.join(ROOT_DIR, "dados", "pacientes.json")
PROFISSIONAIS_PATH = path.join(ROOT_DIR, "dados", "profissionais.json")
CONSULTAS_PATH = path.join(ROOT_DIR, "dados", "consultas.json")




def carregar_dados(arquivo_json):

    if path.exists(arquivo_json):
        with open(arquivo_json, "r", encoding="utf-8") as f: 
            return json.load(f)
    
    return [] 


def salvar_dados(dados, arquivo_json):
    
    with open(arquivo_json, "w", encoding="utf-8") as f: 
        json.dump(dados, f, indent=4, ensure_ascii=False)


def buscar_por_valor(valor, chave, lista: list):
    for item in lista:
        if item[chave] == valor:
            return item

    return None