from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'

db = SQLAlchemy(app)

# ================= MODELS =================

class Song(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    artist = db.Column(
        db.String(200),
        nullable=False
    )

    album = db.Column(
        db.String(200),
        nullable=False
    )

    duration = db.Column(
        db.String(50),
        nullable=False
    )

    def __repr__(self):
        return self.title

# ================= ROUTES =================

@app.route('/')
def home():

    songs = Song.query.all()

    return render_template(
        'songs.html',
        songs=songs
    )

@app.route('/add-song', methods=['GET', 'POST'])
def add_song():

    if request.method == 'POST':

        title = request.form['title']
        artist = request.form['artist']
        album = request.form['album']
        duration = request.form['duration']

        song = Song(
            title=title,
            artist=artist,
            album=album,
            duration=duration
        )

        db.session.add(song)
        db.session.commit()

        return redirect('/')

    return render_template('add_song.html')

@app.route('/delete-song/<int:id>')
def delete_song(id):

    song = Song.query.get_or_404(id)

    db.session.delete(song)
    db.session.commit()

    return redirect('/')

@app.route('/update-song/<int:id>', methods=['GET', 'POST'])
def update_song(id):

    song = Song.query.get_or_404(id)

    if request.method == 'POST':

        song.title = request.form['title']
        song.artist = request.form['artist']
        song.album = request.form['album']
        song.duration = request.form['duration']

        db.session.commit()

        return redirect('/')

    return render_template(
        'update_song.html',
        song=song
    )

# ================= MAIN =================

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
