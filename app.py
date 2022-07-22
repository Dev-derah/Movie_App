from distutils.log import debug
from email.mime import base
from multiprocessing import connection
from operator import index
from flask import Flask,render_template,url_for
from flask import request as form_request
import json
import urllib.request as request
import ssl
import random

app = Flask(__name__)

# api details
api_key="4c4819ad3a46f0c079a2ea4d467b1cb6"
base_url ="https://api.themoviedb.org/3/"


endpoints ={
        "discover":"discover/movie/?api_key="+api_key+"&language=en-US",
        "trending":"trending/movie/day?api_key="+api_key+"&language=en-US",
        "tv":"tv/popular?api_key="+api_key+"&language=en-US",
}
    

ssl._create_default_https_context = ssl._create_unverified_context
    # connections
conn =request.urlopen(base_url+endpoints["discover"])
conn2 =request.urlopen(base_url+endpoints["trending"])
conn3 =request.urlopen(base_url+endpoints["tv"])
    # conn4 =request.urlopen(base_url+"search/multi?api_key=4c4819ad3a46f0c079a2ea4d467b1cb6&language=en-US&query=")

    #data
trending_data=json.loads(conn2.read())
tv_shows_data=json.loads(conn3.read())
json_data =json.loads(conn.read())

@app.route("/")
def discover_movies(methods=["POST","GET"]):

    # search_data=json.loads(conn4.read())
    return render_template("index.html", discover_data =json_data['results'][0:5],trending_data =trending_data['results'], tv_shows= tv_shows_data["results"])

@app.route('/result', methods=["POST","GET"])
def result():
    output=form_request.form.to_dict()
    query =output["search"]
    conn4 =request.urlopen(base_url+"search/multi?api_key="+api_key+"&language=en-US&query="+query)
    search_data=json.loads(conn4.read())
    return render_template('index.html',search_data=search_data['results'],discover_data =json_data['results'][0:5],trending_data =trending_data['results'], tv_shows= tv_shows_data["results"])

    

@app.route("/<type>/<id>")
def details(type,id):
    ssl._create_default_https_context = ssl._create_unverified_context
    conn =request.urlopen(base_url+"/"+type+"/"+id+"?api_key="+api_key+"&language=en-US")
    conn2 =request.urlopen(base_url+"/"+type+"/"+id+"/"+"similar"+"?api_key="+api_key+"&language=en-US")
    conn3 =request.urlopen(base_url+"/"+type+"/"+id+"/"+"reviews"+"?api_key="+api_key+"&language=en-US")

    json_data =json.loads(conn.read())
    similar_movies =json.loads(conn2.read())
    reviews =json.loads(conn3.read())

    
    return render_template("details.html",movie_info =json_data, similar_movies=similar_movies["results"][0:5],reviews=reviews["results"])

if __name__=='__main__':
    app.run(debug=True)
