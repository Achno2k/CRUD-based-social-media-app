# FastSocial

## Live vercel link

https://fastapicrudbasedapp-rq8dh3obq-aman-singhs-projects-0dbfab15.vercel.app/docs

# Description
FastSocial is a social media type application built using FastAPI and PostgreSQL, with Alembic migrations for database schema management. The application provides CRUD functionalities, allowing users to create, retrieve, update, and delete posts. Authentication is implemented using JWT tokens, and the data is managed through SQLAlchemy ORM.

# Features
**User Authentication:** Utilizes JWT tokens for secure user authentication.

**CRUD Operations:** Allows users to perform Create, Read, Update, and Delete operations on posts.

**Database Management:** Utilizes PostgreSQL as the database backend, with Alembic migrations for seamless schema updates.

**ORM Integration:** Leverages SQLAlchemy ORM for efficient and expressive database interactions.

# Installation
**1. Clone the repository:**

    git clone https://github.com/Achno2k/CRUD-based-social-media-app.git

**2. Navigate to the project directory:**

    cd CRUD-based-social-media-app.git

**3. Install dependencies:**
    
    pip install -r requirements.txt

# Configuration
1. Create a PostgreSQL database and update the database connection string in the database.py file.

    ``SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/dbname"``

2. Generate a secret key for JWT token in oauth2.py.

``SECRET_KEY = "your-secret-key"``

3. Make sure to change all the enviornmental variables in the .env file

# Database Migrations

Apply database migrations using Alembic

``alembic upgrade head``

# Run the Application
Start the FastAPI development server

``uvicorn app.main:app --reload``

The application will be accessible at ``http://127.0.0.1:8000``

# API Endpoints

Do visit the fastAPI swaggerUI at https://fastapicrudbasedapp-rq8dh3obq-aman-singhs-projects-0dbfab15.vercel.app/docs to get all the documentation related to all the endpoints and features.


## 🛠 Technologies Used
  Python, FastAPI, PostgreSQL, Sqlalchemy, Alembic.

## Contributing

Contributions are always welcome!

## License

[MIT](https://choosealicense.com/licenses/mit/)




