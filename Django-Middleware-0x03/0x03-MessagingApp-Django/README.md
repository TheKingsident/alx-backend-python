# Messaging App

A Django REST Framework-based messaging application that supports user registration, conversations between users, and sending messages. The app uses a custom user model and provides a RESTful API with nested routing for conversations and messages.

---

## Features

- **Custom User Model**: Uses UUID as the primary key and extends Django's `AbstractUser`.
- **Conversations**: Users can participate in conversations with multiple participants.
- **Messages**: Users can send messages to each other within conversations.
- **REST API**: Built with Django REST Framework, including filtering, searching, and ordering.
- **Nested Routing**: Supports nested routes for accessing messages within conversations.
- **Authentication**: Uses DRF's session and basic authentication.
- **Browsable API**: Includes login/logout via `/api-auth/`.

---

## Project Structure

```
messaging_app/
├── chats/
│   ├── models.py         # User, Conversation, Message models
│   ├── serializers.py    # Serializers for API representation and validation
│   ├── views.py          # ViewSets for users, conversations, and messages
│   ├── urls.py           # Routers and nested routers for API endpoints
│   └── ...
├── messaging_app/
│   ├── settings.py       # Project settings (INSTALLED_APPS, AUTH_USER_MODEL, etc.)
│   ├── urls.py           # Main URL configuration, includes API and api-auth
│   └── ...
├── manage.py
└── README.md
```

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