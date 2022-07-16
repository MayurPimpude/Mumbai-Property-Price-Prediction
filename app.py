import pickle
from warnings import catch_warnings
import numpy as np
from flask import Flask, redirect, render_template, request, jsonify, flash
from util import get_location_names, load_saved_artifacts, get_estimated_price
from importlib.resources import path
from flask_pymongo import PyMongo
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/todo_db"
mongodb_client = PyMongo(app)
db = mongodb_client.db
# mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")
            db.todos.insert_one({'name': name,
                                 'email': email,
                                 'message': message
                                 })
            # return print("data uploaded successfully")
        return flash("you are successfuly logged in")
    except:
        print("error")
    return render_template("contact.html")


@app.route('/get_location_names', methods=['GET'])
def get_location():
    response = jsonify({
        'locations': get_location_names()
    })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/pre', methods=['GET', 'POST'])
def pre():
    model = pickle.load(open('data/mumbai.pickle', 'rb'))

    price = jsonify({
        'estimated_price': get_estimated_price('worli', 500, 1, 0, 0)
    })

    print(price)
    return price


@app.route('/predict', methods=['GET', 'POST'])
def predictor():
    model = pickle.load(open('data/mumbai.pickle', 'rb'))
    price = None
    message = -1
    if request.method == "POST":
        Locations = request.form.get("Location")
        sqft = request.form.get("sqft")
        BHK = request.form.get("bhk")
        gym = request.form.get("gym")
        lift = request.form.get("lift")

        # print(gym,lift)

        if gym=='No':
            gym = 0
        else:
            gym=1


        if lift=='No':
            lift=0
        else:
            lift=1

        # print(gym,lift)

        price =  get_estimated_price(Locations,sqft,BHK,gym,lift)
        
        message = price
        
        return render_template("predict.html",message='Price Of House is {} lakhs'.format(price))
        
    return render_template("predict.html")

    #  return render_template("predict.html",predict_text='Price Of House is {} lakhs'.format(output))


if __name__ == "__main__":

    print("Starting Python Flask Server For Home Price Prediction...")
    load_saved_artifacts()

    app.run(debug=True)
