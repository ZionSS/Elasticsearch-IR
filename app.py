from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import os
app = Flask(__name__)
es = Elasticsearch(['http://elastic:NgDg1vTQeobEwPYgc2Gx@localhost:9200'])

picFolder = os.path.join('static','img')
app.config['UPLOAD_FOLDER'] = picFolder


@app.route('/')
def home():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    print(logo)
    return render_template('index.html', user_image=logo)


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(
        index="netflix_title",
        size=1000,
        body={
            "min_score": 1,
            "query": {
                "bool": {
                    "should": [
                        {
                            "multi_match": {
                                "query": search_term,
                                "fields": [
                                    "title",
                                    "release_year"
                                    "listed_in",
                                    "description"
                                ],
                                "type": "most_fields",
                                "operator": "and",
                                "boost": 10
                            }
                        },
                        {
                            "multi_match": {
                                "query": search_term,
                                "fields": [
                                    "title",
                                    "release_year"
                                    "listed_in",
                                    "description"
                                ],
                                "type": "most_fields",
                                "operator": "and",
                                "fuzziness": "AUTO",
                                "boost": 5
                            }
                        },
                        {
                            "multi_match": {
                                "query": search_term,
                                "fields": [
                                    "title",
                                    "release_year"
                                    "listed_in",
                                    "description"
                                ],
                                "type": "most_fields",
                                "boost": 1
                            }
                        },
                        {
                            "multi_match": {
                                "query": search_term,
                                "fields": [
                                    "title",
                                    "release_year"
                                    "listed_in",
                                    "description"
                                ],
                                "type": "most_fields",
                                "boost": 0.5,
                                "fuzziness": "AUTO"
                            }
                        }
                    ],
                    "must": [], "must_not": [], "filter": []
                }
            }
        }
    )
    return render_template('result.html', res=res)


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='localhost', port=5000)
