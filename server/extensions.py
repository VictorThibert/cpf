"""Flask and other extensions instantiated here.

To avoid circular imports with views and create_app(), extensions are instantiated here.
They will be initialized
(calling init_app()) in main.py.
"""

from flask import Flask

# -------------------- logger stuff ------------------------------
import logging

# set all the custom logging information needed
logging.basicConfig(filename='main.log',level=logging.DEBUG)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
# -------------------- logger stuff ------------------------------


## create the main app for flask
app = Flask(__name__)


# -------------------- database stuff ------------------------------
# from model.player import Player
# from model.game import Game
## initialize the mongodb driver

from pymongo import MongoClient

mongo = MongoClient('mongodb://localhost:27017/recSystemGames');
db = mongo.get_default_database();
# ## not going to use pymongo anymore,
# mongo = PyMongo()
# app.config['MONGO_HOST'] = 'localhost'
# app.config['MONGO_PORT'] = 27017
# app.config['MONGO_DBNAME'] = 'games'
# mongo.init_app(app, config_prefix='MONGO')

# with app.get_context():
# result = mongo.db.games.insert_one({"name":"temp", "stuff":"asdad"})

# connection = Connection(host="27017", port=27017)
# connection.register([Player, Game])


# -------------------- database stuff ------------------------------



