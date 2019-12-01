CREATE TABLE public.buses (
	bus_code varchar NULL,
	color varchar NULL,
	"timestamp" timestamp NULL,
	CONSTRAINT buses_un UNIQUE (bus_code)
);

CREATE TABLE public.trips (
	trip_id varchar NULL,
	bus_code varchar NULL,
	koridor varchar NULL,
	"timestamp" timestamp NULL,
	CONSTRAINT trips_unique UNIQUE (trip_id),
	CONSTRAINT trips_buses_fk FOREIGN KEY (bus_code) REFERENCES public.buses(bus_code)
);
