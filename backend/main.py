from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import requests
from bs4 import BeautifulSoup
import re
import json
import requests

app = Flask(__name__)

# Carregar os dados
ratings = pd.read_csv('./dataset/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
movies = pd.read_csv('./dataset/u.item', sep='|', encoding='latin-1', header=None, 
                     names=['movie_id', 'title', 'release_date', 'video_release_date', 'IMDb_URL'] + 
                     list(map(str, range(19))))

# Pré-processar os dados para filtragem colaborativa
user_item_matrix = ratings.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
user_similarity = cosine_similarity(user_item_matrix)

# Pré-processar os dados para filtragem baseada em conteúdo
movies['genres'] = movies.iloc[:, 5:].apply(lambda x: ' '.join(x.index[x == 1].tolist()), axis=1)
count_matrix = CountVectorizer().fit_transform(movies['genres'])
cosine_sim = cosine_similarity(count_matrix)

def remove_year(title):
    cleaned_title = re.sub(r'\s*\(\d{4}\)', '', title)
    return cleaned_title

def get_movie_image(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": "40a4bab7fcb59e0cf99bd396a74d57e3",
        "query": remove_year(movie_title)
    }
    print(movie_title)
    response = requests.get(search_url, params=params)
    data = response.json()
    print(data)
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    
    return None


def collaborative_filtering(user_id, n_recommendations=5):
    similar_users = user_similarity[user_id-1].argsort()[::-1][1:11]
    user_ratings = user_item_matrix.iloc[user_id-1]
    unwatched = user_ratings[user_ratings == 0].index
    
    recommendations = {}
    motives = {}
    
    for movie in unwatched:
        pred_rating = 0
        total_similarity = 0
        for similar_user in similar_users:
            if user_item_matrix.iloc[similar_user][movie] > 0:
                pred_rating += user_similarity[user_id-1][similar_user] * user_item_matrix.iloc[similar_user][movie]
                total_similarity += user_similarity[user_id-1][similar_user]
        if total_similarity > 0:
            recommendations[movie] = pred_rating / total_similarity
            similar_users_details = ", ".join([f"Usuário {sim_user+1} (similaridade: {user_similarity[user_id-1][sim_user]:.2f})" for sim_user in similar_users])
            motives[movie] = f"Baseado nas avaliações de usuários semelhantes: {similar_users_details}"
    
    sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
    
    result = []
    for movie_id, _ in sorted_recommendations[:n_recommendations]:
        title = movies[movies['movie_id'] == movie_id]['title'].values[0]
        image_url = get_movie_image(title)
        result.append({
            'movie_id': int(movie_id),
            'title': title,
            'image_url': image_url,
            'motives': motives[movie_id]
        })
    
    return result


def content_based_filtering(movie_id, n_recommendations=5):
    similar_movies = list(enumerate(cosine_sim[movie_id-1]))
    similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:n_recommendations+1]
    
    result = []
    motives = {}
    
    for movie in similar_movies:
        title = movies.iloc[movie[0]]['title']
        image_url = get_movie_image(title)
        result.append({
            'movie_id': int(movies.iloc[movie[0]]['movie_id']),
            'title': title,
            'image_url': image_url,
            'motives': f"Baseado em semelhança de gêneros com o filme '{movies.iloc[movie_id-1]['title']}'"
        })
    
    return result


@app.route('/collaborative', methods=['GET'])
def get_collaborative_recommendations():
    user_id = int(request.args.get('user_id', 1))
    n_recommendations = int(request.args.get('n', 5))
    recommendations = collaborative_filtering(user_id, n_recommendations)
    response = jsonify(recommendations)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/content-based', methods=['GET'])
def get_content_based_recommendations():
    movie_id = int(request.args.get('movie_id', 1))
    n_recommendations = int(request.args.get('n', 5))
    recommendations = content_based_filtering(movie_id, n_recommendations)
    response = jsonify(recommendations)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/', methods=['GET'])
def home():
    return """
    <h1>Sistema de Recomendação de Filmes</h1>
    <p>Use /collaborative?user_id=X&n=Y para recomendações colaborativas</p>
    <p>Use /content-based?movie_id=X&n=Y para recomendações baseadas em conteúdo</p>
    """

if __name__ == '__main__':
    app.run(debug=False)
