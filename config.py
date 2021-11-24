import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:myPassword@localhost:5432/fyyur'


SQLALCHEMY_TRACK_MODIFICATIONS = False
# I have impemented the above due to the following error 
#/home/sreeram/Documents/workspace/FSND-master/projects/01_fyyur/starter_code/env/lib/python3.8/site-packages/flask_sqlalchemy/__init__.py:833: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future. \
# Set it to True or False to suppress this warning.