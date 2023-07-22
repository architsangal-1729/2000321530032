from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 60})

from flask import Flask, request, jsonify

app = Flask(__name__)

registered_company_roll_number = "2000321530032"
access_code = None

@app.route('/register', methods=['POST'])
def register_company():
    global access_code
    data = request.get_json()
    received_roll_number = data.get('roll_number')
    received_access_code = data.get('access_code')

    if received_roll_number == registered_company_roll_number:
        access_code = received_access_code
        return jsonify({'message': 'Registration successful!'}), 200
    else:
        return jsonify({'error': 'Invalid roll number or access code'}), 401
def authenticate_with_railways_api():
    global access_code
    # Make an API call to John Doe Railways API to get the authentication token
    # The details of how this works will be provided by John Doe Railways documentation
    authentication_token = "qxrwbC"
    return authentication_token
def fetch_train_data():
    # Sample train data - Replace this with actual API call to John Doe Railways
    trains_data = [
        {
"trainName": "Hyderabad Exp",
"trainNumber": "2341",
"departureTime": {
"Hours": 23,
"Minutes" : 55,
"Seconds": 0
},
"seatsAvailable": {
"sleeper": 6,
"AC": 7
},
"price": {
"sleeper": 554,
"AC": 1854
},
"delayedBy": 5
        },
        {
"trainName": "Chennai Exp",
"trainNumber": "2344",
"departureTime": {
"Hours": 21,
"Minutes":35,
"Seconds": 0
},
"seatsAvailable": {
"sleeper": 3,
"AC": 1
},
"price": {
"sleeper": 2,
"AC": 5
},
"delayedBy": 15
        },
        
    ]
    return trains_data

from datetime import datetime, timedelta

def calculate_actual_departure_time(train):
    scheduled_departure_time = datetime.strptime(train['scheduled_departure_time'], '%H:%M')
    delay_in_minutes = train['delay_in_minutes'] if 'delay_in_minutes' in train else 0
    actual_departure_time = scheduled_departure_time + timedelta(minutes=delay_in_minutes)
    return actual_departure_time.strftime('%H:%M')

def update_seat_availability_and_pricing(train):
    # Assuming the train API response contains seat_availability and pricing fields
    # Here, you can implement logic to update seat availability and pricing based on market conditions
    updated_seat_availability = train['seat_availability']
    updated_pricing = train['pricing']
    return updated_seat_availability, updated_pricing

def sort_trains(trains):
    trains.sort(key=lambda x: (x['pricing'], -x['seat_availability'], calculate_actual_departure_time(x)))
    return trains

def prepare_response(trains):
    response = []
    for train in trains:
        actual_departure_time = calculate_actual_departure_time(train)
        sleeper_seat_availability, sleeper_pricing = update_seat_availability_and_pricing(train['sleeper'])
        ac_seat_availability, ac_pricing = update_seat_availability_and_pricing(train['ac'])

        train_details = {
            'train_name': train['train_name'],
            'departure_time': actual_departure_time,
            'arrival_time': train['arrival_time'],
            'sleeper_seat_availability': sleeper_seat_availability,
            'sleeper_pricing': sleeper_pricing,
            'ac_seat_availability': ac_seat_availability,
            'ac_pricing': ac_pricing
        }
        response.append(train_details)

    return response

@app.route('/trains', methods=['GET'])
@cache.cached()
def get_train_schedules():
    trains_data = fetch_train_data()
    current_time = datetime.now().strftime('%H:%M')
    valid_trains = [train for train in trains_data if calculate_actual_departure_time(train) >= current_time]

    sorted_trains = sort_trains(valid_trains)
    response = prepare_response(sorted_trains)
    return jsonify(response), 200
