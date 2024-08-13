import pickle as pkl
from pymongo import MongoClient
import streamlit as st
from pymongo.server_api import ServerApi
import json
# Replace with your MongoDB connection string

import requests

# def get_external_ip():
#     response = requests.get("https://api64.ipify.org?format=json")
#     if response.status_code == 200:
#         data = response.json()
#         return data.get("ip")
#     else:
#         return "Unknown"
#
# external_ip = get_external_ip()
# st.write("External IP:", external_ip)
@st.cache_resource
def init_connection():
    connection_string = "mongodb+srv://"+st.secrets.username+":"+st.secrets.password+"@cluster0.aikbkzz.mongodb.net/?retryWrites=true&w=majority&appName=Streamlit"
    return MongoClient(connection_string,server_api=ServerApi('1'))
client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_movies_data():
    db = client["MovieRS"]
    collection = db["pklsmov"]
    items = collection.find()
    items = list(items)  # make hashable for st.cache_data
    return items
def get_similarity_data(ind):
    db = client["MovieRS"]
    collection = db["pklsim"]
    items = collection.find_one({"sno":ind})
    #items = list(items)  # make hashable for st.cache_data
    return items
import pandas as pd
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = [record['sno'] for record in movies if record['title'] == movie]
    sim=get_similarity_data(index[0])
    sim.pop("sno")
    sim.pop("_id")
    sim=[sim[str(i)] for i in range(4805)]
    distances = sorted(list(enumerate(sim)), key=lambda item: item[1], reverse=True)
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        k=[ko for ko in movies if ko['sno'] == i[0]]
        k=k[0]
        movie_id = k['id']
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(k['title'])

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = get_movies_data()


movie_list =  [record['title'] for record in movies]
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    options=movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5,gap='small',vertical_alignment='bottom')
    with col1:
        #st.text(recommended_movie_names[0])
        st.markdown(f"""
        <div style="width: 100%; white-space: pre-wrap;">{recommended_movie_names[0]}</div>
        """, unsafe_allow_html=True)
        st.image(recommended_movie_posters[0])
    with col2:
        #st.text(recommended_movie_names[1])
        st.markdown(f"""
        <div style="width: 100%; white-space: pre-wrap;">{recommended_movie_names[1]}</div>
        """, unsafe_allow_html=True)
        st.image(recommended_movie_posters[1])

    with col3:
        #st.text(recommended_movie_names[2])
        st.markdown(f"""
        <div style="width: 100%; white-space: pre-wrap;">{recommended_movie_names[2]}</div>
        """, unsafe_allow_html=True)
        st.image(recommended_movie_posters[2])
    with col4:
        st.markdown(f"""
        <div style="width: 100%; white-space: pre-wrap;">{recommended_movie_names[3]}</div>
        """, unsafe_allow_html=True)
        st.image(recommended_movie_posters[3])
    with col5:
        st.markdown(f"""
        <div style="width: 100%; white-space: pre-wrap;">{recommended_movie_names[4]}</div>
        """, unsafe_allow_html=True)
        st.image(recommended_movie_posters[4])