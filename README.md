# **Parkify - Book Your Parking Spot with Ease**

Welcome to **Parkify**, your go-to solution to escape the parking mayhem and seamlessly **reserve your spot** ahead of time.

Minimal clicks. Maximum convenience.
**Park smart. Park easy. Parkify.**

---

## **1. What is Parkify?**

**Parkify** is a modern, user-friendly web application that lets you book a parking spot *before* you arrive. Whether you're heading downtown or attending a packed event, you're just a tap away from guaranteed peace of mind.

---

## **2. Development Setup**

Follow these instructions to set up the project locally.

### **2.1 Backend Setup**

The backend is built with Flask and uses UV for dependency management.

#### **Prerequisites**
*   **UV** Python Package Manager
*   **Redis**: Required for caching and Celery tasks.
*   **MailHog**: Required for Sample Mailing (Sample SMTP Server)

#### **Installation**
Navigate to the `Backend` directory and sync dependencies:

```bash
cd Backend
uv sync
```

#### **Environment Configuration**
Create a `.env` file in the `Backend` directory with the following variables:

```ini
FLASK_DEBUG = ...
FLASK_RUN_HOST = ...
FLASK_RUN_PORT = ...
CACHE_TYPE = ...

SECRET_KEY = ...

SQLALCHEMY_DATABASE_URI = ...
SQLALCHEMY_TRACK_MODIFICATIONS = ...

ADMIN_MAIL = ...
ADMIN_PASSWORD = ...
ADMIN_NAME = ...
ADMIN_PINCODE = ...
ADMIN_ADDRESS = ...

SECONDS = ...

SESSION_REFRESH_EACH_REQUEST = ...
SESSION_PERMANENT = ...

SECURITY_LOGIN_URL = ...
SECURITY_LOGOUT_URL = ...
SECURITY_REGISTERABLE = ...
SECURITY_SEND_REGISTER_EMAIL = ...
SECURITY_USERNAME_ENABLE = ...

FRONTEND_URL=...
```

#### **Running the Backend Services**

1.  **Start Redis Server**
    ```bash
    sudo service redis-server start
    ```

2.  **Start Celery Worker (with Beat)**
    ```bash
    uv run celery -A app.celery worker --loglevel=info --beat
    ```

3.  **Start Flask Application**
    ```bash
    uv run flask run
    ```

---

### **2.2 Frontend Setup**

The frontend is built with Vue.js.

#### **Prerequisites**
*   **Node.js** and **npm**

#### **Installation**
Navigate to the `Frontend` directory and install dependencies:

```bash
cd Frontend
npm install
```

#### **Environment Configuration**
Create a `.env` file in the `Frontend` directory with the following variables:

```ini
VITE_API_BASE_URL = ...
```

#### **Running the Frontend**

1.  **Start Development Server**
    ```bash
    npm run dev
    ```

2.  **Build for Production & Preview**
    ```bash
    npm run build
    npm run preview
    ```

Your Parkify app frontend will typically be available at `http://localhost:5173/` (dev build) & `http://localhost:4173/` (preview build).

---

## **3. Tech Stack**

*   **Flask** - Python web framework
*   **Vue.js** - Progressive JavaScript framework
*   **UV** - Fast dependency and environment manager
*   **Redis** - In-memory data structure store
*   **Celery** - Distributed task queue
*   **HTML, CSS, JS** - For a clean and responsive frontend

---

## **4. Park Like Royalty**

No more circling blocks.
No more awkward valet interactions.
Just you, your ride, and a perfectly timed parking spot.

**Parkify** - *because parking should be predictable.*
