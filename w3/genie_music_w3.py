import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

songs = soup.select('.music-list-wrap > .list-wrap > tbody > .list')

song_rank = 0
for song in songs:
    song_name = song.select_one('td.info > a.title.ellipsis')
    song_singer = song.select_one('td.info > a.artist.ellipsis')
    if song_name is not None:
        song_rank += 1
        # print(song_rank, song_name.text, song_singer.text)

        doc = {
            'rank': song_rank,
            'title': song_name.text,
            'singer': song_singer.text
        }
        db.songs.insert_one(doc)

    else:
        print("Error")



