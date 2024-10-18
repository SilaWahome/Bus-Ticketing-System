from flask import Flask, render_template, request, jsonify
import pandas as pd
import datetime

app = Flask(__name__)

# Read Excel file
excel_file = r"C:\Users\allan\Desktop\Routes.xlsx"
df = pd.read_excel(excel_file)

# Process Excel data to extract routes information
routes_data = []
for index, row in df.iterrows():
    route_info = {
        "planner": row['Planner'],
        "routes": row['Routes'],
        "fare": row['Fare'],
        "from": row['From'],
        "thru": row['Thru'],
        "destination": row['Destination']
    }
    routes_data.append(route_info)

# Function to calculate fare
def calculate_fare(one_way):
    base_fare = 100
    if one_way == 'no':
        return base_fare * 2 * 0.8  # 20% discount for two-way
    return base_fare

@app.route('/')
def index():
    return render_template('index.html', routes=routes_data)

@app.route('/book', methods=['POST'])
def book():
    data = request.json
    from_location = data['from']
    destination = data['destination']
    one_way = data['one_way']
    
    # Calculate fare
    fare = calculate_fare(one_way)
    
    # Generate ticket
    ticket = {
        "from": from_location,
        "destination": destination,
        "fare": fare,
        "one_way": one_way,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return jsonify(ticket)

if __name__ == '__main__':
    app.run(debug=True)
