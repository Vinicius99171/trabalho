from utils.persistencia import ler_dados, salvar_dados

def usuario_pode_excluir(user, autor_id):
    """Simplificado com operador OR: True se for admin OU se for o dono."""
    return user["perfil"] == "admin" or user["id"] == autor_id

def alternar_curtida(receita_id, nick):
    dados = ler_dados()
    # Busca a receita diretamente (ou retorna None se não achar)
    r = next((r for r in dados["receitas"] if r["id"] == receita_id), None)
    
    if r:
        # Lógica de toggle em uma linha: remove se já existe, senão adiciona
        r["curtidas"].remove(nick) if nick in r["curtidas"] else r["curtidas"].append(nick)
        salvar_dados(dados)
        return {"total_curtidas": len(r["curtidas"]), "curtiu": nick in r["curtidas"]}
    return None

def remover_comentario(com_id, user):
    dados = ler_dados()
    for receita in dados["receitas"]:
        # Busca o comentário dentro da lista da receita
        com = next((c for c in receita["comentarios"] if c["id"] == com_id), None)
        
        if com:
            if not usuario_pode_excluir(user, com["autor_id"]):
                return {"erro": "Sem permissão"}, 403
            
            receita["comentarios"].remove(com)
            salvar_dados(dados)
            return {"mensagem": "Removido"}, 200
            
    return {"erro": "Não encontrado"}, 404