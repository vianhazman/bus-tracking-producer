#!/bin/bash
psql -U postgres -h localhost -d bus_trip -c "DELETE FROM TRIPS; DELETE FROM BUSES;"
