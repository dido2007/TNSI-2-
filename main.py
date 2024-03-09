from flask import Flask, render_template, request, jsonify

from search import search_keywords

app = Flask(__name__)


@app.route('/')
def index():
    message = "Hello from Flask!"
    return render_template('index.html', message=message)


@app.route('/keywording', methods=['POST'])
def handle_form_submission():
    keyword = request.form.get('key')
    print(keyword)
    # Utiliser la fonction de recherche pour obtenir les résultats basés sur le mot-clé
    results = search_keywords(keyword)
    print(results)
    # Renvoyer les résultats en JSON
    if len(results) == 0:
        return jsonify({"error": "No results found"})
    return jsonify(results)



if __name__ == '__main__':
    app.run()
