from flask import Flask
from flask import jsonify
from flask import request
from datetime import datetime
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)
CORS(app)

@app.route('/ping-test')
def pingTest():
    return 'Hello, World!'

@app.route('/sendchat/', methods = ['POST'])
def postChat():

    # {
    #     "sender": "JayZ",
    #     "receiver": "Jiali",
    #     "message": "Does this work"
    # }

    content = request.get_json()
    
    if request.is_json:
        doc_ref = db.collection(u'users').document(content['sender']).collection(content['receiver']).document(datetime.now().strftime('%Y%m%d%H%M%S'))
        doc_ref.set({
           "content" : content['message'],
           "sender" : content['sender']
        }, merge=True)

        doc_ref = db.collection(u'users').document(content['receiver']).collection(content['sender']).document(datetime.now().strftime('%Y%m%d%H%M%S'))
        doc_ref.set({
           "content" : content['message'],
           "sender" : content['sender']
        }, merge=True)
        return 'message sent', 201
    else:
        return 'message error', 420

@app.route('/getchat/', methods = ['POST'])
def getChat():

    # {
    #     "sender": "JayZ",
    #     "receiver": "Jiali"
    # }

    content = request.get_json()
    if request.is_json:
        users_ref = db.collection(u'users').document(content['sender']).collection(content['receiver'])
        docs = users_ref.stream()
        toList = list()
        for doc in docs:
            toList.append(doc.to_dict())

        toReturn = {"message" : toList}
        return jsonify(toReturn), 201

    else:
        return 'message error', 420

@app.route('/gettrip/', methods = ['GET'])
def getTrips():
    users_ref = db.collection(u'trips')
    docs = users_ref.stream()

    toList = list()
    for doc in docs:
        toList.append(doc.to_dict())

    toReturn = {"trips" : toList}
    return jsonify(toReturn), 201

@app.route('/sendtrip/', methods = ['POST'])
def postTrips():
    # {
    #     "description": "I love batam.",
    #     "destination": "Batam",
    #     "enddate": "28/02/2019",
    #     "host": "JZ",
    #     "limit": 2,
    #     "startdate": "24/02/2019"
    # }

    content = request.get_json()
    
    if request.is_json:
        doc_ref = db.collection(u'trips').document(datetime.now().strftime('%Y%m%d%H%M%S'))
        doc_ref.set({
            "description": content['description'],
            "destination": content['destination'],
            "enddate": content['enddate'],
            "host": content['host'],
            "limit": content['limit'],
            "startdate": content['startdate']
        }, merge=True)
        return 'message sent', 201
    else:
        return 'message error', 420
