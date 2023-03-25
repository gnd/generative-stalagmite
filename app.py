import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import logging
from logging.config import dictConfig

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

@app.route("/stalagmite", methods=["GET"])
def index():
    p = request.args.get("prompt")
    res=os.getenv("RESOLUTION")
    if p is None :
        p=os.getenv("PROMPT")
        return render_template("stalagmite.html",res=res,prompt=p)
    else :
        response = openai.Image.create(
        prompt=p,
        n=1,
        size=f"{res}x{res}"
        )
        image_url = response['data'][0]['url']
        app.logger.info(image_url)
        return render_template("stalagmite.html", image_url=image_url,res=res,prompt=p)
