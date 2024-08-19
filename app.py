from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests

app = Flask(__name__)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a5f40438209e351d7475e552b85358e7&language=en-US"
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

# Load the movie dictionary and similarity matrix
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_movie = None
    recommended_movie_names = []
    recommended_movie_posters = []
    
    if request.method == 'POST':
        selected_movie = request.form.get('movie_name')
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
    return render_template('index.html', movies=movies['title'].values, selected_movie=selected_movie or '', recommended_movie_names=recommended_movie_names, recommended_movie_posters=recommended_movie_posters, zip=zip)


if __name__ == '__main__':
    app.run(debug=True)
