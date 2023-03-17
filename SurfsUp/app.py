import datetime as dt
import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def index():
    return (
        f"Available Routes: <br/> <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start_end <br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    last_12_months = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()
    session.close()
    
    all_prcp = []
    for date, prcp in last_12_months:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations_list = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    all_stations = []
    for id, station, name, latitude, longitude, elevation in stations_list:
        stations_dict = {}
        stations_dict["id"] = id
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations_dict["latitude"] = latitude
        stations_dict["longitude"] = longitude
        stations_dict["elevation"] = elevation
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_12_temperature = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').filter(Measurement.station == 'USC00519281').order_by(Measurement.date).all()
    session.close()

    all_tobs = []
    for date, tobs in last_12_temperature:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def startdate(start):
    session = Session(engine)
    temps_from_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > start).all()
    session.close()

    all_starts = list(np.ravel(temps_from_start))

    return jsonify(all_starts)

@app.route("/api/v1.0/<start_end>")
def startandenddate(start_end):
    x = start_end.split("_")
    start = x[0]
    end = x[1]

    session = Session(engine)
    temps_from_start_and_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).all()
    session.close()

    all_starts_ends = list(np.ravel(temps_from_start_and_end))

    return jsonify(all_starts_ends)


if __name__ == "__main__":
    app.run(debug=True)