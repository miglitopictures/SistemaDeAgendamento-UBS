import json
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # talvez usar get realpath
PACIENTES_PATH = os.path.join(ROOT_DIR, "dados", "pacientes.json")
PROFISSIONAIS_PATH = os.path.join(ROOT_DIR, "dados", "profissionais.json")
CONSULTAS_PATH = os.path.join(ROOT_DIR, "dados", "consultas.json")

def carregar_dados(arquivo_json):
    """Carrega os dados do arquivo JSON ou cria um novo se não existir."""
    if os.path.exists(arquivo_json):
        with open(arquivo_json, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_dados(dados, arquivo_json):
    """Salva os dados no arquivo JSON."""
    with open(arquivo_json, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)