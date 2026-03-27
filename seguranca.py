import bcrypt # Importa a biblioteca de hash seguro

def hash_senha(senha_texto_puro: str) -> str:
    """Transforma senha comum em um hash protegido."""
    senha_bytes = senha_texto_puro.encode('utf-8') 
    salt = bcrypt.gensalt() 
    hash_bytes = bcrypt.hashpw(senha_bytes, salt) 
    return hash_bytes.decode('utf-8') 

def verificar_senha(senha_texto_puro: str, senha_hash: str) -> bool:
    """Compara uma tentativa de senha com o hash do banco."""
    try:
        senha_bytes = senha_texto_puro.encode('utf-8') 
        hash_bytes = senha_hash.encode('utf-8') 
        return bcrypt.checkpw(senha_bytes, hash_bytes) 
    except Exception: 
        return False 