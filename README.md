# Glucose Data API

This project is a **Flask-based API** for managing glucose level data from CSV files. It allows **uploading, retrieving, and filtering** glucose data efficiently using **SQLite + SQLAlchemy**.

---

## Installation

Clone the repository:
```sh
git clone https://github.com/kat-git-hub/una_tech_test.git
cd una_tech_test
```
Create and activate a virtual environment:
```sh
python -m venv venv
source venv/bin/activate
```
Install dependencies with Poetry
```sh
poetry install
```
Run database migrations:
```sh
poetry run flask db upgrade
```
Start the Flask application:
```sh
poetry run python run.py
```

Now, the API is running on:
http://127.0.0.1:5000/api/v1
