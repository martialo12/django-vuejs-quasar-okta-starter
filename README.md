# django-vuejs-quasar-okta-starter

This repository, authored by [martialo12](https://github.com/martialo12), is a starter kit designed for building web applications using Django, Vue.js 3, and Quasar, with Okta OAuth2 authentication. This project provides a robust setup with Django and Django Rest Framework on the backend, a modern Vue.js and Quasar framework on the frontend, and secure user management through Okta. The application is dockerized for easy development and deployment, with Nginx serving as a reverse proxy.

## Features

- **Backend**: Django 5.0.2 with Django Rest Framework 3.14.0.
- **Frontend**: Responsive UI built with Vue.js 3 and Quasar.
- **Authentication**: Secure Okta OAuth2 integration with login, logout, and callback functionality.
- **Dockerization**: Containerized setup for both development and production environments.
- **Reverse Proxy**: Nginx used to efficiently route requests from the frontend to the backend.

## Prerequisites

Before you begin, ensure you have Docker and Docker Compose installed on your system. This will handle all requirements for both frontend and backend setups.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/martialo12/django-vuejs-quasar-okta-starter.git
    cd django-vuejs-quasar-okta-starter
    ```

2. **Dockerized Setup**

    Build and run the containers with Docker Compose:

    ```bash
    docker-compose up --build
    ```

    This command builds the Docker images and starts the containers as defined in the `docker-compose.yml` file. It includes the Django server, Vue.js frontend, and Nginx reverse proxy.

## Usage

After starting the containers, the application will be accessible at:
- **Frontend**: [http://localhost](http://localhost) (served by Quasar through Nginx)
- **api docs**: [http://localhost/api/docs](http://localhost/api/docs) (served by Django)

Use the frontend application to navigate and authenticate via Okta. The Nginx server routes these requests to the appropriate backend service securely.

## Contributing

Contributions to improve the project are welcome. Please follow these steps:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
