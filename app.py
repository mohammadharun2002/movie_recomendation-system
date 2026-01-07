from flask import Flask, request, jsonify, render_template
import pickle
import requests

app = Flask(__name__)

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=05126ed19870d7d6c23f324e19017f52&language=en-US')
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend(movie):
    movie = movie.lower()

    if movie not in movies['title'].str.lower().values:
        return []

    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommendations = []
    for i in movie_list:
        movie_data = movies.iloc[i[0]]
        recommendations.append({
            'title': movie_data.title,
            'poster': fetch_poster(movie_data.id)
        })

    return recommendations

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["GET"])
def recommend_api():
    movie = request.args.get("movie")
    if not movie:
        return jsonify({"error": "movie parameter is required"}), 400

    recommendations = recommend(movie)
    if not recommendations:
        return jsonify({"error": "movie not found"}), 404

    return jsonify({"searched_movie": movie, "recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)
