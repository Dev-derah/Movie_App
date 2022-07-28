
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
        "tv":"tv/popular?api_key="+api_key,
        "action":"discover/movie?api_key="+api_key+"&with_genres=28",
        "comedy":"discover/movie?api_key="+api_key+"&with_genres=35",
        "crime":"discover/movie?api_key="+api_key+"&with_genres=80",
        "horror":"discover/movie?api_key="+api_key+"&with_genres=27",
        "mystery":"discover/movie?api_key="+api_key+"&with_genres=9648",
        "romance":"discover/movie?api_key="+api_key+"&with_genres=10749"
}
    

ssl._create_default_https_context = ssl._create_unverified_context
    # connections
conn =request.urlopen(base_url+endpoints["discover"])
conn2 =request.urlopen(base_url+endpoints["trending"])
conn3 =request.urlopen(base_url+endpoints["tv"])
conn4 =request.urlopen(base_url+endpoints["action"])
conn5 =request.urlopen(base_url+endpoints["comedy"])
conn6 =request.urlopen(base_url+endpoints["crime"])
conn7 =request.urlopen(base_url+endpoints["horror"])
conn8 =request.urlopen(base_url+endpoints["mystery"])
conn9 =request.urlopen(base_url+endpoints["romance"])


    #data
trending_data=json.loads(conn2.read())
tv_shows_data=json.loads(conn3.read())
json_data =json.loads(conn.read())
action_data =json.loads(conn4.read())
comedy_data = json.loads(conn5.read())
crime_data = json.loads(conn6.read())
horror_data = json.loads(conn7.read())
mystery_data = json.loads(conn8.read())
romance_data = json.loads(conn9.read())

@app.route("/")
def discover_movies(methods=["POST","GET"]):
    # search_data=json.loads(conn4.read())
    return render_template("index.html", discover_data =json_data['results'][0:5],trending_data =trending_data['results'], tv_shows= tv_shows_data["results"],action_data=action_data["results"],comedy_data=comedy_data["results"],crime_data=crime_data["results"],horror_data=horror_data["results"], mystery_data=mystery_data["results"],romance_data=romance_data["results"])

@app.route('/result', methods=["POST","GET"])
def result():
    output=form_request.form.to_dict()
    query =output["search"]
    conn4 =request.urlopen(base_url+"search/multi?api_key="+api_key+"&language=en-US&query="+query)
    search_data=json.loads(conn4.read())
    if len(search_data["results"])==0:
        return render_template('404.html',query=query)
    else:
            return render_template('search.html',search_data=search_data['results'],query=query)

    

@app.route("/<type>/<id>")
def details(type,id):
    ssl._create_default_https_context = ssl._create_unverified_context
    conn =request.urlopen(base_url+"/"+type+"/"+id+"?api_key="+api_key+"&language=en-US")
    conn2 =request.urlopen(base_url+"/"+type+"/"+id+"/"+"similar"+"?api_key="+api_key+"&language=en-US")
    conn3 =request.urlopen(base_url+"/"+type+"/"+id+"/"+"reviews"+"?api_key="+api_key+"&language=en-US")

    json_data =json.loads(conn.read())
    similar_movies =json.loads(conn2.read())
    reviews =json.loads(conn3.read())

    return render_template("details.html",movie_info =json_data, similar_movies=similar_movies["results"][0:6],reviews=reviews["results"])

if __name__=='__main__':
    app.run(debug=True)
