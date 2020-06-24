import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SECRET KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A-VERY-LONG-SECRET-KEY'
