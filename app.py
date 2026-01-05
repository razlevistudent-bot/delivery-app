from flask import Flask, render_template, request, jsonify
import uuid

app = Flask(__name__)
routes_db = {} # מסד נתונים זמני בזיכרון

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_route', methods=['POST'])
def save_route():
    route_id = str(uuid.uuid4())[:8]
    routes_db[route_id] = {"locations": request.json.get('locations', [])}
    return jsonify({"route_id": route_id})

@app.route('/get_route/<route_id>')
def get_route(route_id):
    return jsonify(routes_db.get(route_id, {"locations": []}))

@app.route('/update_status/<route_id>', methods=['POST'])
def update_status(route_id):
    if route_id in routes_db:
        routes_db[route_id]["locations"] = request.json.get('locations')
        return jsonify({"status": "updated"})
    return jsonify({"error": "not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
