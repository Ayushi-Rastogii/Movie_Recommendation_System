import configparser
import toml
from flask import Flask, render_template, jsonify,request
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from flask_cors import CORS
import requests
#from dotenv import load_dotenv
import os

# Load the .env file

app = Flask(__name__)
CORS(app)
# secrets = toml.load('secrets.toml')
#load_dotenv()
config = configparser.ConfigParser()
app.config['DEBUG'] = True
app.config['USERNAME'] = os.getenv('username')
app.config['PASSWORD'] = os.getenv('password')
app.config['MONGO_URI'] = "mongodb+srv://"+app.config['USERNAME']+":"+app.config['PASSWORD']+"@cluster0.aikbkzz.mongodb.net/MovieRS?retryWrites=true&w=majority&appName=Flask"
mongo = PyMongo(app)

# Use LocalProxy to read the global db instance with just `db`
client = LocalProxy(lambda: mongo.db)


@app.route('/')
def home():
    return render_template('index.html')

def get_similarity_data(ind):
    collection = client.pklsim
    items = collection.find_one({"sno":ind})
    return items
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def get_sno(movie):
    collection = client.pklsmov
    items = collection.find_one({"title":movie})
    return items["sno"]
def get_movie_det(sno):
    collection = client.pklsmov
    items = collection.find_one({"sno":sno})
    return items
def recommend(movie):
    index = get_sno(movie)
    sim=get_similarity_data(index)
    sim.pop("sno")
    sim.pop("_id")
    sim=[sim[str(i)] for i in range(4805)]
    distances = sorted(list(enumerate(sim)), key=lambda item: item[1], reverse=True)
    recom = []
    for i in distances[1:9]:
        # fetch the movie poster
        recom_di=dict()
        movie_rec= get_movie_det(i[0])
        recom_di['title']=movie_rec['title']
        recom_di['url']=fetch_poster(movie_rec['id'])
        recom.append(recom_di)
    return recom
def recommend2(movie):
    index = get_sno(movie)
    sim=get_similarity_data(index)
    sim.pop("sno")
    sim.pop("_id")
    sim=[sim[str(i)] for i in range(4805)]
    distances = sorted(list(enumerate(sim)), key=lambda item: item[1], reverse=True)
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id,movie_title = get_movie_det(i[0])
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movie_title)
    recommendation=dict()
    recommendation['movie_name']=recommended_movie_names
    recommendation['movie_poster']=recommended_movie_posters
    return recommendation
@app.route('/recommend', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        movie = data.get('movie')
        if not movie:
            return jsonify({"error": "No movie provided"}), 400

        recommendations = recommend(movie)
        return jsonify(recommendations)
    except Exception as e:
        # Log the error and return a 500 error with a message
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/api/data', methods=['GET'])
def get_movies_data():
    collection = client.pklsmov  # Access the collection
    items = collection.find()      # Find all documents
    items_list = list(items)       # Convert cursor to list
    # Optionally: Convert ObjectId to string if needed
    for item in items_list:
        item['_id'] = str(item['_id'])

    return jsonify(items_list)

if __name__ == "__main__":
    app.run(debug=True,port=8000)
