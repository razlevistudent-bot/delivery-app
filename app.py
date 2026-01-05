from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    # פונקציה זו נשארת כגיבוי, החישוב החי מבוצע ב-JS
    data = request.json
    locations = data.get('locations', [])
    return jsonify(locations)

if __name__ == '__main__':
    app.run(debug=True)
