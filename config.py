import os

DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string-zanyk'
