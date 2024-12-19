# Bismillah Selesai

## Overview
Bismillah Selesai is a backend application built with Django and Django REST Framework. It provides APIs for user authentication, face shape prediction, hairstyle and accessory recommendations, and user profile management.

## Features
- User registration and authentication
- Face shape prediction using a pre-trained model
- Hairstyle and accessory recommendations based on face shape and gender
- User profile management
- Password reset and change functionality
- Logging and error handling
- Rate limiting for API endpoints

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- Docker (optional, for containerized deployment)

### Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/bismillah-selesai.git
    cd bismillah-selesai
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database and update the `config/settings.py` file with your database credentials.

5. Run the migrations:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

7. Start the development server:
    ```sh
    python manage.py runserver
    ```

## API Endpoints
- `POST /api/login/` - User login
- `POST /api/register/` - User registration
- `POST /api/logout/` - User logout
- `POST /api/predict/` - Predict face shape
- `GET /api/profile/` - Get user profile
- `PUT /api/profile/update/` - Update user profile
- `POST /api/password-change/` - Change password
- `POST /api/password-reset/` - Request password reset
- `POST /api/password-reset/confirm/` - Confirm password reset
- `POST /api/delete-image/` - Delete image
- `POST /api/save-record/` - Save user choices
- `POST /api/history/<int:history_id>/note/` - Update history note

## Deployment
### Using Docker
1. Build and push the Docker image:
    ```sh
    docker build -t yourusername/bismillah-selesai:latest .
    docker push yourusername/bismillah-selesai:latest
    ```

2. Deploy to your VPS using the provided GitHub Actions workflow.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
