import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=a5f40438209e351d7475e552b85358e7&language=en-US".format(
        movie_id)
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_moviename = st.selectbox(
    'Select a movie to get recommendations',
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_moviename)

    # Display all the posters in a single line with their names above
    cols = st.columns(5)  # Create 5 columns for 5 recommendations
    for i in range(len(recommended_movie_names)):
        with cols[i]:
            st.text(recommended_movie_names[i])  # Display the name above
            st.image(recommended_movie_posters[i])  # Display the poster below the name
