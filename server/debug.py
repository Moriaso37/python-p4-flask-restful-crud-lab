#!/usr/bin/env python3

from app import app
from models import db, Plant

if __name__ == '__main__':
    # Push the app context so we can access db and models easily
    with app.app_context():
        import ipdb; ipdb.set_trace()
