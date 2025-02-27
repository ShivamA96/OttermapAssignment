# Vendor and Shop Management API

This FastAPI application provides a complete backend for managing vendors and their shops, including geographical search functionality.

To test the api deployed use base url : http://13.233.118.48/api/v1 (health test)
docs :
-> http://13.233.118.48/docs
-> http://13.233.118.48/redoc


Source code inside app/src folder

## Getting Started

Follow these instructions to set up the project locally.

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

### Installation

1. **Clone the repository** (if you haven't already)

   ```bash
   git clone https://github.com/yourusername/OttermapAssignment.git
   cd OttermapAssignment
   ```

### Create a virtual environment

# On Windows

python -m venv venv
venv\Scripts\activate

# On macOS/Linux

python3 -m venv venv
source venv/bin/activate

#Install deps
pip install -r requirements.txt
or
pip install fastapi uvicorn sqlmodel pydantic python-jose[cryptography] passlib[bcrypt] python-multipart

# From the project root

cd app
uvicorn src.main:app --reload

The API will be available at: http://localhost:8000

Access the API documentation

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

API Endpoints
The API provides the following main endpoints:

### API's

# Authentication

POST /api/v1/auth/register - Register a new user
POST /api/v1/auth/login - Authenticate a user

# Users

GET /api/v1/users/{user_id} - Get user details
PUT /api/v1/users/ - Update current user
DELETE /api/v1/users/ - Delete current user

# Shops

POST /api/v1/shops - Create a new shop
GET /api/v1/shops/{shop_id} - Get shop details
GET /api/v1/shops - Get all shops for current vendor
PUT /api/v1/shops/{shop_id} - Update a shop
DELETE /api/v1/shops/{shop_id} - Delete a shop

# Geographic Search

POST /api/v1/search - Find shops near specified coordinates
