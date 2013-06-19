__author__ = 'javierAle'


from flask import Flask, jsonify, request, Response
from gp import Search


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/app/search', methods=['GET'])
def s_apps():
    q = request.args.get('q', None)  # ?q=some-value
    p = request.args.get('p', 1)

    search = Search(q)

    page = search.get_page(p)

    app_array = []

    apps = {
        'apps': app_array
    }

    #iterate through the apps on page 2. there are 24 apps/page
    for a in range(0,24):

        app_array.append({'name': page[a].get_name(), 'permissions' : page[a].get_permission()})
        # app_data.clear()
        # print page[a].get_name(), page[a].get_permission()

    resp = jsonify(apps)
    resp.status_code = 200
    return resp

@app.route('/app/compare', methods=['GET'])
def c_apps():
    q = request.args.get('q', 'twitter') # ?q=some-value
    p = request.args.get('p', 1)

    search = Search(q)

    # compare returns a Counter
    counter = search.compare_page(p)


    resp = jsonify(counter.most_common(30))
    resp.status_code = 200
    return resp

if __name__ == '__main__':
    app.run()