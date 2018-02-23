import logging
from flask import Flask, send_from_directory, redirect
from restaurants import restaurant
from extensions import app
from flask_cors import CORS

CORS(app)
app.register_blueprint(restaurant)



# this is the main route
@app.route('/')
def mainPage():
  return "fallback :)"


## makes it so that when you run this script it starts flask, but it is recommmened to start
## the server using the flask cli
if __name__ == "__main__":
    print("starting the server app.run()");
    app.debug = True;
    app.run(port=4000, host='0.0.0.0')


