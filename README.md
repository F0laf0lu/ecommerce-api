## Ecommerce API

### Project Overview

This Api serves as the backend for an ecommerce application. It allows users create a shopping cart and create orders.

### Installation Instructions
#### Prerequisties

Before running the project locally ensure you have the folloing installed:

- Python
- Django
- Django Rest Framework
- Database System

### Installation Instructions

1. Clone the repository

    ```
    git clone https://github.com/F0laf0lu/ecommerce-api.git
    ```

2. Create a virtual environment
    ```
    python -m venv venv
    ```

3. Activate the virtual environment

    ```
    venv\Scripts\activate
    ```

4. Install project dependencies
    ```
    pip install -r requirements.txt
    ```

5. Configure the database settings in the settings.py file according to    your chosen database system.

6. Apply migrations to create database schema
    ``` 
     python manage.py migrate
    ```

7. Create a superuser for administrative access:

        ```
        python manage.py createsuperuser
        ```

8. Start the development server: 
    ```
    python manage.py runserver
    ```


The Api should be running locally at [http://localhost:8000/](http://localhost:8000/.)