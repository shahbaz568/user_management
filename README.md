# Flask User Management API

This project implements a Flask-based API for managing user data. It includes a signup API for user registration with data validation using Pydantic, and stores the data in a PostgreSQL database. Additionally, it provides an API to retrieve the list of users with pagination and filtering capabilities.

## Setup Instructions

### Prerequisites

- Python 3.11
- PostgreSQL

### Installation
First, install the required libraries:

pip install Flask pydantic psycopg2 email_validator


### Database Creation

1. Create the database using the following command:

    CREATE DATABASE user_db;

2. Create the table using the following command:

    CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INT NOT NULL
);


### Run the application:
**Execute the following command in the terminal:**
    python app.py

The Flask application will run at: http://127.0.0.1:5000    

## API Usage Instructions

### Signup API

**Endpoint:** `/signup`

**Method:** `POST`

**Request Body:**

**json**
Valid json data
{
    "name": "shahbaz hussain",
    "email": "shahbazh568@gamil.com",
    "age": 25
}

Invalid json data
{
    "name": "shahbaz hussain",
    "email": "shahbazh568@gamil.com",
    "age": 110
}
Response: Age is invalid. Age should be between 18 to 100.


### User list API

**Endpoint:** `/users?page=1&per_page=5&name=shahbaz&min_age=18&max_age=100`

**Method:** `GET`

**Request Body:**


