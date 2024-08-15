# library-API
The goal of this project is to develop a comprehensive online management system for a library using Django REST Framework (DRF). The system will provide APIs to manage various library operations, including managing books, authors, borrowing activities, and more. The API is designed to be used by front-end applications or other systems to interact with the library's resources.

Features
Book Management: Create, read, update, and delete information about books, including title, author, cover type, inventory, and daily fee.
Borrowing System: Manage borrowing and returning of books with validations on availability and user eligibility.
Search and Filtering: Implement search and filtering functionality for books and authors to provide easy access to specific resources.
Project Structure
The project is organized as follows:

Authentication:
    To use the API, you need to create a user account and obtain an JWT token:
    api/user/register/
    api/user/ token/verify/
    api/user/ token/refresh/

Features:
    ·JWT authenticated
    ·Customized admin panel /admin/
    ·Payments Service: Handle payments for book borrowings through Stripe.
    ·Notifications Service: Send notifications about borrowings and overdue items via Telegram.

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

Run the development server:
    python manage.py runserver

Run with Docker:
    docker-compose build
    docker-compose up


Use accounts for test api library service:
    Admin Users:
        Email: admin@mail.com
        Password: 123
        Email: user@mail.com
        Password: 123
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
