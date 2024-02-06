CREATE TABLE IF NOT EXISTS `admin` (
    `id` varchar(128) NOT NULL UNIQUE DEFAULT (UUID()) PRIMARY KEY,
    `username` varchar(128) NOT NULL UNIQUE DEFAULT '',
    `password` varchar(255) NOT NULL DEFAULT '',
    `name` varchar(64) NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS `driver` (
    `id` varchar(40) NOT NULL UNIQUE DEFAULT (UUID()) PRIMARY KEY,
    `username` varchar(128) NOT NULL UNIQUE DEFAULT '',
    `password` varchar(255) NOT NULL DEFAULT '',
    `name` varchar(64) NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS `student` (
    `id` varchar(40) NOT NULL UNIQUE DEFAULT (UUID()) PRIMARY KEY,
    `username` varchar(128) NOT NULL UNIQUE DEFAULT '',
    `password` varchar(255) NOT NULL DEFAULT '',
    `name` varchar(64) NOT NULL DEFAULT '',
    `bus_route` varchar(40) NOT NULL DEFAULT '' REFERENCES `bus_route`(`id`)
);


CREATE TABLE IF NOT EXISTS `bus_route` (
    `id` varchar(128) NOT NULL UNIQUE DEFAULT (UUID()) PRIMARY KEY,
    `driver` varchar(40) UNIQUE REFERENCES `driver`(`id`),
    `next_stop` varchar(40) UNIQUE REFERENCES `bus_stand`(`id`),
    `location_x` float,
    `location_y` float,
    `last_location_updated` timestamp,
    `name` varchar(64) NOT NULL UNIQUE DEFAULT ''
);

CREATE TABLE IF NOT EXISTS `bus_stand` (
    `id` varchar(40) NOT NULL UNIQUE DEFAULT (UUID()) PRIMARY KEY,
    `name` varchar(64) NOT NULL UNIQUE DEFAULT '',
    `x_coordinate` float NOT NULL UNIQUE DEFAULT 0.0,
    `y_coordinate` float NOT NULL UNIQUE DEFAULT 0.0,
    `bus_route` varchar(40) NOT NULL DEFAULT '' REFERENCES `bus_route`(`id`),
    `route_order` int NOT NULL DEFAULT 1
);
