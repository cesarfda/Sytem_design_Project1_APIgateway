import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config['MONGO_URI'] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    
    if not err:
        return token, 200
    else:
        return err
    
@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token()
    
    access = json.loads(access)
    
    if access["admin"]:
        if len(request.files) == 1:
            for _, file in request.files.items():
                err = util.upload(file, fs, channel, access)
                
                if err:
                    return err, 500
                
            return "File uploaded", 200
        else:
            return "Exactly 1 file required", 400
        
    else:
        return "You do not have permission to upload", 401
    
@server.route("/download", methods=["GET"])
def download():
    pass

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)