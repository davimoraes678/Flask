from flask import Flask, jsonify, request, render_template, redirect, url_for
import dados
import json

biblioteca = dados.carregar_do_arquivo()
app = Flask(__name__)

@app.route('/api/biblioteca', methods=['GET', 'POST'])
@app.route('/api/biblioteca/<isbn>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manipular_livro(isbn=None):
    if request.method == 'GET':
        if isbn is None:
            return jsonify(biblioteca)
        else:
            for livro in biblioteca:
                if livro['isbn'] == isbn:
                    return jsonify(livro)
        return jsonify("Livro não encontrado"), 404
        
    elif request.method == 'POST':
        novo_livro = request.get_json()
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return jsonify("Livro criado com sucesso"), 201
        
    elif request.method == 'DELETE':
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                biblioteca.remove(livro)
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("Livro deletado com sucesso"), 200
        return jsonify("Livro não encontrado"), 404
                
    elif request.method == 'PUT':
        novo_livro = request.get_json()
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                for key, value in novo_livro.items():
                    livro[key] = value
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("Livro Alterado com Sucesso"), 200
        return jsonify("Livro não encontrado"), 404

@app.route('/')
def home():
    return render_template('biblioteca.html', variavel1=biblioteca)

@app.route('/biblioteca/atualizar', methods=['GET', 'POST'])
def interface_atualizar():

    pass

@app.route('/biblioteca/criar', methods=['GET', 'POST'])
def interface_criar():
    global biblioteca
    biblioteca = dados.carregar_do_arquivo()
    if request.method == 'POST':
        novo_livro = {
            "isbn": request.form.get('isbn'),
            "titulo": request.form.get('titulo'),
            "autor": request.form.get('autor'),
            "genero": request.form.get('genero'),
            "ano_publicacao": request.form.get('ano_publicacao'),
            "editora": request.form.get('editora'),
            "paginas": request.form.get('paginas'),
            "status": request.form.get('status'),
            "localizacao": request.form.get('localizacao')
        }
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return redirect(url_for('home')) 
    else:
        return render_template('criar_livro.html')

if __name__ == '__main__':
    app.run(debug=True)