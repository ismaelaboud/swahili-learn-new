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

### Content Visibility Controls
#### Overview
The Content Visibility Controls feature provides granular control over lesson accessibility in the learning management system. This feature allows administrators to:

- Set lesson visibility status
- Define start and end dates for lesson availability
- Restrict lesson access based on user roles

#### Key Features

##### Visibility Management
- `is_visible`: Boolean flag to enable/disable lesson visibility
- `visibility_start_date`: Defines when a lesson becomes accessible
- `visibility_end_date`: Defines when a lesson becomes inaccessible

##### Role-Based Access Control
- `required_roles`: Specifies which user roles can access a lesson
- Supports multiple roles per lesson
- Prevents unauthorized access based on user role

#### Accessibility Rules
Lessons are considered accessible when ALL of the following conditions are met:
1. `is_visible` is set to `True`
2. Current time is between `visibility_start_date` and `visibility_end_date`
3. User's role is in the `required_roles` list

#### Use Cases
- Scheduled course content release
- Exam preparation materials with time-limited access
- Role-specific learning paths
- Compliance training with strict access controls

#### Implementation Details
- Implemented in `LessonModule` model
- Validation in `LessonVisibilityService`
- Comprehensive test coverage in `test_lesson_visibility.py`

#### Example Scenarios
```python
# Lesson only for students, available from Jan 1 to Feb 1
lesson.is_visible = True
lesson.visibility_start_date = datetime(2024, 1, 1)
lesson.visibility_end_date = datetime(2024, 2, 1)
lesson.required_roles = ['student']
```

#### Future Enhancements
- Notification system for upcoming lesson availability
- More granular role-based permissions
- Integration with course progression tracking

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

## Deployment

[Add specific deployment instructions for your infrastructure]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python
- Use TypeScript strict mode
- Write comprehensive tests

## Roadmap

- [ ] Advanced Project-based Learning
- [ ] AI-powered Learning Recommendations
- [ ] Enhanced Community Features
- [ ] Expanded Learning Paths
