from flask import Flask, request, jsonify
from edge_db import EdgeDatabase
import time
db = EdgeDatabase('localhost', 5432)

app = Flask(__name__, static_folder=None)
start = time.time()
@app.route('/latest-login', methods=['GET'])
def getLatestLogin():
    data = db.getLogs(1)[0] 
    res = {'id': data[0], 'time': data[1], 'device': data[2]}
    return jsonify(res)

@app.route('/')
def stat():
    urls = app.url_map.iter_rules()
    l = []
    for x in urls:
        l.append(x.rule)
    return jsonify({'runtime': time.time() - start, 'endpoints': l})

@app.route('/logs')
def getLogs():
    amount = request.args.get('qty')
    if amount == None:
        amount = 10
    else:
        try:
            amount = int(amount)
        except:
            amount = 10
    raw = db.getLogs(amount)

    data = []
    for x in raw:
        obj = {'id': x[0], 'time': x[1], 'device': x[2]}
        data.append(obj)
    return jsonify({'result': data})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
