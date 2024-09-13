import psycopg2


def create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT):
    connection = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )

    return connection


def execute_query(connection, query, params=None):
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)

        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()
            return {"status": "success", "data": result}
        else:
            connection.commit()
            return { "status": "success" }

    except Exception as e:
        connection.rollback()
        return {"status": "error", "message": str(e)}