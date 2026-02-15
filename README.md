# Gym Tracker Web App

A Flask-based web application to track workouts.

## Features
- User Registration & Login
- Add workouts (exercise, reps, weight)
- Delete workouts
- Dockerized for deployment

## Tech Stack
- Python
- Flask
- SQLAlchemy
- Flask-Login
- SQLite
- Docker

## Run with Docker
docker build -t gym-tracker .
docker run -p 5000:5000 gym-tracker
