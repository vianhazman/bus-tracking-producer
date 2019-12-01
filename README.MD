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