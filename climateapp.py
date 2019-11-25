import numpy as np 

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

################################################
#Database Setup
################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base=automap_base()

Base.prepare(engine,reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station 

################################################
#Flask Setup
################################################
app = Flask(__name__)

################################################
#Flask Routes
################################################

@app.route("/")
def home():
    """List all routes that are available"""
    return (
        f"Available Route:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltstart&gt<br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(Measurement.prcp, Measurement.date).all()
    
    session.close()

    all_precipitation=[]
    for prcp, date in results:
        precip_dict={}
        precip_dict["prcp"] = prcp
        precip_dict["date"] = date
        all_precipitation.append(precip_dict)
   
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def station():

    session = Session(engine)

    results = session.query(Measurement.station).group_by(Measurment.station).all()
 
    session.close()

    all_station = list(np.ravel(results))
   
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.date > '2016-08-23').all()

    session.close()
    
    all_tobs =  list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/&ltstart&gt")
def start(startdate):
    
    session = Session(engine)

    results = (session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
              filter(Measurement.date == startdate).all())

    session.close()

    startdateresults = list(np.ravel(results))

    return startdateresults

    return jsonify(startdateresults)

@app.route("/api/v1.0/&ltstart&gt/&ltend&gt")
def startend(startdate,enddate):
    
    session = Session(engine)

    results = (session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
              filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all())

    session.close()

    startendresults = list(np.ravel(results))

    return jsonify(startendresults)


if __name__ == '__main__':
    app.run(debug=True)
