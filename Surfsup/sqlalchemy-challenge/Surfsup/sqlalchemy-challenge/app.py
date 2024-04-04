from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Create Flask app instance
app = Flask(__name__)

# Create engine and reflect database tables
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Reference the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link to the database
session = Session(engine)

# Define routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of precipitation data for the last 12 months."""
    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(func.max(Measurement.date)).scalar()
    last_date = datetime.strptime(last_date, '%Y-%m-%d')
    one_year_ago = last_date - timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)



if __name__ == '__main__':
    app.run(debug=True)