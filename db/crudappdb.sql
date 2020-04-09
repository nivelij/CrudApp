CREATE DATABASE crudappdb;

USE crudappdb;

CREATE TABLE foods (
	id VARCHAR(64),
	name VARCHAR(30),
	date_added date,
	PRIMARY KEY (id)
);

CREATE USER 'appuser' IDENTIFIED BY 'apppwd';

GRANT ALL ON *.* TO 'appuser'@'localhost' IDENTIFIED BY 'apppwd';