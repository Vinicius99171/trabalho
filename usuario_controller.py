from flask import session
from utils.persistencia import ler_dados, salvar_dados
from utils.seguranca import hash_senha, verificar_senha

def processar_cadastro(nick, senha):
    dados = ler_dados()
    # Verifica duplicidade ignorando case em uma linha
    if any(u["nickname"].lower() == nick.lower() for u in dados["usuarios"]):
        return {"erro": "Nickname já existe"}, 409

    # Cria e salva o usuário diretamente na lista
    dados["usuarios"].append({
        "id": dados["proximo_usuario_id"],
        "nickname": nick,
        "senha": hash_senha(senha), # Criptografia aplicada conforme requisito
        "perfil": "comum"
    })
    
    dados["proximo_usuario_id"] += 1
    salvar_dados(dados)
    return {"mensagem": "Sucesso!"}, 201

def processar_login(nick, senha):
    dados = ler_dados()
    # Busca o usuário; se não achar, 'u' será None
    u = next((u for u in dados["usuarios"] if u["nickname"].lower() == nick.lower()), None)

    # Validação unificada: se o usuário não existe OU a senha não bate
    if not u or not verificar_senha(senha, u["senha"]):
        # Mensagem exata exigida pelo desafio: "Usuário ou senha incorreto"
        return {"erro": "Usuário ou senha incorreto"}, 401 

    # Inicia a sessão apenas com o necessário
    session["usuario"] = {"id": u["id"], "nickname": u["nickname"], "perfil": u["perfil"]}
    return {"mensagem": "Logado!", "usuario": session["usuario"]}, 200