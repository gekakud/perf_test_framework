from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import random
import string
import time

app = FastAPI()

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host="postgres-service",  # Replace with your DB host
        port="5432",  # Default PostgreSQL port
        database="testdb",
        user="user",
        password="password"
    )

# Initialize database
def initialize_database():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create table if not exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS data (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100)
    );
    """
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()

# Utility to measure execution time
def measure_time(operation_name, func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed_time = (time.time() - start_time) * 1000  # Convert seconds to milliseconds
    return result, {"operation": operation_name, "duration_ms": round(elapsed_time, 2)}

# Models
class DataItem(BaseModel):
    id: int
    name: str

# Sample pre-DB logic
def pre_db_logic(data):
    # Simulate some operation (e.g., input validation or transformation)
    if len(data.name) > 100:
        raise ValueError("Name is too long")
    return data.name.upper()  # Example transformation

# API Endpoints
@app.post("/populate/")
def populate_data(data: DataItem):
    metrics = []

    # Measure pre-DB logic
    def pre_logic():
        return pre_db_logic(data)

    transformed_data, pre_logic_metric = measure_time("pre_db_logic", pre_logic)
    metrics.append(pre_logic_metric)

    # Measure database query
    def db_query():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO data (id, name) VALUES (%s, %s)", (data.id, transformed_data))
        conn.commit()
        cur.close()
        conn.close()

    _, db_metric = measure_time("db_query", db_query)
    metrics.append(db_metric)

    # Return response
    return {"data": {"message": "Data inserted successfully"}, "metrics": metrics}

@app.post("/populate_random_100/")
def populate_random_100():
    metrics = []

    # Measure pre-DB logic
    def pre_logic():
        # Generate 100 random names
        random_names = [
            ''.join(random.choices(string.ascii_letters + string.digits, k=100))
            for _ in range(100)
        ]
        return random_names

    random_names, pre_logic_metric = measure_time("pre_db_logic_generate_random_100", pre_logic)
    metrics.append(pre_logic_metric)

    # Measure database query
    def db_query():
        conn = get_db_connection()
        cur = conn.cursor()
        for random_name in random_names:
            cur.execute("INSERT INTO data (name) VALUES (%s)", (random_name,))
        conn.commit()
        cur.close()
        conn.close()

    _, db_metric = measure_time("db_query_insert_random_100", db_query)
    metrics.append(db_metric)

    # Return response
    return {"data": {"message": "100 random rows added successfully"}, "metrics": metrics}

@app.post("/populate_random_1000/")
def populate_random_1000():
    metrics = []

    # Measure pre-DB logic
    def pre_logic():
        # Generate 1000 random names
        random_names = [
            ''.join(random.choices(string.ascii_letters + string.digits, k=100))
            for _ in range(1000)
        ]
        return random_names

    random_names, pre_logic_metric = measure_time("pre_db_logic_generate_random_1000", pre_logic)
    metrics.append(pre_logic_metric)

    # Measure database query
    def db_query():
        conn = get_db_connection()
        cur = conn.cursor()
        for random_name in random_names:
            cur.execute("INSERT INTO data (name) VALUES (%s)", (random_name,))
        conn.commit()
        cur.close()
        conn.close()

    _, db_metric = measure_time("db_query_insert_random_1000", db_query)
    metrics.append(db_metric)

    # Return response
    return {"data": {"message": "1000 random rows added successfully"}, "metrics": metrics}


@app.delete("/clear/")
def clear_data():
    metrics = []

    # Measure pre-DB logic
    def pre_logic():
        # Example: Simulate a check before clearing data
        return "All checks passed"

    _, pre_logic_metric = measure_time("pre_clear_logic", pre_logic)
    metrics.append(pre_logic_metric)

    # Measure database query
    def db_query():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM data")
        conn.commit()
        cur.close()
        conn.close()

    _, db_metric = measure_time("db_query", db_query)
    metrics.append(db_metric)

    # Return response
    return {"data": {"message": "Data cleared successfully"}, "metrics": metrics}

@app.get("/fetch/")
def fetch_data():
    metrics = []

    # Measure pre-DB logic
    def pre_logic():
        # Simulate logic before the DB query (e.g., preparing filters)
        return "Filter applied successfully"  # Example: Simulating a filter logic

    filter_result, pre_logic_metric = measure_time("pre_fetch_logic", pre_logic)
    metrics.append(pre_logic_metric)

    # Measure database query
    def db_query():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM data")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    rows, db_metric = measure_time("db_query_fetch", db_query)
    metrics.append(db_metric)

    # Return response
    return {"data": rows, "metrics": metrics}


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with PostgreSQL"}

# Initialize the database on startup
@app.on_event("startup")
def on_startup():
    initialize_database()