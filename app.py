import geocoder
import requests
#import folium
import re
from flask import Flask, render_template, request, redirect, jsonify


app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/index')

@app.route('/index')
def index():

    def get_vehicle_id(vehicle_number):
        vehicle_id = vehicles_info[vehicle_number]['MonitoredVehicleJourney']['VehicleRef']
        match = re.search(r'\_(\d+)$', vehicle_id)
        if match:
            vehicle_id = match.group(1)
        else:
            vehicle_id = 0
        return vehicle_id

    '''
    payload = {'key': '740c5f9a-c180-42e0-bafc-5723516152bf',
               'version': '2',
               'VehicleMonitoringDetailLevel': 'minimum'}
    url = 'http://bustime.mta.info/api/siri/vehicle-monitoring.json'
    mta_json = requests.get(url, params=payload).json()
    vehicles_info = mta_json['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    vehicle_ids = [get_vehicle_id(x) for x in range(0, 10)]
    '''

    vehicle_ids = ['3846', '430', '4223', '2520', '453', '3967', '2735', '4198', '4710', '6429']
    return render_template('index.html', vehicle_ids=vehicle_ids)

@app.route('/getMap', methods=['POST'])
def getMap():
    vehicle_id = request.form['vehicle_id']
    payload = {'key': '740c5f9a-c180-42e0-bafc-5723516152bf',
               'version': '2',
               'VehicleRef': vehicle_id,
               'VehicleMonitoringDetailLevel': 'minimum'}
    url = 'http://bustime.mta.info/api/siri/vehicle-monitoring.json'
    mta_json = requests.get(url, params=payload).json()
    vehicles_info = mta_json['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    (vehicle_lat, vehicle_lng) = (vehicles_info[0]['MonitoredVehicleJourney']['VehicleLocation']['Latitude'],
                                  vehicles_info[0]['MonitoredVehicleJourney']['VehicleLocation']['Longitude'])
    (center_lat, center_lng) = (vehicle_lat, vehicle_lng)
    popup_text = 'Bus: %s' % vehicle_id
    return render_template('map.html', vehicle_id=vehicle_id, vehicle_lat=vehicle_lat, vehicle_lng=vehicle_lng,
                           popup_text=popup_text,
                           center_lat=center_lat, center_lng=center_lng)

@app.route('/getPosition', methods=['GET'])
def getPosition():
    vehicle_id = request.args.get('vehicle_id')
    payload = {'key': '740c5f9a-c180-42e0-bafc-5723516152bf',
               'version': '2',
               'VehicleRef': vehicle_id,
               'VehicleMonitoringDetailLevel': 'minimum'}
    url = 'http://bustime.mta.info/api/siri/vehicle-monitoring.json'
    mta_json = requests.get(url, params=payload).json()
    vehicles_info = mta_json['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    (vehicle_lat, vehicle_lng) = (vehicles_info[0]['MonitoredVehicleJourney']['VehicleLocation']['Latitude'],
                                  vehicles_info[0]['MonitoredVehicleJourney']['VehicleLocation']['Longitude'])
    return jsonify(vehicle_lat=vehicle_lat,
                   vehicle_lng=vehicle_lng)

if __name__ == '__main__':
    app.run()
