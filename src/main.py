import psycopg2
from fastapi import FastAPI
from src.utils.database import create_connection, execute_query
from src.config import DB_NAME, DB_HOST, DB_PASSWORD, DB_USER, DB_PORT
app = FastAPI(
    title="Math backend",
    version="1.0.1",
)

@app.get("/")
def main():
    return {"message": "Hello world"}

@app.get("/test")
def test_bd():
    connection = create_connection(
        DB_NAME = DB_NAME,
        DB_USER = DB_USER,
        DB_PASSWORD = DB_PASSWORD,
        DB_HOST=DB_HOST,
        DB_PORT = DB_PORT
    )

    query = "SELECT * FROM test"
    answer = execute_query(connection, query)

    data = [{"id": row[0], "name": row[1], "age": row[2]} for row in answer]

    return data