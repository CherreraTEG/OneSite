# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OneSite is a full-stack web application built with Angular 20 (frontend) and FastAPI (backend) for truck fleet management and company operations. The system integrates with Active Directory for authentication and uses multiple SQL Server databases for different business domains.

## Development Commands

### Backend (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload

# Run tests
pytest

# Create/activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Frontend (Angular)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
ng serve

# Build for production
ng build

# Run tests
ng test

# Watch build
ng build --watch --configuration development
```

### Docker Development
```bash
# Run entire stack
docker-compose up

# Build and run
docker-compose up --build

# Run specific service
docker-compose up backend
docker-compose up frontend
```

## Architecture Overview

### Multi-Database Backend Architecture
The FastAPI backend (`/backend/app/`) uses a sophisticated multi-database architecture:

- **Main Database (OneSite)**: User management, permissions, roles
- **SATURNO13 (TheEliteGroup_Parameters)**: Company data and business parameters
- **JUPITER12MIA (EFLOWER_Reports)**: Truck operations and logistics

Key backend patterns:
- **Repository Pattern**: CRUD classes in `/crud/` for data access abstraction
- **Dependency Injection**: FastAPI's built-in DI for database sessions and auth
- **Service Layer**: Business logic separated from API endpoints
- **Multi-database session management**: `DatabaseManager` handles multiple DB connections

### Frontend Architecture
The Angular frontend (`/frontend/src/app/`) follows modern Angular patterns:

- **Standalone Components**: Mixed with traditional modules for flexibility
- **Feature-based structure**: `auth/`, `dashboard/`, `trucks/` modules
- **Reactive state management**: BehaviorSubject-based services
- **Internationalization**: ngx-translate with JSON files for ES/EN/FR

### Authentication & Security
- **LDAP/Active Directory integration**: SSL/TLS with fallback options
- **JWT token management**: Access tokens with Redis-based blacklisting
- **Role-Based Access Control**: Granular permissions system
- **Rate limiting**: Redis-based request throttling
- **Security headers**: CSP, HSTS, X-Frame-Options

## Key Configuration Files

### Backend Configuration
- `/backend/app/core/config.py`: Multi-environment configuration with Pydantic
- `/backend/.env`: Environment variables (not tracked in git)
- `/backend/requirements.txt`: Python dependencies
- `/backend/app/main.py`: FastAPI application entry point

### Frontend Configuration
- `/frontend/src/app/app.config.ts`: Angular application configuration
- `/frontend/src/environments/`: Environment-specific settings
- `/frontend/package.json`: Node.js dependencies and scripts
- `/frontend/angular.json`: Angular CLI configuration

## Database Schema Patterns

### Models Location
- `/backend/app/models/`: SQLAlchemy ORM models
- Schema-specific table definitions with `__table_args__`
- Foreign key relationships across databases

### Key Models
- `User`: Main user table with AD integration
- `Company`: Business unit definitions in SATURNO13
- `Truck`: Logistics operations in JUPITER12MIA
- `UserCompanyPermission`: Many-to-many permission mapping

## Development Patterns

### Backend Development
- Use CRUD classes for data operations, not direct SQLAlchemy queries
- Follow dependency injection pattern for database sessions
- Implement proper error handling with HTTPException
- Use Pydantic schemas for request/response validation
- Test database connections with `/health` endpoint

### Frontend Development
- Use standalone components for new features
- Implement reactive forms with proper validation
- Follow the existing service pattern for HTTP calls
- Use the shared component library for UI consistency
- Implement proper loading states and error handling

### Environment Setup
- Copy `/backend/env.example` to `/backend/.env` and configure
- Configure Redis for rate limiting and session management
- Set up SQL Server connections for all three databases
- Configure LDAP/AD connection details

## Testing

### Backend Testing
- Use pytest for backend tests
- Test files in `/backend/tests/`
- Connection testing utilities in `/backend/app/db/`

### Frontend Testing
- Use Jasmine/Karma for Angular tests
- Test files follow `*.spec.ts` pattern
- Component and service testing patterns established

## Security Considerations

- Never commit `.env` files or sensitive configuration
- Use environment variables for all secrets and connection strings
- Implement proper CORS configuration for production
- Follow the established pattern for token management
- Use the security monitoring service for suspicious activity

## Internationalization

- Translation files in `/frontend/src/assets/i18n/`
- Use translation keys consistently: `FEATURE.SECTION.KEY`
- Default language is Spanish (es)
- Supported languages: Spanish, English, French

## Docker & Deployment

- `docker-compose.yml`: Multi-service development setup
- Production deployment uses AWS under `teg.1sitesoft.com`
- SSL certificates required for LDAP and production
- Redis container for session management and rate limiting

## Development Rules & Best Practices
 
### General Rules
- Always respond in spanish
 
 