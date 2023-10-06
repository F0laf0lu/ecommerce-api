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


The Api should be running locally at [http://localhost:8000/api](http://localhost:8000/.)


### API Endpoints

#### API root
- /api/

#### Authentication endpoints
- /auth/users/: to allow users to register for an account.
- /auth/jwt/create (POST): to allow users to log in to their account.
- auth/user/me/: retrieve/update authenticated user.


#### Category
- /api/category/ : Create, list search for category
- /api/category/{id} :Retrieve, update, or delete a specific category

#### Product 
- /api/product/ : Create, list search for products
- /api/product/{id} :Retrieve, update, or delete a specific product

#### Cart
- /api/cart/ : Create, list search for carts
- /api/cart/{id} :Retrieve, update, or delete a specific cart
- /api/cart/{id}/items :Retrieve, update, or delete items in a specific cart

#### Order
- /api/order/ : Create, list search for orders
- /api/order/{id} :Retrieve, update, or delete a specific order
- /api/order/{id}/items :Retrieve, update, or delete items in a specific order


### Authentication 
Authentication is required for most endpoints in the API. To authenticate, include an access token in the Authorization header of your request. The access token can be obtained by logging in to your account or registering a new account.

### Configuration

Configuration details can be found in the project's `settings.py` file. Make sure to configure the required environment variables or configuration files as needed.

### API Documentation (if applicable)

You can access the API documentation [here](https://octopus-app-nax2o.ondigitalocean.app/) when the server is running. It provides comprehensive information on how to use the API endpoints.
