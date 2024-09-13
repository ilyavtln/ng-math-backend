from fastapi import APIRouter
from config.database.database import create_connection, execute_query
from config.config import DB_NAME, DB_HOST, DB_PASSWORD, DB_USER, DB_PORT

router = APIRouter(
    prefix="/api/test",
    tags=["test"],
    responses={404: {"description": "Not found"}}
)

@router.options("/items")
async def options_items():
    return {"methods": ["GET", "POST", "PUT", "DELETE"]}

@router.get("/")
async def test_bd():
    connection = create_connection(
        DB_NAME=DB_NAME,
        DB_USER=DB_USER,
        DB_PASSWORD=DB_PASSWORD,
        DB_HOST=DB_HOST,
        DB_PORT=DB_PORT
    )

    query = "SELECT * FROM test"
    answer = execute_query(connection, query)

    data = [{"id": row[0], "name": row[1], "age": row[2]} for row in answer]

    return data

@router.post("/")
async def post_into_bd(name: str, age: int):
    connection = create_connection(
        DB_NAME=DB_NAME,
        DB_USER=DB_USER,
        DB_PASSWORD=DB_PASSWORD,
        DB_HOST=DB_HOST,
        DB_PORT=DB_PORT
    )

    query = "INSERT INTO test (name, age) VALUES (%s, %s)"
    values = (name, age)
    answer = execute_query(connection, query, values)

    return answer

@router.delete("/{id}")
async def delete_from_bd(id: int):
    connection = create_connection(
        DB_NAME=DB_NAME,
        DB_USER=DB_USER,
        DB_PASSWORD=DB_PASSWORD,
        DB_HOST=DB_HOST,
        DB_PORT=DB_PORT
    )

    query = "DELETE FROM test WHERE id = %s"
    values = (id,)

    answer = execute_query(connection, query, values)

    return answer

@router.put("/{id}")
async def update_bd(id: int, name: str = "", age: int = -1):
    connection = create_connection(
        DB_NAME=DB_NAME,
        DB_USER=DB_USER,
        DB_PASSWORD=DB_PASSWORD,
        DB_HOST=DB_HOST,
        DB_PORT=DB_PORT
    )

    # Шаг 1: Получаем текущие данные по id
    query = "SELECT name, age FROM test WHERE id = %s"
    values = (id,)
    result = execute_query(connection, query, values)

    if result['status'] == "error":
        return result

    current_data = result["data"]

    if not current_data:
        return {"status": "error", "message": "Record not found"}

    # Извлекаем текущее имя и возраст из полученных данных
    current_name, current_age = current_data[0]

    # Шаг 2: Обновляем только те поля, которые были переданы
    if name == "":
        name = current_name
    if age == -1:
        age = current_age

    # Шаг 3: Обновляем запись
    query = "UPDATE test SET name = %s, age = %s WHERE id = %s"
    values = (name, age, id)
    answer = execute_query(connection, query, values)

    return answer
