# Profile Management App

This application provides RESTful APIs for managing user profiles. Users can register, login, create, update, and delete their profiles.

## Requirements

- Python 3.x
- Flask
- Flask-PyMongo
- Flask-JWT-Extended
- MongoDB

## Installation

1. Install Python 3.x from [python.org](https://www.python.org/downloads/).
2. Install required Python packages:


3. Ensure you have MongoDB installed and running locally on port `27017`.

## Running the Application

1. Clone the repository or download the source code./git@github.com:Sibabalo97/flaskCrudApp.git
2. Navigate to the directory containing the source code.



4. The application will be running on `http://localhost:5003`.

## API Endpoints

- **POST /register**: Register a new user. Requires providing an email and password in the request body.

- **POST /login**: Login with an existing user. Requires providing a registered email and password in the request body.

- **GET /profile**: Retrieve the profile of the logged-in user. Requires a valid JWT token obtained after login.

- **GET /profiles**: Retrieve profiles of all users. No authentication required.

- **POST /profile**: Create a new profile for the logged-in user. Requires providing name, surname, and phone number in the request body. Authentication via JWT token is required.

- **PUT /profile/{profile_id}**: Update the profile of the logged-in user. Requires providing name, surname, and phone number in the request body. Authentication via JWT token is required.

- **DELETE /profile/{profile_id}**: Delete the profile of the logged-in user. Authentication via JWT token is required.

## Authorization

- JWT (JSON Web Tokens) is used for authentication. After successful login, the client receives an access token which should be included in subsequent requests in the `Authorization` header.

## Example Usage

1. Register a new user:






