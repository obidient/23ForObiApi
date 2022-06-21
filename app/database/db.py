from bigfastapi.db import database as bfa_db


def create_database():
    return bfa_db.create_database()

def get_db():
    return next(bfa_db.get_db())