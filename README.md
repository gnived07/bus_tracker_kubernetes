# Amrita Bus Tracker

A simple full-stack bus tracking dashboard for Amrita campus routes. The app shows bus statuses, ETAs, occupancy, alerts, and basic stats using a Flask backend and a static frontend served by Nginx.

## Features

- View a list of active buses and their routes
- See live-style status information such as On Time, Delayed, and Arriving
- Monitor ETA and capacity for each bus
- Browse dashboard stats and alerts
- Add, update, and delete bus entries through the backend API
- Containerized for local development and Kubernetes deployment

## Project Structure

- backend/: Flask API server with SQLite storage
- frontend/: Nginx-served frontend UI
- k8s/: Kubernetes manifests for deployment

## Tech Stack

- Python / Flask
- SQLite
- HTML, CSS, JavaScript
- Nginx
- Docker
- Kubernetes

## Backend API

The backend exposes these endpoints:

- GET /api/buses - List all buses
- POST /api/addbus - Add a new bus
- PUT /api/updatebus/<id> - Update a bus
- DELETE /api/deletebus/<id> - Delete a bus
- GET /api/stats - Get dashboard stats
- GET /api/alerts - Get alert messages
- GET /health - Health check

## Running Locally

### 1. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The backend will run on http://localhost:5000.

### 2. Start the frontend

Open the frontend in a browser by serving the static files, or use a simple local server:

```bash
cd frontend
python -m http.server 8000
```

Then open http://localhost:8000.

> Note: The frontend expects the backend API to be available at the configured URL. In the current setup, the Nginx container proxies /api requests to the backend service.

## Running with Docker

### Build and run the backend

```bash
cd backend
docker build -t bus-tracker-backend .
docker run -p 5000:5000 bus-tracker-backend
```

### Build and run the frontend

```bash
cd frontend
docker build -t bus-tracker-frontend .
docker run -p 80:80 -e BACKEND_API_URL=http://host.docker.internal:5000 bus-tracker-frontend
```

## Kubernetes Deployment

Apply the manifests in the k8s folder:

```bash
kubectl apply -f k8s/bus_tracker.yaml
```

This deploys:

- a backend service and deployment
- a frontend service and deployment
- a namespace named webapp
- a ConfigMap for backend URL configuration

## Notes

- The app currently uses a local SQLite database file named buses.db.
- Default sample bus data is inserted on first startup if the database is empty.
- This project is intended as a lightweight demo dashboard rather than a production-grade transit system.

## License

This project is open-source and available for educational/demo purposes.
