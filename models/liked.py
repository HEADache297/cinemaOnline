from . import db

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, movie_id, name, author_id):
        self.movie_id = movie_id
        self.name = name
        self.author_id = author_id