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
        "list-surah": "https://localhost:5000/list",
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
            "status": "Error",
            "Help": "https://localhost:5000/api?surah=al-fatihah",
            })

    ses = requests.session()
    req = ses.get("https://litequran.net/"+nama)
    print(req.encoding)
    soup = bs(req.text, "html.parser")
    ol = soup.find("ol").findAll("li")
    surah = []
    nomor = 0
    for hasil in ol:
        nomor += 1
        print(hasil.findAll("span")[0].get_text())
        surah.append({
            "arab": hasil.findAll("span")[0].get_text(),
            "latin": hasil.findAll("span")[1].get_text(),
            "arti": hasil.findAll("span")[2].get_text()
            })

    return jsonify(surah)
if __name__ == "__main__":
    app.run(debug=True)
