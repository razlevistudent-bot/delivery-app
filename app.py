from flask import Flask, render_template, request, jsonify
import uuid

app = Flask(__name__)
# מסד נתונים זמני (חשוב: ב-Render הזיכרון מתאפס מדי פעם, בשימוש אמיתי מומלץ DB)
routes_db = {} 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_route', methods=['POST'])
def save_route():
    try:
        data = request.get_json()
        if not data or 'locations' not in data:
            return jsonify({"error": "No data"}), 400
            
        route_id = str(uuid.uuid4())[:8]
        routes_db[route_id] = {"locations": data['locations']}
        return jsonify({"route_id": route_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_route/<route_id>')
def get_route(route_id):
    route = routes_db.get(route_id)
    if route:
        return jsonify(route)
    return jsonify({"error": "Route not found"}), 404

@app.route('/update_status/<route_id>', methods=['POST'])
def update_status(route_id):
    if route_id in routes_db:
        routes_db[route_id]["locations"] = request.json.get('locations')
        return jsonify({"status": "updated"})
    return jsonify({"error": "not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
