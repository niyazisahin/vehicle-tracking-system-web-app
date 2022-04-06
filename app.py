
from crypt import methods
from flask import Flask, render_template, url_for, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from numpy import where
import slate3k as slate
import io
import pymongo
from pymongo.server_api import ServerApi
from sqlalchemy import true
import threading
import zmq
from flask_executor import Executor
import datetime


client = pymongo.MongoClient(
    "mongodb+srv://Charon:cufcuf@navigation.xptsq.mongodb.net/VehicleMonitor?retryWrites=true&w=majority", server_api=ServerApi('1'))
database = client["VehicleMonitor"]
collection = database["Vehicles"]
collection2 = database["VehicleRelations"]
collection3 = database["UserLog"]


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
current_user = None
current_admin = None

executor = Executor(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.id}> => Email:{self.email},Password{self.password}"


@app.route('/')
def index():
    return redirect("/login", code=302)


@app.route('/login')
def user_login():
    return render_template("user_login.html")


@app.route('/login', methods=['GET', 'POST'])
def user_login_post():
    global current_user
    email = request.form['email']
    password = request.form['password']
    current_user = User.query.filter_by(email=email, password=password).first()

    return redirect("/index", 302)


@app.route('/index')
def user_index():
    global current_user

    if current_user:
        time = datetime.datetime.now()
        date = datetime.datetime.strftime(time, '%c')
        collection3.insert_one({"UserID" : current_user.id, "Date" : date})
        return render_template("user_index.html")
    else:
        return redirect("/login", 302)


@app.route('/signup')
def signup():
    return render_template("user_signup.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup_post():

    email = request.form['email']
    password = request.form['password']
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect("/login", 302)


@app.route('/logout')
def user_logout():
    global current_user
    current_user = None
    return redirect('/login', 302)


@app.route('/map', methods=["POST", "GET"])
def user_map():

    if not current_user:
        return redirect("/login", 302)

    id = int(request.args.get('vehicle-id'))
    sure1 = request.args.get("slider-value")
    sure2 = request.args.get("slider2-value")

    s1, d1 = sure1.split(":")
    s2, d2 = sure2.split(":")

    sure_total1 = int(s1) * 60 + int(d1)
    sure_total2 = int(s2) * 60 + int(d2)

    print(sure1)
    print(sure2)

    data_vehicle = []

    if id == 999:
        data = get_vehicles_id(current_user.id)

        for _id in data:

            tmp = collection.find({"Id": str(_id["VehicleID"])})
            
            tmp = list(tmp)

            tmp = tmp[:24*60]
            tmp = tmp[sure_total1:sure_total2]

            data_vehicle += tmp

    else:
        data = get_vehicles_id(current_user.id)

        data_vehicle = collection.find({"Id": str(id)})


        data_vehicle = list(data_vehicle)

        data_vehicle = data_vehicle[:24*60]
        data_vehicle = data_vehicle[sure_total1:sure_total2]

    

    ids = [999]
    for i in data:
        print(i)
        ids.append(int(i["VehicleID"]))

    if (id not in ids):
        print("****** GİRDİM *****")
        return redirect("/vehicles", 302)

    if current_user:
        return render_template("user_map.html", data=data_vehicle)
    else:
        return redirect("/login", 302)


@app.route('/vehicles')
def user_vehicles():

    if current_user:

        data = get_vehicles_id(current_user.id)
        return render_template('user_vehicles.html', data=data)
    else:
        return redirect("/login", 302)


def get_vehicles_id(userID):

    vehicles = []

    for i in collection2.find({"UserID": userID}):
        vehicles.append(i)

    return vehicles


def broker_reciever():

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    print("bağlandık gardaşşşş")

    # try:
    while True:

        socket.send_string("Data received")

        #  Get the reply.
        message = socket.recv().decode()

        no, date, cord1, cord2, id = message.split()
        date = no + " " + date

        collection.insert_one(
            {"Date": date, "Cord1": cord1, "Cord2": cord2, "Id": id})
        print("******* Veri gönderdim ********")


if __name__ == '__main__':
    broker_t = threading.Thread(target=broker_reciever)
    broker_t.daemon = True
    broker_t.start()
    app.run(debug=True)
