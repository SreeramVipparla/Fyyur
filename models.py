
  
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


class Shows(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('venues.id', ondelete='CASCADE'), nullable=False)
    artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('artists.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<shows>" % self.id % self.venue_id % self.artist_id % self.start_time


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(1000))
    facebook_link = db.Column(db.String(500))
    genres = db.Column(JSON)
    website = db.Column(db.String(1000))
    seeking_talent = db.Column(db.Boolean, default=False, server_default="false", nullable=False)
    seeking_description = db.Column(db.String(1000))
    

    shows = relationship("Shows", backref=backref("Venue", lazy=True))

    def __repr__(self):
        return "<venues>" % self.name

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(JSON)
    image_link = db.Column(db.String(1000))
    facebook_link = db.Column(db.String(500))
    website = db.Column(db.String(1000))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(1000))

    shows = relationship("Shows", backref=backref("Artist", lazy=True))

    def __repr__(self):
        return "<artists>" % self.name

