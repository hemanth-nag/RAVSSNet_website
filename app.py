from flask import Flask, render_template, Response, request
import sys
from moviepy.editor import *
from werkzeug.utils import secure_filename
app = Flask(__name__)
import os
import requests
api_url = 'http://72ab-34-133-180-183.ngrok.io/'
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/live_demo_1')
def live_demo_1():
    return render_template('page1.html') 

@app.route('/report')
def report():
    return render_template('page2.html')     

@app.route('/live_demo_2', methods=['POST', 'GET'])
def live_demo_2():
    global api_url
    api_url = request.form['name']
    return render_template('page3.html')   

@app.route('/result', methods=['POST', 'GET'])
def result():
    coordinates = request.form['name']
    data = {'coords':coordinates}
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'vid.mp4')) 
    files = {'file': open('static/uploads/vid.mp4','rb')}
    requests.post(api_url,files=files,data=data)
    r1 = requests.get(api_url+'get1')
    r2 = requests.get(api_url+'get2')
    with open('static/results/a1.wav', 'wb') as w:
        w.write(r1.content)
    with open('static/results/a2.wav', 'wb') as w:
        w.write(r2.content)
        
    clip1 = VideoFileClip("static/uploads/vid.mp4")
    clip2 = VideoFileClip("static/uploads/vid.mp4")
    a1 = AudioFileClip("static/results/a1.wav")
    a2 = AudioFileClip("static/results/a2.wav")
    v1 = clip1.set_audio(a1)
    v2 = clip2.set_audio(a2)
    v1.write_videofile("static/results/s1.mp4")
    v2.write_videofile("static/results/s2.mp4")
    
    return render_template('res.html')

@app.route('/home')
def home():
    return render_template('index.html')  
    
if __name__ == '__main__':
    app.run() 