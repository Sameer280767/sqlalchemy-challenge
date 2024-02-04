# First we import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


# Lets set up the Databse/ reflect it into a new model and save references to 2 tables
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
Station = Base.classes.station
Measurement = Base.classes.measurement

# Lets set up Flask
app = Flask(__name__)

# Lets define the route which lists all available routes
@app.route("/")
def welcome():
    """All avaialble api routes are listed"""
    return(
        f"All API routes listed below<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Lets define a route for getting precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # We now create a link from Python to DB
    session = Session(engine)
    # From the last date in the DB go back a year. Store this date in a variable
    date_ly = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # With this link we will query all dates and preipitation data and store it in a dictionary and close the session
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=date_ly).all()
    session.close()
    # Lets convert the results into a dictionary so we can display json output
    prcp_data_all = {date: prcp for date, prcp in results}
    return jsonify(prcp_data_all)

# Lets define a route to get station lists
@app.route("/api/v1.0/stations")
def stations():
    # We now create a link from Python to DB
    session = Session(engine)
    # Lets create a query which gives us the list of all stations and close the session
    all_stations = session.query(Station.station).all()
    session.close()
    # Lets convert this to a normal list
    station_ID_list = list(np.ravel(all_stations))
    # Data is now ready to be returned as json list
    return jsonify(station_ID_list=station_ID_list)

# Lets define a route to define temperature observations
@app.route("/api/v1.0/tobs")
def tobs():
     # We now create a link from Python to DB
    session = Session(engine)
    # From the last date in the DB go back a year. Store this date in a variable
    date_ly = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # A query for most active station is now written and all temperatures for that station are stored
    # Most active station id is secured from Part 1 of the project, which is USC00519281
    #Session is then closed
    station_temp = session.query(Measurement.tobs,Measurement.date).filter(Measurement.date >= date_ly).filter(Measurement.station=="USC00519281").all()
    session.close()
    # Lets convert the results into a dictionary so we can display json output
    temp_data = {date: tobs for date, tobs in station_temp}
    return jsonify(temp_data)

# 2 routes are now defined, which allows the user to enter a start and end date to analyse temperatures
# The analysis required is min/max/avg temperatures for the 2 routes
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
# First query gets us the data with no end date provided
# Second query gets us data for start and end date
def query_data(start=None, end=None):
        if not end:
             session = Session(engine)
             first_query_results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
             session.close()
             list_result_first = list(np.ravel(first_query_results))
             return jsonify(list_result_first)
        session = Session(engine)
        second_query_results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
        session.close()
        list_result_second = list(np.ravel(second_query_results))
        return jsonify(list_result_second)

if __name__ == '__main__':
    app.run(debug=True)






    




        





