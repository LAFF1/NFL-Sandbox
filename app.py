import numpy as np
import sqlite3
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///players.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
player_stats = Base.classes.players

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
def get_db_connection():
    conn = sqlite3.connect('players.sqlite')
    conn.row_factory = sqlite3.Row
    return conn
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///players.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#################################################
# Flask Routes
#################################################

@app.route("/api")
def welcome():
    """List all available api routes."""
    return (
        f'<b>Available Routes:</b><br/>'
        f'# retrieves unique list of player names<br/>'
        f'@app.route("/players/names")<br/>'
        # f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/")
def template():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# retrieves unique list of stock ticker names
@app.route("/players/names")
def namesUnique():
    session = Session(engine)
    names = session.query(player_stats.Player).distinct(player_stats.Player).all()
    namesPrint = list(np.ravel(names))
    session.close()
    return jsonify(namesPrint)


if __name__ == '__main__':
    app.run(debug=True)
