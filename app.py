from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError, EmailStr, constr, Field
import psycopg2

app = Flask(__name__)

# Database connection
DB_NAME = 'user_db'
DB_USER = 'postgres'
DB_PASSWORD = 'Test@123'
DB_HOST = 'localhost'
DB_PORT = '5432'
conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
cursor = conn.cursor()

class User(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    age: int = Field(..., ge=18, le=100)

@app.route("/signup", methods=["POST"])
def signup():
    try:
        user_data = request.json
        user = User(**user_data)

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    
    try:
        last_name = ''
        first_name, last_name = user_data["name"].split(' ', maxsplit=1)
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email, age) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, user.email, user.age)
        )

        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"message": "User data have inserted successfully"}), 201


@app.route("/users", methods=["GET"])
def get_users():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    name_filter = request.args.get("name")
    min_age = request.args.get("min_age", default=18, type=int)
    max_age = request.args.get("max_age", default=100, type=int)
    
    query = "SELECT * FROM users WHERE age BETWEEN %s AND %s"
    params = (min_age, max_age)
    
    if name_filter:
        query += " AND (first_name ILIKE %s OR last_name ILIKE %s)"
        params += ('%' + name_filter + '%', '%' + name_filter + '%')
    
    query += " ORDER BY id LIMIT %s OFFSET %s"
    params += (per_page, (page - 1) * per_page)
    
    cursor.execute(query, params)
    users = cursor.fetchall()

    user_list = []
    for user in users:
        user_dict = {
            "id": user[0],
            "first_name": user[1],
            "last_name": user[2],
            "email": user[3],
            "age": user[4]
        }
        user_list.append(user_dict)

    return jsonify(user_list)


if __name__ == "__main__":
    app.run(debug=True)
