import requests
import datetime
from bs4 import BeautifulSoup

import json

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.linkcinema

## HTML을 주는 부분
@app.route('/')
def index():
   return render_template('index.html')


@app.route('/ticket')
def getTicket():
   return render_template('ticket.html')


@app.route('/movieList', methods=['POST'])
def post_now_showing():

   # movieGlu 의 GET filmsNowShowing 받기
   # datetime = datetime.datetime.now().isoformat()
   url = "https://api-gate2.movieglu.com/filmsNowShowing/?n=10"
   apikey = "1S4l9ifKks9mCX4AxGTVm9Q6SszGA9YU4Iiv3P9j"
   geolocation = "51.510408;-0.130105"
   authorization = "Basic U1RVRF8xMDQ6d2ZQVFludnVaUDF2"
   params = {"client" : "STUD_104",
             "x-api-key" : apikey,
             "Authorization" : authorization,
             "api-version" : "v200",
             "geolocation" : geolocation,
             "territory" : "US",
             "device-datetime" : "2020-01-08T08:30:17.360Z"}
   movieList = requests.get(url, headers= params).json()
   movies = movieList["films"]
   # print(movies)
   db.movies.remove({})

   for film in movies:
      movieTitle = film["film_name"]
      movieReleaseDate = film["release_dates"][0]["release_date"]
      movieAge = film["age_rating"][0]["rating"]
      movieImage = film["images"]["poster"]["1"]["medium"]["film_image"]
      movieDescription = film["synopsis_long"]

      movie = {'Title': movieTitle, 'Age Rating':movieAge, 'Release Date': movieReleaseDate, 'Poster': movieImage, 'Description': movieDescription}
      db.movies.insert_one(movie)


   return jsonify({'result': 'success'})



@app.route('/movieList', methods=['GET'])
def get_now_showing():
   all_movies = list(db.movies.find({}, {'_id': 0}))
   return jsonify({'result': 'success', 'info': all_movies})



if __name__ == '__main__':
   app.run('0.0.0.0',port=5002,debug=True)