import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route('/')
def welcome():
   return (
        f'Welcome to the Justice League API!<br/>'
        f'Available Routes:<br/>'       
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start_date<br/>'
        f'/api/v1.0/start_date&end_date<br/><br/>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-12-31').\
        filter(Measurement.date < '2018-01-01').\
        order_by(Measurement.date.asc()).all()
    precipitation = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["temp_obs"] = result[1]
        precipitation.append(row)
    return jsonify(precipitation)

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station, Station.name).\
        order_by(Station.name.asc()).all()
    station_info = []
    for result in results:
        row = {}
        row["station"] = result[0]
        row["name"] = result[1]
        station_info.append(row)
    return jsonify(station_info)

@app.route('/api/v1.0/tobs')
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-12-31').\
        filter(Measurement.date < '2018-01-01').\
        order_by(Measurement.date.asc()).all()
    temp_obs = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["temp_obs"] = result[1]
        temp_obs.append(row)
    return jsonify(temp_obs)


@app.route('/api/v1.0/<start>')
def start(start_date):
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= '2017-01-12').all()
    temp_summary = []
    for result in results:
        row = {}
        row["minimum_temp"] = result[0]
        row["maximum_temp"] = result[1]
        row["average_temp"] = float(result[2])
        temp_summary.append(row)
    return jsonify(temp_summary)

@app.route('/api/v1.0/<start>/<end>')
def start_and_end(start_date,end_date):
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date > start_date).\
        filter(Measurement.date < end_date).\
        order_by(Measurement.date.asc()).all()
    
    temp_summary = []
    for result in results:
        row = {}
        row["minimum_temp"] = result[0]
        row["maximum_temp"] = result[1]
        row["average_temp"] = float(result[2])
        temp_summary.append(row)
    return jsonify(temp_summary)

if __name__ == '__main__':
    app.run()

