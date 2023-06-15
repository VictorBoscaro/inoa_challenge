# INOA Stock Market Alert

This application is a Django web application developed to monitor stock prices and send alerts when certain conditions are met.

## Getting Started

These instructions will guide you on how to run the project on your local machine for development and testing purposes.

### Prerequisites

Before starting, make sure you have the following installed on your system:

- Python 3.11.3
- Docker and Docker Compose

You can check the version of Python and Docker you have installed with the following commands:

```sh
python --version
docker --version
docker-compose --version
```

Clone the repository:
```sh
git clone https://github.com/VictorBoscaro/inoa_challenge.git
```

Navigate to the project directory
```sh
cd inoa_challenge
```

Build and run the Docker containers
```sh
docker-compose up --build -d
```

### Application Features
1 - Stock price monitoring

2 - Database to store stock prices

3 - Email alerts - To use this functionality run: docker-compose exec -it web python manage.py send_email

### Users available
If the application is started using Docker, you will be able to access a test account:

```sh
Login: user1
Password: password
```
