from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import itertools

app = Flask(__name__)
# הגדרת שירות המפות - הוספנו user_agent ייחודי
geolocator = Nominatim(user_agent="israel_delivery_optimizer_v1")

def calculate_route_distance(route):
    total_dist = 0
    for i in range(len(route) - 1):
        total_dist += geodesic(route[i]['coords'], route[i+1]['coords']).km
    return total_dist

def get_optimized_route(locations):
    # אלגוריתם שבודק את כל האפשרויות למציאת המסלול הקצר ביותר
    best_route = None
    min_distance = float('inf')
    
    # הגבלה ל-9 כתובות כדי למנוע קריסה של המחשב (חישוב עצרת)
    actual_locations = locations[:9] 
    
    for route in itertools.permutations(actual_locations):
        current_distance = calculate_route_distance(route)
        if current_distance < min_distance:
            min_distance = current_distance
            best_route = route
            
    return best_route, round(min_distance, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        address_list = request.form.get('addresses').split('\n')
        locations = []
        
        for addr in address_list:
            addr = addr.strip()
            if addr:
                try:
                    # הוספת "ישראל" עוזרת למנוע טעויות עם ערים בחו"ל
                    location = geolocator.geocode(f"{addr}, Israel", timeout=10)
                    if location:
                        locations.append({
                            'address': addr,
                            'coords': (location.latitude, location.longitude)
                        })
                except:
                    continue
        
        if len(locations) > 1:
            optimized_route, total_km = get_optimized_route(locations)
            return render_template('results.html', route=optimized_route, distance=total_km)
        
    return render_template('index.html')

if __name__ == '__main__':
    # הרצה על פורט 5001 כדי למנוע התנגשויות ב-Mac
    app.run(debug=True, port=5001, host='0.0.0.0')