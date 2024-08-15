# library-API
The goal of this project is to develop a comprehensive online management system for a library using Django REST Framework (DRF). The system will provide APIs to manage various library operations, including managing books, authors, borrowing activities, and more. The API is designed to be used by front-end applications or other systems to interact with the library's resources.


Authentication:
    To use the API, you need to create a user account and obtain an JWT token:
    api/user/register/
    api/user/ token/verify/
    api/user/ token/refresh/

Features
    ·Admin Panel: Customized management interface at /admin/.
    ·Book Management: Full CRUD operations for books, including title, author, cover type, inventory, and daily fee.
    ·Borrowing System: Manage borrowing and returning of books with validations on availability and user eligibility.
    ·Payments Service: Handle book borrowing payments via Stripe.
    ·Search and Filtering: Easily search and filter books and authors.
    ·JWT Authentication: Secure API access using JWT tokens.
    ·Notifications Service: Send alerts about borrowings and overdue items via Telegram.
    ·Swagger Docs: Interactive API documentation available at /swagger/.

Installation
Clone the repository:
    git clone https://github.com/lilarin/library-API.git
    cd library-API
    Create a virtual environment:
    python -m venv env
    source env/bin/activate
    Install dependencies:
    pip install -r requirements.txt

Apply migrations:
    python manage.py migrate

To create a superuser for accessing the Django admin panel, use the following command:
    python manage.py createsuperuser

Run the development server:
    python manage.py runserver

Run with Docker:
    docker-compose up --build

The API can be accessed via http://localhost:8000/api/.

API Endpoints
·Admin:
    ·/admin/
·Books:
    ·/api/book/
    ·/api/book/<id>/
·Users:
    ·/api/user/
    ·/api/user/me/
·Borrowings:
    ·/api/borrowing/
    ·/api/borrowing/<id>/
·Payment:
    ·/api/payment/
    ·/api/payment/<id>/

Project Team
Team Leader: Pavlo Krakovych
Developers:
    ·Vladyslav Chichkan
    ·Stanislav Sudakov
    ·Bohdan Kuzik
    ·Bohdan Zinchenko
    ·Nykyta Nykolaitsev
