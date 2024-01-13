from datetime import *
import json
import requests
from flask import Flask, request, render_template, url_for

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
    
    full_video_url = BASE_VIDEO_URL + videofile
    return render_template('video.html', name=video, file=full_video_url, pic=pic)

# ... (rest of your code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
