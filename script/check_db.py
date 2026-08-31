from test import app
from sql_lite import db, CachedMatch, NameLookup
from sqlalchemy import inspect

data = [
    {"id": 1, "name": "Infernus"},
    {"id": 2, "name": "Seven"},
    {"id": 3, "name": "Vindicta"},
    {"id": 4, "name": "Lady geist"},
    {"id": 5, "name": None },
    {"id": 6, "name": "Abrams"},
    {"id": 7, "name": "Wraith"},
    {"id": 8, "name": "McGinns"},
    {"id": 9, "name": None},
    {"id": 10, "name": "Paradox"},
    {"id": 11, "name": "Dynamo"},
    {"id": 12, "name": "Kelvin"},
    {"id": 13, "name": "Haze"},
    {"id": 14, "name": "Holiday"},
    {"id": 15, "name": "Bebop"},
    {"id": 16, "name": "Calico"},
    {"id": 17, "name": "Grey Talon"},
    {"id": 18, "name": "Mo & Krill"},
    {"id": 19, "name": "Shiv"},
    {"id": 20, "name": "Ivy"},
    {"id": 21, "name": "Kali"},
    {"id": 22, "name": None},
    {"id": 23, "name": None},
    {"id": 24, "name": None},
    {"id": 25, "name": "Warden"},
    {"id": 26, "name": None},
    {"id": 27, "name": "Yamato"},
    {"id": 28, "name": None},
    {"id": 29, "name": None},
    {"id": 30, "name": None},
    {"id": 31, "name": "Lash"},
    {"id": 32, "name": None},
    {"id": 33, "name": None},
    {"id": 34, "name": None},
    {"id": 35, "name": "Vicous"},
    {"id": 36, "name": None},
    {"id": 37, "name": None},
    {"id": 38, "name": "Gunslinger"},
    {"id": 39, "name": "The Boss"},
    {"id": 40, "name": None},
    {"id": 41, "name": None},
    {"id": 42, "name": None},
    {"id": 43, "name": None},
    {"id": 44, "name": None},
    {"id": 45, "name": None},
    {"id": 46, "name": None},
    {"id": 47, "name": "Tokamak"},
    {"id": 48, "name": "wrecker"},
    {"id": 49, "name": "Rutger"},
    {"id": 50, "name": "Pocket"},
    {"id": 51, "name": "Thumper"},
    {"id": 52, "name": "Mirage"},
    {"id": 53, "name": "Fathom"},
    {"id": 54, "name": "Cadence"},
    {"id": 55, "name": None},
    {"id": 56, "name": "Bomber"},
    {"id": 57, "name": "Shield Guy"},
    {"id": 58, "name": "Vyper"},
    {"id": 59, "name": "Vandal"},
    {"id": 60, "name": "Sinclair"},
    {"id": 61, "name": "Trapper"},
    {"id": 62, "name": "Raven"},
    {"id": 63, "name": "Mina"},
    {"id": 64, "name": "Drifter"},
    {"id": 65, "name": "Venator"},
    {"id": 66, "name": "Victor"},
    {"id": 67, "name": "Paige"},
    {"id": 68, "name": "Boho"},
    {"id": 69, "name": "The Doorman"},
    {"id": 70, "name": "Skyrunner"},
    {"id": 71, "name": "Swan"},
    {"id": 72, "name": "Billy"},
    {"id": 73, "name": None},
    {"id": 74, "name": None},
    {"id": 75, "name": "Fortuna"},
    {"id": 76, "name": "Graves"},
    {"id": 77, "name": None},
    {"id": 78, "name": None},
    {"id": 79, "name": "Rem"},
    {"id": 80, "name": "Silver"},
    {"id": 81, "name": "Celeste"},
    {"id": 82, "name": None},



]
# with app.app_context():
#     # insert a test row
    

#     for item in data:
#         entry = NameLookup(id=item["id"], name=item["name"])
#         db.session.merge(entry)
#     db.session.commit()
with app.app_context():

    all_entries = NameLookup.query.all()
    for e in all_entries:
        print(e.id, e.name)

from test import app, db

with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Number of tables:", len(tables))
    print("Table names:", tables)    
