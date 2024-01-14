from datetime import *
import json
import requests
from flask import Flask, render_template, url_for

app = Flask(__name__)
app.debug = True

@app.route('/Video/<video>')
def video_page(video):
    url = 'http://34.154.15.243/myflix/videos?filter={"video.uuid":"' + video + '"}'
    headers = {}
    payload = json.dumps({})
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message'])
    
    jResp = response.json()
    
    for index in jResp:
        for key in index:
            if key != "_id":
                for key2 in index[key]:
                    if key2 == "Name":
                        video = index[key][key2]
                    if key2 == "file":
                        videofile = index[key][key2]
                    if key2 == "pic":
                        pic = index[key][key2]
    
    return render_template('video.html', name=video, file=videofile, pic=pic)

@app.route('/NewVideo/<video>')
def new_video_page(video):
    return render_template('video.html', video=video)

@app.route('/')
def cat_page():
    url = "http://34.34.30.78/myflix/videos"
    headers = {}
    payload = json.dumps({})
    response = requests.get(url)

    if response.status_code != 200:
        return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message'])

    jResp = response.json()

    html = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <title>MyFlix - Your Videos</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #141414;
                color: #fff;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                margin: 0;
                padding: 0;
            }

            h2 {
                margin-top: 20px;
                font-size: 32px;
                color: #fff;
            }

            #video-list {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-around;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }

            .video-card {
                background-color: #000;
                box-shadow: 0 2px 15px rgba(0, 0, 0, 0.8);
                border-radius: 5px;
                overflow: hidden;
                margin: 20px;
                width: 300px;
            }

            .video-thumb {
                width: 100%;
                height: auto;
                border-radius: 5px 5px 0 0;
            }

            .video-details {
                padding: 15px;
            }

            h3 {
                font-size: 18px;
                color: #fff;
                margin-bottom: 10px;
            }

            a {
                text-decoration: none;
                color: #fff;
                display: inline-block;
                background-color: #e50914;
                color: #fff;
                padding: 10px 15px;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }

            a:hover {
                background-color: #fff;
                color: #e50914;
            }
        </style>
    </head>

    <body>
        <h2>Your Videos</h2>
        <div id="video-list">
    """

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
                FULL_PATH = 'http://34.154.127.150/mp4/' + uuid
                html += f"""
                    <div class="video-card">
                        <img class="video-thumb" src="http://34.91.193.43/pics/{thumb}" alt="{name}">
                        <div class="video-details">
                            <h3>{name}</h3>
                            <a href="{url_for('new_video_page', video=uuid)}">Watch Now</a>
                        </div>
                    </div>
                """

    html += """
        </div>
    </body>

    </html>
    """

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
