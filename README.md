# TrueNorth LoanPro Coding Challenge

## Prerequisites

Before running the application, make sure you have the following installed:

- Python
- Docker

## Getting Started
- Clone this repository:
`git clone https://github.com/LucasAfonso96/backend-truenorth.git`


## Calculator Backend

### Description
The Calculator Backend is a RESTful API that provides the necessary endpoints to perform arithmetic calculations, built with Python/Django

### Installation

1. `cd calculator_backend`

2. Create Virtual Enviroment: `python -m venv venv`

3. Activate Venv:
    - Windows `venv\Scripts\activate`
    - Linux  `source venv/bin/activate`

4. Install the dependencies: `pip install -r requirements.txt`

### OBS : Already let the migrations with everything you will need to run the project, so you can skip the step 5
5. Run the Migrations on Django: 
    - `python manage.py makemigrations`
    - `python manage.py migrate`

6. Populate the Operations on Database, run: `python manage.py populate_operations`

7. Run the project:
    `python manage.py runserver`

The server will be running at http://localhost:8000.


### Testing Backend
To run the tests, use the following command: `python manage.py test`

## Using Docker Compose

Alternatively, you can use Docker Compose to run the application in a containerized environment. Make sure Docker is installed and running on your system.

1. From the root directory, build the Docker images: `docker-compose build`

2. Start the application containers: `docker-compose up`
