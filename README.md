# Food-Pre-Ordering-Module
Smart AI-Enabled Food Stall Pre-Ordering System built using Flask and MySQL with role-based authentication, real-time order management, peak demand analytics, and student expense tracking dashboard.

# 🍽️ Smart Food Stall Pre-Ordering System

A Smart AI-Enabled Food Stall Management Module built using **Flask, MySQL, and SQLAlchemy** as part of the Campus Management System project.

This system allows students to pre-order food, reduces crowd congestion, tracks peak demand times, and provides analytics for both students and administrators.

---

## 🚀 Features

### 👨‍🎓 Student Features
- Register and login using University ID
- Pre-order food items
- Select preferred time slots
- View order history
- Track total spending
- View analytics dashboard
- See peak order time
- Real-time status updates (Pending → Preparing → Ready → Received)

### 👨‍💼 Admin Features
- Admin dashboard with analytics
- View active orders
- Track daily received orders
- Detect peak order time
- Manage and update order status
- Role-based access control

---

## 🧠 Smart Analytics Features

- 📊 Orders per day visualization (Chart.js)
- 🔥 Peak Order Time Detection using historical data
- 💰 Total student expense tracking
- 📦 Active vs Completed order tracking
- 🕒 Daily received order analytics

---

## 🏗️ Tech Stack

- Backend: Flask
- ORM: SQLAlchemy
- Database: MySQL
- Authentication: Flask-Login
- Password Hashing: Flask-Bcrypt
- Frontend: HTML + Bootstrap 5
- Charts: Chart.js
- Analytics: SQL Aggregation Functions

---
ood_ordering_module/
│
├── app.py
├── models.py
├── routes.py
├── forms.py
│
├── templates/
│ ├── home.html
│ ├── admin_dashboard.html
│ ├── manage_orders.html
│ ├── order.html
│ ├── my_orders.html
│ ├── login.html
│ └── register.html
│
├── static/
│ ├── admin.css
│ └── auth.css

---

## ⚙️ How It Works

### 🔹 Authentication Flow
- Users register with name and university ID.
- Passwords are hashed using Bcrypt.
- Role-based routing ensures:
  - Students access student dashboard.
  - Admin accesses admin dashboard.

---

### 🔹 Order Flow

1. Student selects:
   - Food item
   - Quantity
   - Time slot

2. System checks:
   - Food availability
   - Slot capacity

3. Order is saved with default status: `Pending`

4. Admin updates status:
   - Pending → Preparing → Ready → Received

5. Dashboard updates dynamically.

---

### 🔹 Peak Time Detection

The system calculates:
SELECT slot_id, COUNT(*)
FROM orders
GROUP BY slot_id
ORDER BY COUNT(*) DESC;


The slot with highest count is displayed as:

🔥 Peak Order Time

---

## 🧮 Database Design

### User
- id
- name
- uni_id (unique)
- password
- role (student/admin)

### FoodItem
- id
- name
- price
- available_quantity
- is_available

### TimeSlot
- id
- slot_time
- max_capacity

### Order
- id
- user_id
- food_id
- slot_id
- quantity
- total_price
- status
- order_time

---

## 🔐 Security Features

- Password hashing
- Role-based access control
- Route protection using `@login_required`
- Validation checks for capacity and inventory

---

## 📊 Admin Dashboard Metrics

- Active Orders (not received)
- Orders Received Today
- Peak Order Time

---

## 🎓 Academic Value

This module demonstrates:

- ORM-based database design
- SQL aggregation using SQLAlchemy `func`
- Role-based authorization
- Real-time order lifecycle management
- Data visualization
- Analytics integration

---

## 📌 Future Improvements

- AI-based demand prediction
- Live WebSocket notifications
- Payment integration
- Vendor-specific dashboards
- Revenue analytics
- Weekly trend forecasting

---

## 👨‍💻 Developed By

Harsh Kumar  
B.Tech CSE  
Lovely Professional University

---

## 📜 License

This project is developed for academic purposes under university guidelines.



## 🗂️ Project Structure

