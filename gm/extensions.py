# flask and other extensions instantiated here.

from flask import Flask
import logging
from pymongo import MongoClient

# -------------------- logger stuff ------------------------------


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


# create the main app for flask
app = Flask(__name__)


# -------------------- database stuff ------------------------------

mongo = MongoClient('mongodb://localhost:27017/cpf');
db = mongo.get_default_database();





