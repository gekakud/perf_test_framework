from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import random
import string

app = FastAPI()

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host="postgres-service", # host="localhost",  # Change to "db", "host.docker.internal", or the container's IP address
        port="5432", # default port
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

# Models
class DataItem(BaseModel):
    id: int
    name: str

# API Endpoints
@app.post("/populate/")
def populate_data(data: DataItem):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO data (id, name) VALUES (%s, %s)", (data.id, data.name))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Data inserted successfully"}

@app.post("/populate_random_100/")
def populate_random():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Insert 100 random rows
    for _ in range(100):
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
        cur.execute("INSERT INTO data (name) VALUES (%s)", (random_name,))
    
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "100 random rows added successfully"}

@app.post("/populate_random_1000/")
def populate_random():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Insert 100 random rows
    for _ in range(1000):
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
        cur.execute("INSERT INTO data (name) VALUES (%s)", (random_name,))
    
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "1000 random rows added successfully"}

@app.get("/fetch/")
def fetch_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM data")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data": rows}

@app.delete("/clear/")
def clear_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM data")
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Data cleared successfully"}

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with PostgreSQL"}

# Initialize the database on startup
@app.on_event("startup")
def on_startup():
    initialize_database()
