import json
import os

# Define onde o banco de dados (JSON) vai ficar
CAMINHO_BD = "dados.json" 

def ler_dados():
    """Lê os dados do arquivo JSON. Se não existir, retorna a estrutura básica."""
    if not os.path.exists(CAMINHO_BD):
        return {"usuarios": [], "receitas": []}
    
    try:
        with open(CAMINHO_BD, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"usuarios": [], "receitas": []}

def salvar_dados(dados):
    """Salva o dicionário de dados no arquivo JSON."""
    with open(CAMINHO_BD, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)