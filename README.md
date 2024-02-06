# Driver Tracker API Documentation

This documentation provides comprehensive information about the Driver Tracker API, designed for parents to track the location of their students' bus routes. The API supports three user types: parents, drivers, and admins. It utilizes Json Web Tokens (JWT) for authentication and implements role-based authorization.

**Note:** Before running the API, ensure you run the `create_table.sql` script located in the SQL folder. This script sets up the necessary tables in the MySQL database for the API to function properly.

The list of technologies used in the Driver Tracker API are:

- **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python.

- **Passlib with Argon2 Hashing:** Passlib is used for secure password hashing, and specifically, the Argon2 algorithm is employed for robust password security.

- **Json Web Tokens (JWT):** JWT is implemented for secure user authentication, ensuring the API can verify user identity and authorization.

- **MySQL Connector Library:** The API relies on the MySQL Connector library to facilitate communication between the API and the MySQL database, enabling efficient data retrieval and storage.

- **Python 3.10:** The API is developed using Python, with a specific version dependency on Python 3.10. This ensures compatibility with the latest language features and improvements.

- **Asynchronous Capabilities (async/await):** The API leverages asynchronous features provided by FastAPI, enabling concurrent processing of requests. This enhances overall responsiveness and performance, especially during high-traffic scenarios.

- **UVicorn:** UVicorn is employed as the ASGI server to run the FastAPI application, providing a reliable and efficient runtime environment.

These technologies collectively contribute to the reliability, security, and efficiency of the Driver Tracker API, ensuring a seamless experience for users and developers alike.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Authentication](#authentication)
4. [API Structure](#api-structure)
   - [Database Connection](#database-connection)
   - [JWT Functions](#jwt-functions)
   - [RBAC Functions](#rbac-functions)
   - [Dependency Injection Classes](#dependency-injection-classes)
   - [Parents API](#parents-api)
   - [Driver API](#driver-api)
   - [Admin Bus Route API](#admin-bus-route-api)
   - [Admin Bus Stand API](#admin-bus-stand-api)
   - [Admin Student API](#admin-student-api)
   - [Admin Driver API](#admin-driver-api)
5. [Error Handling](#error-handling)

## Introduction

The Driver Tracker API enables parents to monitor the location of their students' bus routes. Authentication is handled through Json Web Tokens (JWT), with role-based authorization for different user types.

## Installation

To run the API locally, ensure you have Python installed. Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

Run the API with:

```bash
uvicorn your_file_name:app --reload
```

Replace `your_file_name` with the name of the Python file containing the API code. In this case, it is **`main.py`**.

**Note:** Before running the API, run the `create_table.sql` script from the SQL folder to set up the required database tables.

## Authentication

The API utilizes Json Web Tokens (JWT) for authentication. Users need to include the JWT token in the `Authorization` header with the format `Bearer <token>` for accessing protected endpoints.

## API Structure

### Database Connection

The API connects to a MySQL database to retrieve and store information. The database connection details are specified in the `get_db` function.

### JWT Functions

The API includes functions for creating and decoding JWT tokens. These functions are used for user authentication.

### RBAC Functions

The API defines functions (`verify_student`, `verify_driver`, `verify_admin`) for role-based access control (RBAC). These functions ensure that only authorized users can access specific endpoints.

### Dependency Injection Classes

The API uses classes (`StudentId`, `DriverId`) to pass data from functions to controllers. These classes are annotated with dependencies for user verification.

### Parents API

The API includes endpoints for parent-related operations, such as student login and retrieving bus route information.

### Driver API

The API provides endpoints for driver-related functionalities, including driver login, updating bus route location, and updating the next stop.

### Admin Bus Route API

Endpoints are available for CRUD operations related to bus routes, including getting all bus routes, getting students for a specific bus route, and updating bus route information.

### Admin Bus Stand API

The API includes CRUD operations for bus stands, such as getting bus stands for a route, creating a new bus stand, updating bus stand information, and deleting a bus stand.

### Admin Student API

Endpoints for managing students, including getting all students, getting a student by ID, adding a new student, updating student information, and removing a student.

### Admin Driver API

Endpoints for managing drivers, including getting all drivers, getting a driver by ID, adding a new driver, updating driver information, and removing a driver.

## Error Handling

The Driver Tracker API employs robust error handling with detailed responses, using HTTP status codes to indicate specific issues. Whether it's an authentication error, unauthorized access attempt, or internal server problem, the API provides clear messages for effective debugging. This ensures a reliable and user-friendly experience, allowing developers and users to quickly identify and address any encountered issues. Refer to the API documentation for comprehensive guidance on potential error scenarios and resolution actions.
