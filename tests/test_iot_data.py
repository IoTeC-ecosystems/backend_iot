def test_coordinates_ok(client):
    response = client.post('/iot_data/coordinates', json={
        "uuid": "c5ddb7f8-baf8-43b7-8caa-873cd0cd96c5",
        "latitude": 123.3,
        "longitude": 132.4,
        "height": 1750,
        "velocity": 10,
        "datetime": "11-07-2025 11:14.32"
    })
    assert response.json is not None
    assert response.json['status'] == 200
    assert response.json['error'] == 'success'

def test_coordinates_no_lat_lon_vel(client):
    gps_data = {
        'uuid': 'c5ddb7f8-baf8-43b7-8caa-873cd0cd96c5',
        "longitude": 132.4,
        "height": 1750,
        "velocity": 10,
        "datetime": "11-07-2025 11:14.32"
    }
    response = client.post('/iot_data/coordinates', json=gps_data)
    assert response is not None
    assert response.json['status'] == 400
    assert response.json['error'] == 'Lat'

    gps_data = {
        "uuid": "c5ddb7f8-baf8-43b7-8caa-873cd0cd96c5",
        "latitude": 123.3,
        "height": 1750,
        "velocity": 10,
        "datetime": "11-07-2025 11:14.32"
    }
    response = client.post('/iot_data/coordinates', json=gps_data)    
    assert response is not None
    assert response.json['status'] == 400
    assert response.json['error'] == 'Lon'

    gps_data = {
        "uuid": "c5ddb7f8-baf8-43b7-8caa-873cd0cd96c5",
        "latitude": 123.3,
        "longitude": 132.4,
        "height": 1750,
        "datetime": "11-07-2025 11:14.32"
    }
    response = client.post('/iot_data/coordinates', json=gps_data)
    assert response is not None
    assert response.json['status'] == 400
    assert response.json['error'] == 'Vel'

def test_coordinates_no_uuid(client):
    gps_data = {
        "latitude": 123.3,
        "longitude": 132.4,
        "height": 1750,
        "velocity": 10,
        "datetime": "11-07-2025 11:14.32"
    }
    response = client.post('/iot_data/coordinates', json=gps_data)
    assert response is not None
    assert response.json['status'] == 400
    assert response.json['error'] == 'UUID'

def test_coordinates_no_height_datetime(client):
    gps_data = {
        "uuid": "c5ddb7f8-baf8-43b7-8caa-873cd0cd96c5",
        "latitude": 123.3,
        "longitude": 132.4,
        "velocity": 10,
        "datetime": "11-07-2025 11:14.32"
    }
    response = client.post('/iot_data/coordinates', json=gps_data)
    assert response is not None
    assert response.json['status'] == 400
    assert response.json['error'] == 'Hgt'

    gps_data = {
        "uuid": "c5ddb7f8-baf8-43b7-8caa-873cd0cd96c5",
        "latitude": 123.3,
        "longitude": 132.4,
        "height": 1750,
        "velocity": 10,
    }
    response = client.post('/iot_data/coordinates', json=gps_data)
    assert response is not None
    assert response.json['status'] == 400
    assert response.json['error'] == 'DT'
