import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import logging
from logging.config import dictConfig
import time, threading
import sys
import json
import base64
import io
import datetime
import math
app = Flask(__name__)

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    },
    'file': {
        'class': 'logging.FileHandler',
        'level': 'INFO',
        'formatter': 'default',
        'filename': 'applog.log',
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi','file']
    }
})

openai.api_key = os.getenv("OPENAI_API_KEY")

cache = {
    "nextStatus" : "empty",
    "next" : "",
}
def generateImage(p,res):
    response = openai.Image.create(
                prompt=p,
                n=1,
                size=f"{res}x{res}",
                response_format="b64_json"
            )
    image_data = response['data'][0]['b64_json']
    return image_data

def loadNextThread(p,res):
    app.logger.info("Loading asynchrounsly "+p+" ...")
    image_data = generateImage(p,res)
    cache['next'] = image_data
    cache['nextStatus'] = "ready"
    app.logger.info("Next image ready")
    return

def loadNext(p,res) :
    threading.Thread(target=loadNextThread,args=(p,res)).start()

@app.route("/stalagmiteBatch", methods=["GET"])
def stalagmiteBatch():
    p = request.args.get("prompt")
    num = int(request.args.get("num"))
    maxPerRequest = 10
    numRequests = math.ceil(num/maxPerRequest)
    numRemaining = num
    res=os.getenv("RESOLUTION")
    if p is None :
        p=os.getenv("PROMPT")

    # Get the current date and time as a string
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create a folder with the current date and time
    output_folder = os.path.join(os.getcwd(), current_time)
    os.makedirs(output_folder, exist_ok=True)

    fileNumber = 1
    for r in range(numRequests):
        numThisRequest = min(numRemaining,maxPerRequest)
        print("Generating {} images for promtp {}".format(numThisRequest,p))
        response = openai.Image.create(
                    prompt=p,
                    n=numThisRequest,
                    size=f"{res}x{res}",
                    response_format="b64_json")
        # Decode the base64-encoded image data

        for i, image in enumerate(response['data']):
            # Decode the base64-encoded image data
            image_data = base64.b64decode(image['b64_json'])

            # Create a unique file name for each image
            file_name = f"output_image_{fileNumber}.png"
            fileNumber += 1
            file_path = os.path.join(output_folder, file_name)

            # Save the image to the disk
            with open(file_path, 'wb') as f:
                f.write(image_data)

        numRemaining -= numThisRequest

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
       
@app.route("/stalagmite", methods=["GET"])
def index():
    p = request.args.get("prompt")
    res=os.getenv("RESOLUTION")
    if p is None :
        p=os.getenv("PROMPT")
        return render_template("stalagmite.html",res=res,prompt=p)
    else :
        image_data = ""
        if cache['nextStatus'] == "empty" :
            cache['nextStatus'] = "loading"
            loadNext(p,res)
        else :
            if cache['nextStatus'] == "loading" :
                waited = 0
                while cache['nextStatus'] == "loading" and waited < 30:
                    app.logger.info("Next image is still loading, sleeping...")
                    waited += 1
                    time.sleep(1)
            if cache['nextStatus'] == "ready" :
                image_data = cache['next']
                cache['nextStatus'] = "loading"
                loadNext(p,res)

        if image_data == "" :
            image_data = generateImage(p,res)

        return render_template("stalagmite.html", image_data=image_data,res=res,prompt=p)
