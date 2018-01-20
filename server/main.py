import logging
from flask import Flask, send_from_directory, redirect
from backend.extensions import mongo, app

app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG='debug',
    STEAM_API_KEY="5A077504BD2C3BC32039D1CCF3DE1B75"
))

# -------------------- add blueprints ------------------------------
from backend.blueprint.blueprints import all_blueprints

## all the urls with the prefix /rev will be handles by the recommend blueprint
for blueprint in all_blueprints:
    app.register_blueprint(blueprint)

# -------------------- add blueprints  ------------------------------


# this is the main route
@app.route('/')
def mainPage():
  return redirect('/static/index.html');


## makes it so that when you run this script it starts flask, but it is recommmened to start
## the server using the flask cli
if __name__ == "__main__":
    print("starting the server app.run()");
    app.debug = True;
    app.run(port=4000)


