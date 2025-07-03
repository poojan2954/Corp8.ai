from fastapi import FastAPI, Request
import sqlite3

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the SQL Query API!"}

@app.post("/query")
async def run_sql_query(request: Request):
    body = await request.json()
    query = body.get("query")

    try:
        conn = sqlite3.connect("sample.db")
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return {"result": rows}
    except Exception as e:
        return {"error": str(e)}
