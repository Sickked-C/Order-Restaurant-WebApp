# 🍽️ Order Restaurant WebApp

This is a full-stack restaurant ordering system built using Django for the backend and React for the frontend.  
It allows customers to place orders online and restaurant admins to manage them through an interactive interface.

---

## 🚀 Features

- 🧾 User authentication and login system
- 📋 Menu display and order creation
- 🛒 Cart functionality for customers
- 📊 Admin dashboard for managing orders
- 🌐 Deployed version hosted on Railway (deployment URLs may differ from local setup)

---

## 🛠️ Tech Stack

- **Frontend:** React, Tailwind CSS, Axios
- **Backend:** Django, Django REST Framework
- **Deployment:** Railway, GitHub

---

## 📦 Installation Guide (Local Development)

### 1. Clone the repository
```bash
git clone https://github.com/Sickked-C/Order-Restaurant-WebApp.git
cd Order-Restaurant-WebApp
```

---

### 2. Backend Setup (Django)

Navigate to the backend folder and run:

```bash
cd backend
python -m venv env
env\Scripts\activate  # On Windows
pip install -r requirements.txt
```

Then start the backend server:

```bash
python manage.py runserver
```

📌 **Login credentials (for testing):**
- **Username:** `sickked`
- **Password:** `Jhin@1234`

---

### 3. Frontend Setup (React)

In a new terminal window:

```bash
cd frontend
npm install
npm start
```

---

## ⚠️ Notes

- When running **locally**, make sure to update the **API URLs** in the frontend code to point to your local backend server (e.g., `http://localhost:8000`) instead of the deployed Railway URL.
  - Typically found in files like `axios.js`, `services/api.js`, or environment configs (e.g. `.env.local`).

---

## 🌍 Deployment

The project is deployed using [Railway](https://railway.app/). Make sure the environment variables and URL endpoints match the Railway deployment setup when deploying.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

Developed by [Sickked-C](https://github.com/Sickked-C).  
This is a personal project showcasing about web development with Django and React.
