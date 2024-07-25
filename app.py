from flask import Flask, render_template, request, redirect, url_for
import requests
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
db = SQLAlchemy(app)

# Open the JSON file with api key
with open('api_key.json', 'r') as file:
    api_key = json.load(file)

API_KEY = api_key["api_key"]  # Replace with your ExchangeRate-API key

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    response = requests.get(f'http://www.omdbapi.com/?s={query}&apikey={API_KEY}')
    data = response.json()
    movies = data.get('Search', [])
    return render_template('index.html', movies=movies)

@app.route('/movie/<id>')
def movie_detail(id):
    response = requests.get(f'http://www.omdbapi.com/?i={id}&apikey={API_KEY}')
    movie = response.json()
    return render_template('movie_detail.html', movie=movie)

@app.route('/rate', methods=['POST'])
def rate_movie():
    movie_id = request.form.get('movie_id')
    rating = request.form.get('rating')
    new_rating = Rating(movie_id=movie_id, rating=int(rating))
    db.session.add(new_rating)
    db.session.commit()
    return redirect(url_for('movie_detail', id=movie_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
