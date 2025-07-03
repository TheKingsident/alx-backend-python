# Messaging App

A Django REST Framework-based messaging application that supports user registration, conversations between users, and sending messages. The app uses a custom user model and provides a RESTful API with nested routing for conversations and messages.

**🚀 Features enterprise-grade CI/CD pipeline with Jenkins and GitHub Actions, Docker containerization, automated testing, code quality checks, and security scanning.**

---

## Features

- **Custom User Model**: Uses UUID as the primary key and extends Django's `AbstractUser`.
- **Conversations**: Users can participate in conversations with multiple participants.
- **Messages**: Users can send messages to each other within conversations.
- **REST API**: Built with Django REST Framework, including filtering, searching, and ordering.
- **Nested Routing**: Supports nested routes for accessing messages within conversations.
- **Authentication**: Uses DRF's session and basic authentication.
- **Browsable API**: Includes login/logout via `/api-auth/`.
- **🔄 CI/CD Pipeline**: Automated testing, building, and deployment with Jenkins and GitHub Actions.
- **🐳 Docker Support**: Multi-platform containerization for easy deployment.
- **🛡️ Security Scanning**: Automated vulnerability scanning with Trivy.
- **📊 Code Quality**: Automated linting with flake8 and code coverage reporting.

---

## Project Structure

```
messaging_app/
├── chats/
│   ├── models.py         # User, Conversation, Message models
│   ├── serializers.py    # Serializers for API representation and validation
│   ├── views.py          # ViewSets for users, conversations, and messages
│   ├── urls.py           # Routers and nested routers for API endpoints
│   ├── tests.py          # Test cases for models, views, and API endpoints
│   └── ...
├── messaging_app/
│   ├── settings.py       # Project settings (INSTALLED_APPS, AUTH_USER_MODEL, etc.)
│   ├── test_settings.py  # Test-specific settings for CI/CD
│   ├── urls.py           # Main URL configuration, includes API and api-auth
│   └── ...
├── .github/
│   └── workflows/
│       ├── ci.yml        # GitHub Actions CI pipeline (testing, linting, coverage)
│       └── dep.yaml      # GitHub Actions CD pipeline (Docker build & deploy)
├── Dockerfile            # Jenkins-specific Docker configuration
├── Dockerfile.web        # Production web app Docker configuration
├── Jenkinsfile          # Jenkins CI/CD pipeline configuration
├── docker-compose.yml   # Multi-service Docker setup
├── requirements.txt     # Python dependencies
├── .flake8             # Code linting configuration
├── .coveragerc         # Code coverage configuration
├── pytest.ini         # Test configuration
├── manage.py
└── README.md
```

---

## 🔄 CI/CD Pipeline

This project implements a robust CI/CD pipeline using both **Jenkins** and **GitHub Actions** with clear separation of concerns:

### **GitHub Actions (Primary CI/CD)**

#### **🧪 Continuous Integration (`ci.yml`)**
- **Multi-Python Testing**: Tests against Python 3.10, 3.11, and 3.12
- **Database Integration**: Uses MySQL 8.0 for realistic testing environment
- **Code Quality Checks**:
  - Flake8 linting with critical error detection
  - Code coverage reporting with 25% minimum threshold
  - Automated test result generation
- **Artifact Collection**: Saves test results, coverage reports, and linting reports
- **Smart Caching**: Optimizes build times with dependency caching

#### **🐳 Continuous Deployment (`dep.yaml`)**
- **Docker Build & Push**: Multi-platform (AMD64/ARM64) Docker images
- **Smart Tagging**: Automatic versioning based on branches, PRs, and git tags
- **Security Scanning**: Trivy vulnerability scanning with GitHub Security integration
- **Docker Hub Integration**: Automated pushing to Docker Hub registry

### **Jenkins (Alternative CI)**
- **Local Development**: Self-hosted Jenkins for local testing
- **Docker-in-Docker**: Builds and tests Docker containers
- **Test Reporting**: JUnit test result integration
- **Credential Management**: Secure handling of Docker Hub credentials

---

## 🐳 Docker Support

### **Multi-Container Architecture**

#### **Production Deployment (`Dockerfile.web`)**
```dockerfile
# Optimized for production web serving
FROM python:3.10-slim
# Includes: Gunicorn, health checks, non-root user, multi-platform support
```

#### **Development/Jenkins (`Dockerfile`)**
```dockerfile
# Jenkins-specific with Docker CLI
FROM jenkins/jenkins:lts
# Includes: Python environment, Docker CLI, testing tools
```

### **Quick Start with Docker**
```bash
# Pull and run the latest production image
docker pull yourusername/messaging-app:latest
docker run -p 8000:8000 yourusername/messaging-app:latest

# Or use docker-compose for full stack
docker-compose up -d
```

---

## 📊 Code Quality & Testing

### **Automated Testing**
- **Unit Tests**: Model, view, and API endpoint testing
- **Integration Tests**: Database operations and user workflows
- **Coverage Reporting**: HTML and XML coverage reports
- **Multi-Python Support**: Ensures compatibility across Python versions

### **Code Quality Tools**
- **Flake8**: Python code linting with custom configuration
- **Coverage.py**: Code coverage measurement and reporting
- **pytest**: Advanced testing framework with fixtures and parametrization

### **Quality Gates**
- ✅ All tests must pass
- ✅ No critical linting errors allowed
- ✅ Minimum 25% code coverage required
- ✅ Security vulnerabilities flagged

---

## 🛡️ Security & Monitoring

### **Security Scanning**
- **Trivy Integration**: Automated vulnerability scanning of Docker images
- **GitHub Security Tab**: Centralized security issue tracking
- **Dependency Scanning**: Regular checks for vulnerable dependencies

### **Monitoring & Health Checks**
- **Container Health**: Built-in Docker health checks
- **Application Monitoring**: Ready for integration with monitoring tools
- **Log Management**: Structured logging for production environments

---

## API Endpoints

- `/api/users/` — List, create, retrieve, update, and delete users.
- `/api/conversations/` — List, create, retrieve, update, and delete conversations.
- `/api/messages/` — List, create, retrieve, update, and delete messages.
- `/api/conversations/{conversation_id}/messages/` — List and create messages within a specific conversation.
- `/api-auth/` — Login/logout for the browsable API.

---

## Setup Instructions

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies**:
    ```sh
    pip install django djangorestframework django-filter drf-nested-routers
    ```

3. **Apply migrations**:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Create a superuser** (optional, for admin access):
    ```sh
    python manage.py createsuperuser
    ```

5. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

6. **Access the API** at [http://localhost:8000/api/](http://localhost:8000/api/)  
   **Browsable login/logout** at [http://localhost:8000/api-auth/](http://localhost:8000/api-auth/)

---

## Notes

- The custom user model is defined in `chats.models.User` and set via `AUTH_USER_MODEL` in settings.
- Nested routing is implemented using `rest_framework_nested.routers.NestedDefaultRouter`.
- All endpoints require authentication by default (`IsAuthenticated`).
- You can use the Django admin panel at `/admin/` for direct model management.

---

## License

This project is for educational purposes.