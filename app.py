from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def calculate_distance(p1, p2):
    return math.sqrt((p1['lat'] - p2['lat'])**2 + (p1['lng'] - p2['lng'])**2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.json
    locations = data.get('locations', [])
    if not locations:
        return jsonify([])
    
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
