#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from models import db, Venue, Artist, Shows
from datetime import datetime
import sys
from sqlalchemy import join

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

#  connecting to a local postgresql database-Check config.py for more info



from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # Real venues data.  num_shows is aggregated based on number of upcoming shows per venue.
  details = []
  current_time = datetime.now()
  initial = 0 # Setting number_of_upcoming_shows = 0

  Venue_Information = db.session.query(Venue.city, Venue.state).distinct()
  for place in Venue_Information:
    city = place.city
    state = place.state
    data = [] # This is the venue data
    filter = Venue.query.filter_by(city=city,state=state).all()

    for venue in filter:
      id = venue.id
      name = venue.name
      initial = len(Shows.query.filter_by(venue_id=id).filter(Shows.start_time>current_time).all())
      data.append({
        'id':id,
        'name':name,
        'number_of_upcoming_shows':initial
      })
    
    details.append({
      'city':city,
      'state':state,
      'venues':data
    })

  return render_template('pages/venues.html', areas=details)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # Implement search on artists with partial string search. It is case-insensitive.
  search_term = request.form.get('search_term', '')
  query = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
  
  response = {
    "count": len(query),
    "data": query
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
    venue = Venue.query.get_or_404(venue_id)
    previous_shows = []
    past_shows = []
    upcoming_shows = []
    upcoming_shows = []

    for previous in past_shows:
        previous_shows.append({
            "artist_id": Artist.query.get_or_404(previous.artist_id).id,
            "artist_name": Artist.query.get_or_404(previous.artist_id).name,
            "artist_image_link": Artist.query.get_or_404(
               past_shows.artist_id).image_link,
            "start_time": str(past_shows.start_time)
        })
    for show in venue.shows:
        if show.start_time < datetime.now():
            past_shows.append(show)
            
        else:
            upcoming_shows.append(show)

    for upcoming_show in upcoming_shows:
        upcoming_shows.append({
            "artist_id": Artist.query.get_or_404(upcoming_show.artist_id).id,
            "artist_name": Artist.query.get_or_404(
                upcoming_show.artist_id).name,
            "artist_image_link": Artist.query.get_or_404(
                upcoming_show.artist_id).image_link,
            "start_time": str(upcoming_show.start_time)
        })

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent":venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": previous_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # Here we are modifing data to be the data object returned from db insertion

  form = VenueForm()
  if form.validate_on_submit():  
    try:  

      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      address = request.form['address']
      phone = request.form['phone']
      genres = request.form.getlist('genres')
      facebook_link = request.form['facebook_link']
      image_link = request.form['image_link']
      website = request.form['website_link']
      seeking_description= request.form['seeking_description']
      
      
      if 'seeking_talent' not in request.form:
            seeking_talent = False
      else:
            seeking_talent = True

      Overall_Info = Venue(name=name, city=city, state=state, address=address, 
                          phone=phone, genres=genres, facebook_link=facebook_link,
                          image_link=image_link, website=website,
                          seeking_talent=seeking_talent, seeking_description=seeking_description)

      db.session.add(Overall_Info)
      db.session.commit()
    
    except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
    
    
    finally:
      db.session.close()

  
    # error = False
    # flash('Venue ' + request.form['name'] + ' was successfully listed!')

    flash('Venue ' + request.form['name'] + ' was successfully listed!')


   # error = True
   # flash('Venue ' + request.form['name'] + ' can not be listed!')
    for error in form.errors.items():
      flash('Venue ' + request.form['name'] + ' can not be listed!')

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')
  
#  Delete Venue
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/delete', methods=['DELETE'])

def delete_venue(venue_id):
  # Endpoint for taking a venue_id, and using SQLAlchemy ORM to delete a record. Handles cases where the session commit could fail.
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  if error:
    ('An error occurred. Venue ' + request.form['venue_id'] + ' could not be listed.')
  else:
    flash('No errors. Venue ' + request.form['venue_id'] + ' are listed.')

  return render_template('pages/home.html')
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # Real data returned from querying the database
  Information=[]
  artists = Artist.query.all()
  for artist in artists:
    Information.append({
      "id": artist.id,
      "name": artist.name
    })
  

  return render_template('pages/artists.html', artists=Information)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # Implementing  search on artists with partial string search. It is case-insensitive.
  search_term=request.form.get('search_term', '')
  query= Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  Information= []
  
  response = {
        'count':len(query),
        'data':Information
      }

  for artist in query:
      Information.append({
          'id': artist.id,
          'name': artist.name,
          'num_upcoming_shows': len(Shows.query.filter_by(artist_id=artist.id).filter(Shows.start_time>datetime.now()).all())
      })
      


  return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # Shows the artist page with the given artist_id
  upcoming_shows = db.session.query(Shows).join(Venue).filter(Shows.artist_id==artist_id).filter(Shows.start_time>datetime.now()).all()
  previous_shows = db.session.query(Shows).join(Venue).filter(Shows.artist_id==artist_id).filter(Shows.start_time>datetime.now()).all()

  Artists = Artist.query.get(artist_id)

  Information = {
    "id": Artists.id,
    "name": Artists.name,
    "genres": Artists.genres,
    "city": Artists.city,
    "state":Artists.state,
    "phone":Artists.phone,
    "website": Artists.website,
    "facebook_link": Artists.facebook_link,
    "seeking_venue": Artists.seeking_venue,
    "seeking_description": Artists.seeking_description,
    "image_link": Artists.image_link,
    "past_shows": previous_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(previous_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  for show in previous_shows:
    previous_shows.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue_name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
    })

  for show in upcoming_shows:
    upcoming_shows.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue_name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
    })

  return render_template('pages/show_artist.html', artist=Information)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # populate form with fields from artist with ID <artist_id>
    try:

        update = Artist.query.get_or_404(artist_id)

        form = ArtistForm(obj=update)
        return render_template('forms/edit_artist.html', form=form,artist=update)
    except:
        flash(f"Artist ({update.id}) failed to fetch")

    return render_template('forms/edit_artist.html', form=form, artist=update)
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # Taking values from the form submitted, and update existing
  
    error = False
    artist = Artist.query.get(artist_id)
    requestform = ArtistForm(request.form)

    try:
        artist.name = requestform.name.data
        artist.city = requestform.city.data
        artist.state = requestform.state.data
        artist.phone = requestform.phone.data
        artist.genres = requestform.genres.data
        artist.facebook_link = requestform.facebook_link.data
        artist.image_link = requestform.image_link.data
        artist.website_link = requestform.website_link.data
        artist.seeking_venues = requestform.seeking_venue.data
        artist.seeking_description = requestform.seeking_description.data

        db.session.commit()
        flash(f"Artist {artist.name} was successfully edited!")
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
        flash(f"Could not edit {artist.name} :(")
    finally:
        db.session.close()

    if not error:
        return redirect(url_for('show_artist', artist_id=artist_id))
    else:
        abort(500)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  # Populating form with values from venue with ID <venue_id>
  
  venue = Venue.query.filter_by(id=venue_id).first()
  form = VenueForm(obj=venue)
  if venue:
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.address.data = venue.address
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link

    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  #  taking  values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    error = False
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(request.form)

    print(request.values)
    try:
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.genres = form.genres.data
        venue.facebook_link = form.facebook_link.data
        venue.image_link = form.image_link.data
        venue.website_link = form.website_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data

        db.session.commit()
        flash(f"Successfully edited {venue.name}!")
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
        flash(f"Something went wrong editing {venue.name}")
    finally:
        db.session.close()

    if not error:
        return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # The following function when called upon submitting the new artist listing form modifies data to be the data object returned from db insertion.
  form = ArtistForm(request.form)
  try:
    artist = Artist(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      seeking_venue=form.seeking_venue.data,
      seeking_description=form.seeking_description.data,
      genres=form.genres.data
    )
    db.session.add(artist)
    db.session.commit()
    #On succesive db insert, show message that artist was succesfully listed
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    #In case of failure, show message that an error occured
    flash('An error occurred. Artist '+ request.form['name'] + ' could not be listed')
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows

    all_shows = Shows.query.all()
    data = []

    for show in all_shows:
        data.append({
            "venue_id": Venue.query.get_or_404(show.venue_id).id,
            "venue_name": Venue.query.get_or_404(show.venue_id).name,
            "artist_id": Artist.query.get_or_404(show.artist_id).id,
            "artist_name": Artist.query.get_or_404(show.artist_id).name,
            "artist_image_link": Artist.query.get_or_404(
                show.artist_id).image_link,
            "start_time": str(show.start_time)
        })

    return render_template('pages/shows.html', shows=data)

#  Create Shows
#  ----------------------------------------------------------------

@app.route('/shows/create')
def create_shows():
  # renders form.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # Inserting form data as a new.


  error = False
  try:
      venue_id = request.form['venue_id']
      artist_id = request.form['artist_id']
      start_time = request.form['start_time']
      show_item = Shows(venue_id=venue_id, 
                        artist_id=artist_id, 
                        start_time=start_time)
      db.session.add(show_item)
      db.session.commit()  
  except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
  finally:
      db.session.close()
  if error:
    flash('Oops, an error occurred in Show! ' + 'The Venue (id: ' + venue_id + ') and the Artist (id:' + artist_id +') could not be listed.' )
  else:
    flash('Show was successfully listed!')
  return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

@app.route('/shows/<int:show_id>/edit', methods=['GET'])
def edit_show(show_id):
  show = Shows.query.filter_by(id=show_id).first()
  form = ShowForm(obj=show)

  return render_template('forms/edit_show.html', form=form, show=show)

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''