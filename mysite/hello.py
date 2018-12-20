from flask import Flask, render_template, request
import random
import requests
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('hello.html')

@app.route('/ping')
def ping():
    return render_template('ping.html')

@app.route('/pong')
def pong():
    ball = request.args['ball']
    result = '없었다'
    return render_template('pong.html', ball = ball, result = result)

@app.route('/lotto/<int:num>')
def lotto(num):
    url = f'https://dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={num}'
    response = requests.get(url)
    lotto = response.json()

    winner = []
    for i in range(1, 7):
        winner.append(lotto[f'drwtNo{i}'])

    bonus = lotto['bnusNo']
    return render_template('lotto.html', w=winner, b=bonus, n=num)