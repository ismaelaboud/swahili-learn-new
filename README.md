# Swahili Learn 💻🚀

## Project Overview

Swahili Learn is a comprehensive Learning Management System (LMS) designed to help learners master web development, DevOps, and programming skills. Our platform provides an interactive, structured approach to learning cutting-edge technology skills through comprehensive courses, hands-on projects, and interactive assessments.

## Technology Stack

### Frontend
- Framework: Next.js (React)
- UI Components: Radix UI
- Styling: Tailwind CSS
- Language: TypeScript

### Backend
- Framework: FastAPI
- Language: Python (3.10+)
- ORM: SQLAlchemy (with Alembic for migrations)
- Database: PostgreSQL
- Testing: Pytest

## Key Features

### User Management
- User Registration and Authentication
- Profile Management
- Role-based Access Control
- Password Reset Functionality

### Course Management
- Course Creation and Enrollment
- Course Categorization
- Progress Tracking
- Multimedia Content Support

### Learning Content
- Structured Course Modules
- Video Tutorials
- Interactive Coding Exercises
- Project-based Learning
- Hands-on Labs
- Code Sandboxes

### Assessment and Tracking
- Coding Challenges
- Multiple Choice Quizzes
- Practical Coding Assignments
- Progress Tracking
- Skill Certification
- Performance Analytics

### User Management
- Personalized Learning Paths
- Role-based Access
- Profile and Skill Tracking
- Community Interaction
- Mentorship Connections

## Prerequisites

- Node.js (v16+)
- Python (3.10+)
- pip
- npm or yarn

## Installation

### Clone the Repository
```bash
git clone https://github.com/yourusername/swahili-learn.git
cd swahili-learn
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd ../frontend
npm install
# or
yarn install
```

## Running the Application

### Backend
```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
# or
yarn dev
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Linting
```bash
cd frontend
npm run lint
# or
yarn lint
```


## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request



## Roadmap

- [ ] Advanced Project-based Learning
- [ ] AI-powered Learning Recommendations
- [ ] Enhanced Community Features
- [ ] Expanded Learning Paths




