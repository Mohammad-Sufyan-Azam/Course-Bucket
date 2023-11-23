# Creating a flask backend for the index.html in Frontend folder

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
import requests
import pandas as pd
import json
import numpy as np
import html

import mydata as db


app = Flask(__name__, template_folder='', static_folder='')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route("/search_query", methods=['POST'])
def search_query_input():
    course_name = request.form['course'].strip().lower()
    price = request.form['price']
    university = request.form['institute'].strip()
    platform = request.form['platform'].strip().lower()

    results=db.executeQuery(course_name, price, university, platform)
    # print(results)

    json_results = json.dumps(results, ensure_ascii=True)
    print("Course name: ", course_name)
    print("Price: ", price)
    print("University: ", university)
    print("Platform: ", platform)
    print("-----------------------------------")

    return render_template("search.html", results=json_results)


@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        return jsonify(data)
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

