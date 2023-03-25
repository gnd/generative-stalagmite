import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import logging
from logging.config import dictConfig
import time, threading

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
                size=f"{res}x{res}"
            )
    image_url = response['data'][0]['url']
    return image_url

def loadNextThread(p,res):
    app.logger.info("Loading asynchrounsly "+p+" ...")
    image_url = generateImage(p,res)
    cache['next'] = image_url
    cache['nextStatus'] = "ready"
    app.logger.info("Next image ready")
    return

def loadNext(p,res) :
    threading.Thread(target=loadNextThread,args=(p,res)).start()

@app.route("/stalagmite", methods=["GET"])
def index():
    p = request.args.get("prompt")
    res=os.getenv("RESOLUTION")
    if p is None :
        p=os.getenv("PROMPT")
        return render_template("stalagmite.html",res=res,prompt=p)
    else :
        image_url = ""
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
                image_url = cache['next']
                cache['nextStatus'] = "loading"
                loadNext(p,res)

        if image_url == "" :
            image_url = generateImage(p,res)

        app.logger.info(image_url)
        return render_template("stalagmite.html", image_url=image_url,res=res,prompt=p)
