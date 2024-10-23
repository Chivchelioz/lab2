from flask import Flask, jsonify, request

app = Flask(__name__)

# Данные по авто в формате id, brand, model, year, price, mileage(пробег), color
cars = [
    {'id': 1, 'brand': 'Toyota', 'model': 'Camry', 'year': 2018, 'price': 20000, 'mileage': 30000, 'color': 'Red'},
    {'id': 2, 'brand': 'Honda', 'model': 'Civic', 'year': 2020, 'price': 22000, 'mileage': 25000, 'color': 'Blue'},
    {'id': 3, 'brand': 'VAZ', 'model': '2106', 'year': 1985, 'price': 5000, 'mileage': 510000, 'color': 'Cherry'},
    {'id': 4, 'brand': 'Toyota', 'model': 'mark II', 'year': 1992, 'price': 15000, 'mileage': 78200, 'color': 'Silver'},
    {'id': 5, 'brand': 'Nissan', 'model': '240SX', 'year': 1994, 'price': 11200, 'mileage': 51200, 'color': 'Yellow'},
    {'id': 6, 'brand': 'Nissan', 'model': 'Skyline', 'year': 1994, 'price': 123456, 'mileage': 20, 'color': 'Silver'},
    {'id': 7, 'brand': 'Mazda', 'model': 'RX-7', 'year': 1992, 'price': 1, 'mileage': 123456, 'color': 'Blue'},
]
#API запросы

# Получение всех автомобилей с возможностью сортировки(по умолчанию сортируется по id)
@app.route('/cars', methods=['GET'])
def get_cars():
    sort_by = request.args.get('sort_by', 'id')
    if sort_by not in cars[0]:
        return jsonify({'error': 'Invalid sort field'}), 400
    
    sorted_cars = sorted(cars, key=lambda x: x[sort_by])
    return jsonify(sorted_cars)

# Добавление нового автомобиля
@app.route('/cars', methods=['POST'])
def add_car():
    new_car = request.json
    new_car['id'] = len(cars) + 1
    cars.append(new_car)
    return jsonify(new_car), 201

# Удаление автомобиля по ID
@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    global cars
    cars = [car for car in cars if car['id'] != car_id]
    return '', 204

# Вычисление средней, максимальной и минимальной стоимости и пробега
@app.route('/cars/stats', methods=['GET'])
def car_stats():
    if not cars:
        return jsonify({'error': 'No cars available'}), 400
    
    prices = [car.get('price', 0) for car in cars if 'price' in car]  # Используем get и проверку наличия ключа
    mileages = [car.get('mileage', 0) for car in cars if 'mileage' in car]

    if not prices or not mileages:  # Проверяем, есть ли данные для расчетов
        return jsonify({'error': 'No valid data for price or mileage'}), 400
    
    return jsonify({
        'average_price': sum(prices) / len(prices),
        'max_price': max(prices),
        'min_price': min(prices),
        'average_mileage': sum(mileages) / len(mileages),
        'max_mileage': max(mileages),
        'min_mileage': min(mileages)
    })

if __name__ == '__main__':
    app.run(debug=True)
