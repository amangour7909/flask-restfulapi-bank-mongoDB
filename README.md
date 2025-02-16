# Flask RESTful API with MongoDB

## Overview

`flask-restful-api-mongodb` is a simple RESTful API for a banking application built using Flask and MongoDB. This API allows users to register, manage their accounts, transfer funds, check balances, and take or pay loans. The application uses bcrypt for password hashing to ensure user security.

## Features

- User registration
- Add funds to user accounts
- Transfer funds between users
- Check account balance and debt
- Take out loans
- Pay off loans

## API Endpoints Planning

| Resource      | URL        | Parameters                | Method | Status Code               |
|---------------|------------|---------------------------|--------|---------------------------|
| Register      | /register  | username, pw              | POST   | 200, 301, 302             |
| Add           | /add       | username, pw, amount      | POST   | 200, 301, 302, 304        |
| Transfer      | /transfer  | username, pw, amount, to  | POST   | 200, 301, 302, 303, 304   |
| Check Balance  | /balance   | username, pw              | POST   | 200, 301, 302             |
| Take Loan     | /takeLoan  | username, pw, amount      | POST   | 200, 301, 302, 304        |
| Pay Loan      | /payLoan   | username, pw, amount      | POST   | 200, 301, 302, 304        |
| Debt          | /debt      | username, pw, amount      | POST   | 200, 301, 302, 304        |

## Status Code Descriptions

- **200** - Ok
- **301** - Invalid username, user already exists
- **302** - Invalid password
- **304** - Amount must be greater than 0
```

## Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python.
- **Flask-RESTful**: An extension for Flask that adds support for quickly building REST APIs.
- **MongoDB**: A NoSQL database for storing user data.
- **bcrypt**: A password hashing library to securely store user passwords.

## Getting Started

### Prerequisites

- Python 3.x
- MongoDB installed and running on your local machine
- `pip` for installing Python packages

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/flask-restful-api-mongodb.git
   cd flask-restful-api-mongodb
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install Flask Flask-RESTful pymongo bcrypt
   ```

4. Ensure MongoDB is running on your local machine. You can start it using:

   ```bash
   mongod
   ```

### Running the Application

To run the application, execute the following command:

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### 1. Register a User

- **Endpoint**: `/register`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response**:
  - 200: User successfully registered
  - 301: User already exists or missing information

### 2. Add Funds

- **Endpoint**: `/add`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password",
    "amount": 100
  }
  ```
- **Response**:
  - 200: Amount added successfully
  - 301: Invalid username or missing information
  - 302: Invalid password
  - 304: Amount must be greater than 0
  - 305: Not enough money in the bank

### 3. Transfer Funds

- **Endpoint**: `/transfer`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password",
    "to": "recipient_username",
    "amount": 50
  }
  ```
- **Response**:
  - 200: Amount transferred successfully
  - 301: Invalid username or missing information
  - 302: Invalid password
  - 304: Amount must be greater than 0
  - 305: Not enough money in the account
  - 306: Cannot transfer to the same account

### 4. Check Balance

- **Endpoint**: `/balance`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response**:
  - 200: Balance and debt information
  - 301: Invalid username or missing information
  - 302: Invalid password

### 5. Take a Loan

- **Endpoint**: `/takeLoan`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password",
    "amount": 1000
  }
  ```
- **Response**:
  - 200: Loan taken successfully
  - 301: Invalid username or missing information
  - 302: Invalid password
  - 304: Amount must be greater than 0
  - 305: Not enough money in the bank

### 6. Pay a Loan

- **Endpoint**: `/payLoan`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password",
    "amount": 500
  }
  ```
- **Response**:
  - 200: Loan paid successfully
  - 301: Invalid username or missing information
  - 302: Invalid password
  - 304: Amount must be greater than 0
  - 305: Not enough money in the account
