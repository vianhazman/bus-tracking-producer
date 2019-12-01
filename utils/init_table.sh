#!/bin/bash
psql -U postgres -h localhost -c "CREATE DATABASE BUS_TRIP;"
psql -U postgres -h localhost -d bus_trip -a -f "init_table.sql"

curl -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '
{
	"name": "trip-data-connector",
	"config": {
	  "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
	  "tasks.max": "1",
	  "database.hostname": "pg-docker",
	  "database.port": "5432",
	  "database.user": "postgres",
	  "database.password": "postgres",
	  "database.dbname": "bus_trip",
	  "database.server.name": "pg1",
	  "database.whitelist": "bus_trip",
	  "database.history.kafka.bootstrap.servers": "kafka1:19092",
	  "database.history.kafka.topic": "schema-changes.trip"
	}
  }'

curl -X GET -H "Accept:application/json" localhost:8083/connectors/trip-data-connector