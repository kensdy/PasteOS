from flask import Flask, render_template, request, redirect, url_for
import json
import uuid

app = Flask(__name__)

# Caminho para o arquivo JSON que armazenará os pastes
JSON_FILE = 'pastes.json'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        visibility = request.form.get('visibility', 'public')  # Público é o padrão

        paste_id = str(uuid.uuid4())  # Gera um GUID único para o paste

        # Carrega os pastes existentes do arquivo JSON
        try:
            with open(JSON_FILE, 'r') as file:
                pastes = json.load(file)
        except FileNotFoundError:
            pastes = []

        # Adiciona o novo paste à lista
        pastes.append({
            'id': paste_id,
            'title': title,
            'content': content,
            'visibility': visibility,
            'author': 'Usuário Anônimo'  # Adicione a lógica para obter o autor se estiver logado
        })

        # Salva a lista atualizada de pastes de volta ao arquivo JSON
        with open(JSON_FILE, 'w') as file:
            json.dump(pastes, file, indent=2)

        # Redireciona para a página do paste recém-criado
        return redirect(url_for('view_paste', paste_id=paste_id))

    return render_template('create.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search'].lower()

        # Carrega os pastes existentes do arquivo JSON
        try:
            with open(JSON_FILE, 'r') as file:
                pastes = json.load(file)
        except FileNotFoundError:
            pastes = []

        # Filtra os pastes com base na pesquisa e visibilidade
        filtered_pastes = [
            paste for paste in pastes if
            (search_term in paste['title'].lower() or
             search_term in paste['content'].lower()) and
            (paste['visibility'] == 'public' or ('user_logged_in_logic_here' and paste['visibility'] != 'unlisted'))
        ]

        if not filtered_pastes:
            return render_template('search.html', no_pastes_found=True)

        return render_template('search.html', pastes=filtered_pastes)

    return render_template('search.html', pastes=[])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/view/<paste_id>')
def view_paste(paste_id):
    # Carrega os pastes existentes do arquivo JSON
    try:
        with open(JSON_FILE, 'r') as file:
            pastes = json.load(file)
    except FileNotFoundError:
        pastes = []

    # Procura o paste pelo ID
    selected_paste = next((paste for paste in pastes if paste['id'] == paste_id), None)

    if selected_paste:
        visibility = selected_paste.get('visibility', 'public')  # Se 'visibility' não existir, assume 'public'

        if visibility == 'public' or 'user_logged_in_logic_here':
            return render_template('view_paste.html', paste=selected_paste)
        else:
            return render_template('view_paste_password.html', paste=selected_paste)
    else:
        return 'Paste não encontrado'

if __name__ == "__main__":
    app.run(debug=True)

# Substitua app.run(debug=True) por app.run(host='0.0.0.0', port=81) para tornar o site público
