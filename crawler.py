import queue
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import re
from collections import Counter
import json
from unidecode import unidecode
import sys



# Définition des files d'attente
urls_to_crawl = queue.Queue()
content_to_add = queue.Queue()
links_to_add = queue.Queue()
keywords_to_add = queue.Queue()

csv.field_size_limit(sys.maxsize)

stop_words = {"a","abord","absolument","afin","ah","ai","aie","aient","aies","ailleurs","ainsi","ait","allaient","allo","allons","allô","alors","anterieur","anterieure","anterieures","apres","après","as","assez","attendu","au","aucun","aucune","aucuns","aujourd","aujourd'hui","aupres","auquel","aura","aurai","auraient","aurais","aurait","auras","aurez","auriez","aurions","aurons","auront","aussi","autant","autre","autrefois","autrement","autres","autrui","aux","auxquelles","auxquels","avaient","avais","avait","avant","avec","avez","aviez","avions","avoir","avons","ayant","ayez","ayons","b","bah","bas","basee","bat","beau","beaucoup","bien","bigre","bon","boum","bravo","brrr","c","car","ce","ceci","cela","celle","celle-ci","celle-là","celles","celles-ci","celles-là","celui","celui-ci","celui-là","celà","cent","cependant","certain","certaine","certaines","certains","certes","ces","cet","cette","ceux","ceux-ci","ceux-là","chacun","chacune","chaque","cher","chers","chez","chiche","chut","chère","chères","ci","cinq","cinquantaine","cinquante","cinquantième","cinquième","clac","clic","combien","comme","comment","comparable","comparables","compris","concernant","contre","couic","crac","d","da","dans","de","debout","dedans","dehors","deja","delà","depuis","dernier","derniere","derriere","derrière","des","desormais","desquelles","desquels","dessous","dessus","deux","deuxième","deuxièmement","devant","devers","devra","devrait","different","differentes","differents","différent","différente","différentes","différents","dire","directe","directement","dit","dite","dits","divers","diverse","diverses","dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent","donc","dont","dos","douze","douzième","dring","droite","du","duquel","durant","dès","début","désormais","e","effet","egale","egalement","egales","eh","elle","elle-même","elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es","essai","est","et","etant","etc","etre","eu","eue","eues","euh","eurent","eus","eusse","eussent","eusses","eussiez","eussions","eut","eux","eux-mêmes","exactement","excepté","extenso","exterieur","eûmes","eût","eûtes","f","fais","faisaient","faisant","fait","faites","façon","feront","fi","flac","floc","fois","font","force","furent","fus","fusse","fussent","fusses","fussiez","fussions","fut","fûmes","fût","fûtes","g","gens","h","ha","haut","hein","hem","hep","hi","ho","holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","i","ici","il","ils","importe","j","je","jusqu","jusque","juste","k","l","la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels","leur","leurs","longtemps","lors","lorsque","lui","lui-meme","lui-même","là","lès","m","ma","maint","maintenant","mais","malgre","malgré","maximale","me","meme","memes","merci","mes","mien","mienne","miennes","miens","mille","mince","mine","minimale","moi","moi-meme","moi-même","moindres","moins","mon","mot","moyennant","multiple","multiples","même","mêmes","n","na","naturel","naturelle","naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième","ni","nombreuses","nombreux","nommés","non","nos","notamment","notre","nous","nous-mêmes","nouveau","nouveaux","nul","néanmoins","nôtre","nôtres","o","oh","ohé","ollé","olé","on","ont","onze","onzième","ore","ou","ouf","ouias","oust","ouste","outre","ouvert","ouverte","ouverts","o|","où","p","paf","pan","par","parce","parfois","parle","parlent","parler","parmi","parole","parseme","partant","particulier","particulière","particulièrement","pas","passé","pendant","pense","permet","personne","personnes","peu","peut","peuvent","peux","pff","pfft","pfut","pif","pire","pièce","plein","plouf","plupart","plus","plusieurs","plutôt","possessif","possessifs","possible","possibles","pouah","pour","pourquoi","pourrais","pourrait","pouvait","prealable","precisement","premier","première","premièrement","pres","probable","probante","procedant","proche","près","psitt","pu","puis","puisque","pur","pure","q","qu","quand","quant","quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt","quatrième","quatrièmement","que","quel","quelconque","quelle","quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze","quoi","quoique","r","rare","rarement","rares","relative","relativement","remarquable","rend","rendre","restant","reste","restent","restrictif","retour","revoici","revoilà","rien","s","sa","sacrebleu","sait","sans","sapristi","sauf","se","sein","seize","selon","semblable","semblaient","semble","semblent","sent","sept","septième","sera","serai","seraient","serais","serait","seras","serez","seriez","serions","serons","seront","ses","seul","seule","seulement","si","sien","sienne","siennes","siens","sinon","six","sixième","soi","soi-même","soient","sois","soit","soixante","sommes","son","sont","sous","souvent","soyez","soyons","specifique","specifiques","speculatif","stop","strictement","subtiles","suffisant","suffisante","suffit","suis","suit","suivant","suivante","suivantes","suivants","suivre","sujet","superpose","sur","surtout","t","ta","tac","tandis","tant","tardive","te","tel","telle","tellement","telles","tels","tenant","tend","tenir","tente","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute","toutefois","toutes","treize","trente","tres","trois","troisième","troisièmement","trop","très","tsoin","tsouin","tu","té","u","un","une","unes","uniformement","unique","uniques","uns","v","va","vais","valeur","vas","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan","voici","voie","voient","voilà","voire","vont","vos","votre","vous","vous-mêmes","vu","vé","vôtre","vôtres","w","x","y","z","zut","à","â","ça","ès","étaient","étais","était","étant","état","étiez","étions","été","étée","étées","étés","êtes","être","ô"}

def normalize_text(text):
    """Normalise le texte en enlevant les accents, en convertissant en minuscule, et en excluant les stop words."""
    words = re.findall(r'\w+', unidecode(text.lower()))
    # Simplification pour mettre au singulier, ajustez selon vos besoins
    words = [word[:-1] if word.endswith('s') else word for word in words]
    return [word for word in words if word not in stop_words]

def load_visited_urls():
    visited_urls = set()
    try:
        with open('webpages.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                url = row[0]  # Assuming the URL is the first column
                visited_urls.add(url)
    except FileNotFoundError:
        print("No existing 'webpages.csv' file found. Starting fresh.")
    return visited_urls

visited_urls = load_visited_urls()


def crawler():
    while True:
        url = urls_to_crawl.get()
        if url in visited_urls:
            urls_to_crawl.task_done()
            continue
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            words = normalize_text(text)
            word_counts = Counter(words)
            total_words = sum(word_counts.values())
            title = soup.find('title').text if soup.find('title') else ""
            description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else ""
            content_to_add.put((url, title, description))
            keywords_data = {word: count / total_words for word, count in word_counts.items()}
            keywords_to_add.put((url, keywords_data))
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            for link in links:
                absolute_link = urljoin(url, link)
                links_to_add.put(absolute_link)
        except requests.RequestException as e:
            print(f"Error fetching page: {url}, due to {e}")
        finally:
            urls_to_crawl.task_done()


def add_to_csv():
    with open('webpages.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        while True:
            url, title, description = content_to_add.get()
            print(f" Adding to CSV: {url} \n")
            writer.writerow([url, title, description])
            file.flush()
            content_to_add.task_done()

def update_keywords_csv():
    """Mise à jour du fichier keywords.csv avec les nouveaux mots-clés."""
    while True:
        url, keywords_data = keywords_to_add.get()
        print(f"Updating keywords for: {url} - {len(keywords_data)} keywords updated. \n")
        updated_keywords = {}
        try:
            with open('keywords.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    keyword = row["mot-clé"]
                    data = json.loads(row["données"])
                    updated_keywords[keyword] = data

            for word, frequency in keywords_data.items():
                if word in updated_keywords:
                    if url not in updated_keywords[word]:
                        updated_keywords[word][url] = frequency
                    else:
                        updated_keywords[word][url] = max(frequency, updated_keywords[word][url])
                else:
                    updated_keywords[word] = {url: frequency}

            with open('keywords.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["mot-clé", "données"])
                writer.writeheader()
                for keyword, data in updated_keywords.items():
                    writer.writerow({"mot-clé": keyword, "données": json.dumps(data)})
        except FileNotFoundError:
            with open('keywords.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["mot-clé", "données"])
                writer.writeheader()
                for word, frequency in keywords_data.items():
                    writer.writerow({"mot-clé": word, "données": json.dumps({url: frequency})})
        finally:
            keywords_to_add.task_done()

def manage_urls():
    visited_urls = set()
    while True:
        url = links_to_add.get()
        if url not in visited_urls:
            visited_urls.add(url)
            urls_to_crawl.put(url)
        links_to_add.task_done()

# Initialisation des threads
crawler_thread = threading.Thread(target=crawler)
csv_thread = threading.Thread(target=add_to_csv)
keywords_csv_thread = threading.Thread(target=update_keywords_csv)
urls_manager_thread = threading.Thread(target=manage_urls)

# Démarrage des threads
crawler_thread.start()
csv_thread.start()
keywords_csv_thread.start()
urls_manager_thread.start()

# URL de départ
urls_to_crawl.put("https://ijeni.tn/")
