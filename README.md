
# PetVerse – All-in-One Smart Pet Care Solution

## Overview

PetVerse is an advanced full-stack web application designed to provide a centralized and intelligent platform for modern pet care management. The system integrates multiple pet-related services including pet adoption, veterinary appointment booking, medical record management, product purchasing, AI-powered chatbot assistance, feeding reminders, and vaccination tracking into a single platform.

The project addresses the limitations of fragmented pet care systems by combining all major pet care functionalities into one scalable and user-friendly solution.

---

# Core Features

## Pet Owner Features

* Secure Registration & Login
* Pet Profile Management
* Feeding Schedule Management
* Vaccination Tracking & Reminders
* Veterinary Appointment Booking
* Medical Record Access
* AI Chatbot Assistance
* Browse & Adopt Pets
* Product Purchase System
* Cart & Order Management
* Real-Time Notifications

## Adoption Agency Features

* Add & Manage Pet Listings
* View Adoption Applications
* Approve or Reject Requests
* Track Adoption Status
* Manage Adoption History

## Veterinary Features

* Manage Appointment Slots
* Maintain Medical Records
* Add Diagnosis & Prescriptions
* View Pet Visit History
* Manage Appointment Requests

## Supplier Features

* Add & Manage Products
* Inventory & Stock Management
* Order Processing
* Product Availability Tracking
* Manage Pet Food & Accessories

---

# AI Features

PetVerse integrates AI technologies using Google GenAI SDK and Gemini 2.5 Flash to provide intelligent pet care assistance.

### AI Capabilities

* Real-time Pet Care Guidance
* Natural Language Query Handling
* Smart Chatbot Responses
* Health & Feeding Suggestions
* Pet Care Assistance using NLP

---

# Reminder & Notification System

The platform includes an automated scheduling and notification system using APScheduler.

### Automated Features

* Feeding Reminders
* Vaccination Alerts
* Appointment Notifications
* Adoption Status Updates
* Order Status Notifications

---

# Technologies Used

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Jinja2

## Backend

* Python
* Flask Framework

## Database

* SQLite

## AI & Automation

* Google GenAI SDK
* Gemini 2.5 Flash
* Natural Language Processing (NLP)
* APScheduler
* SMTP Email Notifications

## Development Tools

* Git & GitHub
* Visual Studio Code

---

# System Architecture

PetVerse follows an Event-Driven Architecture (EDA) to support scalable and efficient processing of real-time events such as reminders, notifications, appointment updates, and chatbot interactions.

---

# Major Modules

## Pet Management Module

Allows users to create and manage pet profiles including breed, age, medical history, feeding schedules, and vaccination information.

## Adoption Management Module

Enables adoption agencies to list pets and allows users to browse and apply for pet adoption.

## Veterinary Management Module

Supports appointment booking, medical record maintenance, diagnosis management, and prescription handling.

## Product & E-Commerce Module

Allows suppliers to manage pet products while users can browse products, add items to cart, and place orders.

## AI Chatbot Module

Provides intelligent responses related to pet health, feeding, and general pet care using NLP techniques.

## Reminder Module

Generates automated feeding reminders and vaccination notifications for pet owners.

---

# Project Structure

```bash
PetVerse/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── pets.html
│   ├── adoption.html
│   ├── appointments.html
│   ├── products.html
│   ├── chatbot.html
│   └── ...
│
├── app.py
├── routes.py
├── models.py
├── database.py
├── requirements.txt
└── README.md
```

---

# Installation Guide

## Clone Repository

```bash
git clone <your-repository-link>
cd PetVerse
```

---

# Create Virtual Environment

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Project

```bash
python app.py
```

Application runs on:

```bash
http://127.0.0.1:5000/
```

---

# Database Tables

The system includes multiple database modules such as:

* User
* Pet
* Feeding Reminder
* Vaccination Reminder
* Chat Session
* Adoption Listing
* Adoption Application
* Product
* Cart & Cart Item
* Order & Order Item
* Vet Appointment Slot
* Vet Appointment
* Medical Record
* Notification

---



---

# Functional Requirements

* User Authentication & Authorization
* Pet Profile Management
* Adoption Request Tracking
* Appointment Booking
* Medical Record Management
* AI Chatbot Assistance
* Product Purchase & Cart Management
* Reminder & Notification System
* Real-Time Updates
* Multi-Role Access System

---

# Non-Functional Requirements

* Scalability
* Reliability
* Security
* Maintainability
* User-Friendly Interface
* High Performance
* Portability Across Devices

---

# Future Enhancements

* Mobile Application
* Online Payment Gateway
* GPS Pet Tracking
* AI Disease Prediction
* Voice-enabled AI Assistant
* Cloud Deployment
* Advanced Analytics Dashboard

---

# Learning Outcomes

This project helped in understanding:

* Full Stack Web Development
* Flask Framework
* AI Integration in Web Applications
* Database Design & Management
* NLP-based Chatbot Development
* Event-Driven Architecture
* Authentication & Authorization
* Reminder Automation
* CRUD Operations
* E-Commerce System Development

---

# Author

Aswan
MCA Student | Python & Full Stack Developer

---

# License

This project is developed for academic and educational purposes.

<img width="1892" height="907" alt="landing page" src="https://github.com/user-attachments/assets/435a11e6-5953-48c1-913e-91b17c9fe220" />
<img width="1920" height="1540" alt="dashboard" src="https://github.com/user-attachments/assets/733470b9-f0cc-4362-9a7d-ab7e4485effd" />
<img width="1358" height="865" alt="ai assistant" src="https://github.com/user-attachments/assets/a203eb82-1913-48fc-8d35-c754ad4022cc" />
<img width="1902" height="910" alt="adoption" src="https://github.com/user-attachments/assets/d06a4bdc-1c43-4c6c-b427-91ca6ca5634a" />
<img width="1287" height="720" alt="appointment" src="https://github.com/user-attachments/assets/c0662a9a-49ff-4533-aac5-b08c032c9bde" />
<img width="1903" height="907" alt="product" src="https://github.com/user-attachments/assets/ec7a81e8-033c-4773-b1b0-cc1b956bd6a9" />
<img width="1877" height="901" alt="petprofile" src="https://github.com/user-attachments/assets/64cf1902-8100-4a2f-b225-ea936859c071" />
<img width="1720" height="907" alt="medical records" src="https://github.com/user-attachments/assets/375e17f1-f615-4ee4-aff2-2ef8c4440b74" />
