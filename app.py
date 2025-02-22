from flask import Flask, request, jsonify, render_template
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_tags', methods=['POST'])
def save_tags():
    file = request.files['file']
    title = request.form.get('title')
    artist = request.form.get('artist')
    album = request.form.get('album')
    genre = request.form.get('genre')
    date = request.form.get('date')

    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    audio = MP3(file_path, ID3=EasyID3)
    if title:
        audio['title'] = title
    if artist:
        audio['artist'] = artist
    if album:
        audio['album'] = album
    if genre:
        audio['genre'] = genre
    if date:
        audio['date'] = date

    audio.save()

    return jsonify({'message': 'Tags saved successfully!'})

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)


