from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load data
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

def recommend(movie):
    movie = movie.lower()

    if movie not in movies['title'].str.lower().values:
        return []

    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    return [movies.iloc[i[0]].title for i in movie_list]

@app.route("/recommend", methods=["GET"])
def recommend_api():
    movie = request.args.get("movie")

    if not movie:
        return jsonify({"error": "movie parameter is required"}), 400

    recommendations = recommend(movie)

    if not recommendations:
        return jsonify({"error": "movie not found"}), 404

    return jsonify({
        "searched_movie": movie,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)
