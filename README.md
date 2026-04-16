# 🚀 InferStack — ML Serving Platform

A production-style machine learning serving platform that enables users to deploy models, run asynchronous predictions, and track results in real time.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
---
## 🧠 Overview

InferStack simulates a real-world ML deployment system using a microservices-style architecture. It supports model registration, background inference processing, and live result tracking through an interactive UI.

Unlike traditional ML projects, InferStack focuses on **deployment, scalability, and system design** rather than just model training.

---

## ⚙️ Tech Stack

* **Backend:** FastAPI
* **Frontend:** Streamlit
* **Message Queue (Optional):** Kafka
* **Database:** MySQL
* **Containerization:** Docker & Docker Compose
* **ML Framework:** Scikit-learn

---

## 🏗️ Architecture

```text
Client → FastAPI → (Kafka) → Worker → Model → MySQL → Frontend (Polling)
```

### Flow:

1. User submits prediction request
2. FastAPI creates a job and stores it
3. Job is processed asynchronously (Kafka or direct worker)
4. Worker loads model and generates prediction
5. Result is stored in database
6. Frontend polls and displays result

---

## ✨ Features

* 📦 Model registration and versioning
* ⚡ Asynchronous inference pipeline
* 🔄 Background worker for prediction processing
* 📊 Real-time prediction tracking (polling)
* 🗂️ Past predictions history
* 🩺 System health monitoring (DB, Kafka)
* 🐳 Fully containerized with Docker

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/daredevil-sk/InferStack.git
cd InferStack
```

---

### 2. Run the application

```bash
docker compose up --build
```

---

### 3. Access the services

* 🌐 Frontend: http://localhost:8501
* 📘 API Docs: http://localhost:8000/docs

---

## 📊 Example Usage

### Input Features

```text
5.1,3.5,1.4,0.2
```

### Workflow

1. Select model and version
2. Enter feature values
3. Submit prediction request
4. View result in real-time or in Past Predictions

---

## 📸 Screenshots


* Predict Interface
* Model Upload
* Past Predictions
* System Health Dashboard



---

## 🧪 API Endpoints

* `POST /inference/predict` → Submit prediction job
* `GET /results/{job_id}` → Fetch prediction result
* `GET /models/list` → List available models
* `GET /health/db` → Database health
* `GET /health/kafka` → Kafka health

---

## 📌 Future Improvements

* 🔐 User authentication & multi-user support
* ⚡ WebSocket-based real-time updates
* ☁️ Cloud storage for models (S3/GCS)
* 📈 Advanced monitoring & logging
* 🤖 Support for multiple ML frameworks

---

## 🧠 Key Learnings

* Designing asynchronous systems using queues
* Building scalable ML inference pipelines
* Managing containerized microservices
* Handling real-time frontend-backend communication

---

## 👨‍💻 Author

Sanjay Kanna S D

---

## ⭐ Acknowledgment

This project was built to simulate real-world ML deployment systems and demonstrate production-level thinking in machine learning engineering.
