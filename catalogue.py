from datetime import *
import json
import requests
from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

BASE_VIDEO_URL = "http://34.154.15.243/mp4/"  # Update this with your actual base video URL

@app.route('/Video/<video>')
def video_page(video):
    url = 'http://34.154.15.243/myflix/videos?filter={"video.uuid":"' + video + '"}'
    headers = {}
    payload = json.dumps({})
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, response.text)
    
    jResp = response.json()
    
    for index in jResp:
        for key in index:
            if key != "_id":
                for key2 in index[key]:
                    if key2 == "Name":
                        video_name = index[key][key2]
                    if key2 == "file":
                        videofile = index[key][key2]
                    if key2 == "pic":
                        pic = index[key][key2]
    
    full_video_url = BASE_VIDEO_URL + videofile
    return render_template('video.html', name=video_name, file=full_video_url, pic=pic)

@app.route('/')
def cat_page():
    url = "http://35.204.223.27/myflix/videos"
    headers = {}
    payload = json.dumps({})

    response = requests.get(url)

    if response.status_code != 200:
        return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, response.text)

    jResp = response.json()
    html = "<h2>Your Videos</h2>"

    for index in jResp:
        for key in index:
            if key != "_id":
                for key2 in index[key]:
                    if key2 == "Name":
                        name = index[key][key2]
                    if key2 == "thumb":
                        thumb = index[key][key2]
                    if key2 == "file":
                        uuid = index[key][key2]

                html = html + '<h3>' + name + '</h3>'
                html = html + '<a href="/Video/' + uuid + '">'
                html = html + '<img src="http://35.204.223.27/pics/' + thumb + '">'
                html = html + "</a>"

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
