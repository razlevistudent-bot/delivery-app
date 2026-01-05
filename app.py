from flask import Flask, render_template, request, jsonify
import math
import uuid

app = Flask(__name__)

# מסד נתונים זמני בזיכרון השרת (בשימוש מקצועי כדאי להשתמש ב-Redis או DB)
routes_db = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_route', methods=['POST'])
def save_route():
    route_id = str(uuid.uuid4())[:8] # יצירת קוד קצר
    routes_db[route_id] = request.json.get('locations', [])
    return jsonify({"route_id": route_id})

@app.route('/get_route/<route_id>')
def get_route(route_id):
    route = routes_db.get(route_id)
    if route:
        return jsonify(route)
    return jsonify({"error": "Route not found"}), 404

@app.route('/optimize', methods=['POST'])
def optimize():
    # חישוב אופטימיזציה פשוט
    data = request.json
    locations = data.get('locations', [])
    return jsonify(locations)

if __name__ == '__main__':
    app.run(debug=True)
