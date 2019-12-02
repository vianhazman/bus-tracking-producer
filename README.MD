## Tracking Data Simulator
This project schedules coordinate GPS data and
 trip information every 5 seconds using Airflow.
 The GPS data were directly mirrored to Kafka and the trip data is 
 ingested to Postgres to simulate CDC. 
 
 To run:
 ```
docker-compose up
```

Initiate DB using
```angular2
./utils/init_table.sh
```

Project Structure:
![Alt text](https://gist.githubusercontent.com/vianhazman/f465d9971ba101dfa39a3cfcd3eb65c0/raw/cf3be2ccaa16a2df6d447922565a418d1f907c23/System%2520Diagram.png "Overall Project")

Services to run:
 - Zookeeper
 - Kafka Broker
 - Airflow
 - PostgreSQL with wal2json
 - Debezium