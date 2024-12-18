# Swahili Learn LMS Backend

## Project Overview
Swahili Learn is a Learning Management System (LMS) designed to facilitate Swahili language learning.

## Prerequisites
- Python 3.9+
- PostgreSQL
- pip
- virtualenv (recommended)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/swahili-learn.git
cd swahili-learn/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development dependencies
```

### 4. Database Setup
1. Create a PostgreSQL database
2. Copy `.env.example` to `.env`
3. Update `.env` with your database credentials

### 5. Run Migrations
```bash
alembic upgrade head
```

### 6. Run Tests
```bash
pytest
```

### 7. Start the Application
```bash
uvicorn app.main:app --reload
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
[Specify your license here]

## Contact
[Your contact information]
