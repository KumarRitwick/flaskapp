from flask import Flask, render_template, redirect, url_for
import json
import requests

app = Flask(__name__)
app.debug = True

@app.route('/Video/<video>')
def video_page(video):
    url = 'http://34.154.15.243/myflix/videos?filter={"video.uuid":"' + video + '"}'
    headers = {}
    payload = json.dumps({})
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Unexpected response: {0}. Status: {1}. Message: {2}".format(
            response.reason, response.status, response.text
        )

    jResp = response.json()
    print("JSON Response for Video Page:", jResp)

    for index in jResp:
        for key, value in index.items():
            if key != "_id" and isinstance(value, dict) and "file" in value:
                video_name = value.get("Name")
                video_file = value.get("file")
                video_pic = value.get("pic")

    return render_template('video.html', name=video_name, file=video_file, pic=video_pic)

@app.route('/')
def cat_page():
    url = "http://35.204.223.27/myflix/videos"
    headers = {}
    payload = json.dumps({})

    response = requests.get(url)

    if response.status_code != 200:
        return "Unexpected response: {0}. Status: {1}. Message: {2}".format(
            response.reason, response.status, response.text
        )

    jResp = response.json()
    print("JSON Response for Main Page:", jResp)

    html = "<h2>Your Videos</h2>"

    if jResp:
        first_video_uuid = jResp[0].get("file")
        return redirect(url_for('video_page', video=first_video_uuid))

    for index in jResp:
        for key, value in index.items():
            if key != "_id" and isinstance(value, dict) and "file" in value:
                name = value.get("Name")
                thumb = value.get("thumb")
                uuid = value.get("file")

                html = html + '<h3>' + name + '</h3>'
                html = html + '<a href="' + url_for('video_page', video=uuid) + '">'
                html = html + '<img src="http://35.204.223.27/pics/' + thumb + '">'
                html = html + "</a>"

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
