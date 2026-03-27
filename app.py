import json
import os
from flask import Flask, render_template, request, jsonify, session # Ferramentas do Flask
from controllers import usuario_controller, receita_controller # Importa as lógicas
from utils.persistencia import ler_dados # Importa leitura para a home

app = Flask(__name__) # Inicializa a aplicação Flask
app.secret_key = "chave_mestra_2024" # Chave para criptografar os cookies de sessão

@app.route("/") # Rota da página inicial
def index():
    dados = ler_dados() 
    # Usamos .get("receitas", []) para evitar erro caso a lista esteja vazia
    lista_receitas = dados.get("receitas", [])
    return render_template("index.html", receitas=lista_receitas, usuario=session.get("usuario"))

@app.route("/cadastrar", methods=["POST"]) # Rota de cadastro
def cadastrar():
    dados = request.get_json() # Pega os dados enviados
    # Chama o controller e recebe a resposta e o status HTTP
    res, status = usuario_controller.processar_cadastro(dados.get('nickname'), dados.get('senha'))
    return jsonify(res), status # Retorna a resposta pro Front-end

@app.route("/login", methods=["POST"]) # Rota de login
def login():
    dados = request.get_json() # Pega nickname e senha do JSON
    # Chama o controller para validar
    res, status = usuario_controller.processar_login(dados.get('nickname'), dados.get('senha'))
    return jsonify(res), status # Retorna a resposta pro Front-end

@app.route("/logout", methods=["POST"]) # Rota de sair
def logout():
    session.pop("usuario", None) # Remove os dados do usuário da sessão
    return jsonify({"mensagem": "Saiu!"}) # Avisa que deslogou

@app.route("/curtir/<int:receita_id>", methods=["POST"]) # Rota de curtir
def curtir(receita_id):
    user = session.get("usuario") # Verifica se tem alguém logado
    if not user: return jsonify({"erro": "Logue primeiro"}), 401
    res = receita_controller.alternar_curtida(receita_id, user["nickname"]) 
    return jsonify(res) # Retorna os novos dados de curtida

@app.route("/comentario/<int:comentario_id>", methods=["DELETE"]) 
def excluir_comentario(comentario_id):
    user = session.get("usuario") # Pega usuário da sessão
    if not user: return jsonify({"erro": "Logue primeiro"}), 401
    
    res, status = receita_controller.remover_comentario(comentario_id, user)
    return jsonify(res), status 

if __name__ == "__main__": 
    app.run(debug=True)