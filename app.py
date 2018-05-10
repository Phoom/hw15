#################################################
# import dependencies
#################################################
from flask import Flask, render_template, jsonify, redirect
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# sqlite : connect to the existing database
#################################################
engine = create_engine("sqlite:///belly_button_biodiversity.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
OTU = Base.classes.otu
Samples = Base.classes.samples
SamplesMetadata = Base.classes.samples_metadata
session = Session(engine)


@app.route('/')
def index():
    return render_template('index.html')
    ##Return the dashboard homepage.


@app.route('/names')
def names():

    # Grab all the results
    results = session.query(SamplesMetadata.SAMPLEID).all()

    # Create Sample List
    samples_list = []


    #For each sample, append BB_ and add to list
    for samples in results:
        currentSample = samples.SAMPLEID
        addSample = ("BB_" +str(currentSample))
        print(addSample)
        samples_list.append(addSample)

    # return the jsonify samples list
    return jsonify(samples_list)


 # ,methods=['POST','GET']
@app.route("/otu")
def otu():
    otu_desc = session.query(OTU.lowest_taxonomic_unit_found).all()
    otu_descriptions = [i[0] for i in otu_desc]
    return jsonify(otu_descriptions)



@app.route('/metadata/<sample>')
def metadata(sample):

    results = session.query(SamplesMetadata).filter(SamplesMetadata.SAMPLEID == sample[3:]).all()

    for samples in results:
        samples_dict = {}
        samples_dict["AGE"] = samples.AGE
        samples_dict["BBTYPE"] = samples.BBTYPE
        samples_dict["ETHNICITY"] = samples.ETHNICITY
        samples_dict["GENDER"] = samples.GENDER
        samples_dict["LOCATION"] = samples.LOCATION
        samples_dict["SAMPLEID"] = samples.SAMPLEID

    return jsonify(samples_dict)

@app.route('/wfreq/<sample>')
def wfreq(sample):
    # Returns an integer value for the weekly washing frequency `WFREQ`
    results = session.query(SamplesMetadata.WFREQ).filter(SamplesMetadata.SAMPLEID == sample[3:]).all()
    return jsonify(results[0][0]);



@app.route('/samples/<sample>')
def samples(sample):

    results = session.query(Samples.otu_id,getattr(Samples, sample)).order_by(getattr(Samples, sample).desc()).all()

    dict1 = {}
    list1 = []
    list2 = []
    list3 = []
    for x in results:
        if(x[1] > 0):
            list1.append(x[0])
            list2.append(x[1])
    dict1['otu_id'] = list1
    dict1['sample_values'] = list2
    list3.append(dict1)

    list3

    return jsonify(list3)


if __name__ == "__main__":
    app.run(debug=True)
