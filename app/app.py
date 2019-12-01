import argparse
import requests
import yaml
from sqlalchemy import create_engine
from kafka import KafkaProducer
import time
from json import dumps


class TransjakartaData:

    def __init__(self, variables):
        self.payload = requests.get(variables['endpoint']).json()['buswaytracking']

    def get_tracking_data(self):
        tracking_data = [{"bus_code": i['buscode'],
                          "longitude": i['longitude'],
                          "latitude": i['latitude'],
                          "gps_timestamp": i['gpsdatetime']} for i in self.payload]
        return tracking_data

    def get_trip_data(self):
        trip_data = [{"trip_id": b['current_tripid'],
                      "buscode": b['buscode'],
                      "koridor": b['koridor'],
                      "color": b["color"]} for b in self.payload if b['current_tripid'] is not '0']
        return trip_data


class DatabaseConnector:

    def __init__(self, variables):
        self.settings = {
            'user': variables['database']['username'],
            'pass': variables['database']['password'],
            'host': variables['database']['host'],
            'db': variables['database']['db'],
            'port': variables['database']['port']
        }
        url_db = 'postgresql+psycopg2://{user}:{pass}@{host}:{port}/{db}'.format(
            **self.settings)
        self.engine = create_engine(url_db, client_encoding='utf8')

    def insert_trip_data(self, trip_data):
        for i in trip_data:
            self.engine.execute(QueryList.get_bus_insert_query(i))
            self.engine.execute(QueryList.get_trip_insert_query(i))


class KafkaSender:

    def __init__(self, variables):
        self.producer = KafkaProducer(bootstrap_servers=[variables['kafka_host']],
                                 value_serializer=lambda x:
                                 dumps(x).encode('utf-8'))

    def loop_and_send_gps_data(self,gps_data):
        for i in gps_data:
            self.producer.send('trackingtj', value=i)


class QueryList:

    @staticmethod
    def get_trip_insert_query(trip_data):
        query = open('/usr/local/airflow/dags/sql/insert_query_trip.sql', 'r')
        statement = query.read()
        query.close()
        statement = statement.format(trip_id= trip_data['trip_id'], bus_code= trip_data['buscode'],koridor = trip_data['koridor'])
        return statement

    @staticmethod
    def get_bus_insert_query(trip_data):
        query = open('/usr/local/airflow/dags/sql/insert_query_bus.sql', 'r')
        statement = query.read()
        query.close()
        statement = statement.format(bus_code= trip_data['buscode'],color = trip_data['color'])
        return statement

    @staticmethod
    def get_update_query():
        UPDATE_QUERY = ''
        return UPDATE_QUERY


start_time = time.time()


with open('/usr/local/airflow/dags/variables.yaml') as var:
    variables = yaml.load(var)

    tj = TransjakartaData(variables)

    kafka = KafkaSender(variables)
    kafka.loop_and_send_gps_data(tj.get_tracking_data())

    db = DatabaseConnector(variables)
    db.insert_trip_data(tj.get_trip_data())

print("--- data scrapping finished ---")
print("--- execution delta: %s seconds ---" % (time.time() - start_time))

