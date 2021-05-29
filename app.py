import requests
import json
from bs4 import BeautifulSoup as bs
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "Author": "Akira Dev",
        "Github": "https://github.com/DavitID",
        "Instagram": "davit__id",
        "list-surah": "http://api-my.herokuapp.com/list",
        })

@app.route("/list")
def list():
    url = "https://litequran.net/"
    req = requests.get(url)
    soup = bs(req.text, "html.parser")
    ol = soup.find("ol", class_="list").find_all("li")
    kosong = []
    for hasil in ol:
        all = hasil.find("a").text
        kosong.append({
            "surah": all,
            })

    return jsonify(kosong)

@app.route("/api")
def api():
    nama = request.args.get("surah")
    if not nama:
        return jsonify({
            "msg": "error",
            "Help": "http://api-my.herokuapp.com/api?surah=(nama surah)",
            })

    user = {
            "user-agent": "Chrome",
            "Content-Type": "text/html",
            }
    ses = requests.session()
    req = ses.get("https://litequran.net/"+nama, headers=user)
    print(req.encoding)
    soup = bs(req.text, "html.parser")
    ol = soup.find("ol").findAll("li")
    surah = []
    nomor = 0
    for hasil in ol:
        nomor += 1
        print(hasil.findAll("span")[0].get_text())
        surah.append({
            "msg": "success",
            "arab": hasil.findAll("span")[0].get_text(),
            "latin": hasil.findAll("span")[1].get_text(),
            "arti": hasil.findAll("span")[2].get_text()
            })

    return jsonify(surah)

@app.errorhandler(AttributeError)
def attr(e):
    return jsonify({
        "msg": "Surah tidak ditemukan",
        "help": "Silakan lihat list kembali",
        })

@app.errorhandler(404)
def found(e):
    return jsonify({
        "msg": "Maaf hal yang anda cari tidak dapat ditemukan",
        "help": "Silakan kembali ke index/list",
        })

if __name__ == "__main__":
    app.run(debug=True)
