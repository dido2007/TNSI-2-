from flask import Flask, render_template, request, jsonify
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

app = Flask(__name__)

mots_inutiles = set(stopwords.words('english') + stopwords.words('french'))

data = [
    {
        "title": "Elon Musk - Wikipedia",
        "description": "Elon Reeve Musk (/ˈiːlɒn/; EE-lon; born June 28, 1971) is a businessman and investor. He is the founder, chairman, CEO, and CTO of SpaceX; angel investor, CEO, product architect, and former chairman of Tesla, Inc.; owner, executive chairman, and CTO of X Corp.; founder of the Boring Company ...",
        "url": "https://en.wikipedia.org/wiki/Elon_Musk"
    },
    {
        "title": "Vladimir Putin - Wikipedia",
        "description": "Vladimir Vladimirovich Putin (Russian: Владимир Владимирович Путин, [vɫɐˈdjimʲɪr vɫɐˈdjimʲɪrəvʲɪtɕ ˈputʲɪn]; born 7 October 1952) is a Russian politician and former intelligence officer who is serving as the president of Russia, a position he has held since 7 May 2012...",
        "url": "https://en.wikipedia.org/wiki/Vladimir_Putin"
    },
    {
        "title": "Donald Trump - Wikipedia",
        "description": "Donald John Trump (born June 14, 1946) is an American politician, media personality, and businessman who served as the 45th president of the United States from 2017 to 2021...",
        "url": "https://en.wikipedia.org/wiki/Donald_Trump"
    },
    {
        "title": "Emmanuel Macron - Wikipedia",
        "description": "Emmanuel Jean-Michel Frédéric Macron (French: [emanɥɛl ʒɑ̃ miʃɛl fʁedeʁik makʁɔ̃]; born 21 December 1977) is a French politician who has been serving as the president of France and ex officio co-prince of Andorra since 14 May 2017...",
        "url": "https://en.wikipedia.org/wiki/Emmanuel_Macron"
    }
]

@app.route('/')
def index():
    message = "Hello from Flask!"
    return render_template('index.html', message=message)

@app.route('/keywording', methods=['POST'])
def handle_form_submission():
    if request.method == 'POST':
        keyword = request.form.get('key')
        mots = keyword.split()
        mots_filtres = [mot for mot in mots if mot.lower() not in mots_inutiles] 
        mots_filtres_uniques = list(set(mots_filtres)) 
        print("Mots-clés reçus (filtrés) :", mots_filtres_uniques)
        return "Données reçues avec succès !" 

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run()
