import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


# Order API (POST)
@app.route('/order', methods=['POST'])
def order():
    # 클라이언트에서 받은 데이터를 받기
    name_receive = request.form['name_give']
    amount_receive = request.form['amount_give']
    address_receive = request.form['address_give']
    contact_receive = request.form['contact_give']

    # 받은 데이터를 DB 에 저장
    db.orders.insert_one(
        {'Name': name_receive, 'Amount': amount_receive, 'Address': address_receive, 'Contact': contact_receive})

    return jsonify({'result': 'success'})


@app.route('/order', methods=['GET'])
def orderList():
    # DB 에서 데이터 불러오기
    result = list(db.orders.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'orders': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
