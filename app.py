import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
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
        return render_template("stalagmite.html", image_url=image_url,res=res,prompt=p)
