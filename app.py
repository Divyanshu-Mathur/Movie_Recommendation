import streamlit as st
import pickle
import pandas
import numpy
import requests
import os

api_key = st.secrets["general"]["API_KEY"]


with open('movies.pkl','rb') as file:
    movie_lst = pickle.load(file)

with open('similar.pkl','rb') as file:
    similar=pickle.load(file)

def recommend(movie):
    ind = movie_lst[movie_lst['title']==movie].index[0]
    dist = similar[ind]
    movie_l = sorted(list(enumerate(dist)),reverse=True,key=lambda x:x[1])[1:11]
    recomd=[]
    poster = []
    for i in movie_l:
        movie_id=i[0]
        recomd.append(movie_lst.iloc[i[0]].title)
        poster.append(find_img(movie_lst.iloc[i[0]].id))
    return(recomd,poster)

def find_img(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0429c425294fb3b573eaefd1c6d71d71&&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']
   
    


st.title('Movie Recommendation System')

entered_movie = st.selectbox(
    'Select any movie',
    movie_lst['title'].values
)

if st.button('Recommend'):
    title,poster = recommend(entered_movie)
    cols = st.columns(5) 

    for i, (title, poster) in enumerate(zip(title, poster)):
        with cols[i % 5]:  
            st.image(poster, caption=title, use_container_width=True)
    