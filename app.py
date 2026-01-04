from flask import Flask, render_template, request, jsonify
import math
import requests
import time

app = Flask(__name__)

def calculate_distance(p1, p2):
    return math.sqrt((p1['lat'] - p2['lat'])**2 + (p1['lng'] - p2['lng'])**2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/batch_import', methods=['POST'])
def batch_import():
    addresses = request.json.get('addresses', [])
    results = []
    
    for addr in addresses:
        if not addr: continue
        try:
            # שליחת בקשה לשרת המפות מהשרת של Render
            response = requests.get(
                f"https://nominatim.openstreetmap.org/search?format=json&q={addr}",
                headers={'User-Agent': 'DeliveryApp/1.0'}
            ).json()
            
            if response:
                results.append({
                    'name': addr,
                    'lat': float(response[0]['lat']),
                    'lng': float(response[0]['lon']),
                    'phone': '',
                    'completed': False
                })
            # השהייה קלה כדי לא להיחסם
            time.sleep(1)
        except Exception as e:
            print(f"Error geocoding {addr}: {e}")
            
    return jsonify(results)

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.json
    locations = data.get('locations', [])
    if not locations: return jsonify([])
    
    unvisited = locations
    optimized_route = [unvisited.pop(0)]
    while unvisited:
        last_node = optimized_route[-1]
        next_node = min(unvisited, key=lambda x: calculate_distance(last_node, x))
        optimized_route.append(next_node)
        unvisited.remove(next_node)
    return jsonify(optimized_route)

if __name__ == '__main__':
    app.run(debug=True)
