from flask import Flask, request, jsonify, make_response
import secrets
from structures.project import Project
from lru_cache import LRUcache

app = Flask(__name__)

cache = LRUcache(100)

@app.route("/")
def index():
    return "MCDA Server"

@app.route("/cache")
def cache_size():
    return "Cache Size: " + str(cache.keys.size)

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    printInfo = request.args.get('printinfo')
    token = request.cookies.get('token')
    info = None
    if token is not None and cache.contains(token) and cache.get(token).diff(data):
        # when token exists, not expired and its corresponding project structure is same as data
        # we can reuse the project
        info = cache.get(token).perform_without_build(data, True if printInfo is not None else False)
        print('hit lru cache!')
        info['hit'] = True
    else:
        project = Project('lsp')
        info = project.perform(data, True if printInfo is not None else False)
        token = secrets.token_urlsafe(16)
        cache.put(token, project)
        info['hit'] = False
    response = make_response(jsonify(info))
    response.set_cookie('token', token, max_age=60*60*24) # cookie will last for one day
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)