# IoT Stream Management Backend (FastAPI)

## Overview
This is the backend for an **IoT Stream Management and Alert System** built with **FastAPI**. The backend provides authentication, device management, real-time data processing, alerting, and filtering functionalities.

## Features
- **User Authentication** (Registration, Login, Admin Access)
- **Device Management** (Adding, Updating, and Removing IoT Devices)
- **Real-Time Data Processing** (Streaming and Storing Sensor Data)
- **Alerts & Notifications** (Trigger alerts based on threshold values)
- **Data Filtering** (Retrieve device data with filtering options)
- **Admin Management** (Manage Users & System Settings)

## Technologies Used
- **FastAPI** - High-performance web framework for APIs
- **MySQL** - Database for storing IoT data
- **SQLAlchemy** - ORM for database interactions
- **HTTPBasic Authentication** - Secure user authentication
- **JWT Tokens** - Secure API access control

## Setup Instructions
### Prerequisites
- Python 3.8+
- MySQL Database
- Virtual Environment (Recommended)

### Installation Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/iot-backend.git
   cd iot-backend
   ```
2. **Create a Virtual Environment & Activate**
   ```bash
   python -m venv my_venv
   source my_venv/bin/activate  # Mac/Linux
   my_venv\Scripts\activate  # Windows
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables** (Modify `.env` file)
   ```env
   DATABASE_URL=mysql+mysqlconnector://user:password@localhost/iot_db
   SECRET_KEY=your_secret_key
   ```
5. **Run Database Migrations**
   ```bash
   alembic upgrade head
   ```
6. **Start the FastAPI Server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
7. **Access API Documentation**
   - Open your browser and visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoints

### **1. Authentication API**
| Method | Endpoint | Description |
|--------|-------------|----------------------|
| `POST` | `/register` | Register a new user |
| `POST` | `/login` | Authenticate user and get JWT token |
| `POST` | `/forgot-password` | Send password reset email |

---

### **2. Dashboard API**
| Method | Endpoint | Description |
|--------|-------------|------------------------------|
| `GET` | `/dashboard` | Get summary of IoT data |
| `GET` | `/dashboard/{device_id}` | Get details of a specific device |

---

### **3. System Management API**
| Method | Endpoint | Description |
|--------|-------------|------------------------------|
| `POST` | `/systems` | Add a new system |
| `GET` | `/systems` | Get all systems |
| `PUT` | `/systems/{id}` | Update system details |
| `DELETE` | `/systems/{id}` | Delete a system |

---

### **4. Device Input Management API**
| Method | Endpoint | Description |
|--------|-------------|------------------------------|
| `POST` | `/device-inputs` | Add device input settings |
| `GET` | `/device-inputs` | Get all device input settings |
| `PUT` | `/device-inputs/{id}` | Update device input settings |
| `DELETE` | `/device-inputs/{id}` | Remove device input settings |

---

### **5. Data Filtering API**
| Method | Endpoint | Description |
|--------|-------------|--------------------------------------|
| `GET` | `/filters` | Retrieve filtered device data |
| `GET` | `/filters/{device_id}` | Get data of a specific device |

---

### **6. Admin API**
| Method | Endpoint | Description |
|--------|-------------|------------------------------|
| `GET` | `/admin/users` | Get all users (Admin only) |
| `DELETE` | `/admin/users/{id}` | Remove a user (Admin only) |
| `PUT` | `/admin/users/{id}` | Update user details (Admin only) |

🔐 **Admin Access Required** → Send `Bearer Token` in headers.

---

### **7. User Profile API**
| Method | Endpoint | Description |
|--------|-------------|------------------------------|
| `GET` | `/profile` | Get current user profile |
| `PUT` | `/profile` | Update user profile |

---

### **8. Alerts & Notifications API**
| Method | Endpoint | Description |
|--------|-------------|------------------------------|
| `POST` | `/alerts` | Create an alert rule |
| `GET` | `/alerts` | Get all alerts |
| `DELETE` | `/alerts/{id}` | Remove an alert rule |

---

## Testing the API
### **Using cURL**
```bash
# Register a new user
curl -X 'POST' \
  'http://127.0.0.1:8000/register' \
  -H 'Content-Type: application/json' \
  -d '{"username": "admin", "password": "password123"}'
```
```bash
# Login and get token
curl -X 'POST' \
  'http://127.0.0.1:8000/login' \
  -H 'Content-Type: application/json' \
  -d '{"username": "admin", "password": "password123"}'
```
```bash
# Get all users (Admin Only)
curl -X 'GET' \
  'http://127.0.0.1:8000/admin/users' \
  -H 'Authorization: Bearer your_jwt_token_here'
```

### **Using Postman**
1. **Login** → Send `POST /login` with username & password.
2. **Copy Token** from response.
3. **Send Requests** → Add `Authorization: Bearer <your_token>` header in Postman.

---

## Contribution Guidelines
1. **Fork the Repository**
2. **Create a New Branch** (`feature-branch`)
3. **Commit Your Changes**
4. **Push the Changes**
5. **Create a Pull Request**

---

## Contact
For queries, feel free to open an issue or reach out via WhatsApp [03467464610].
