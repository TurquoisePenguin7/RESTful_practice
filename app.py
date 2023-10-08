from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()
try:
    cur.execute("CREATE TABLE tasks(task, status)")
except sqlite3.OperationalError:
    print("Table exists, skipping...")

app = Flask(__name__)
api = Api(app)

class addInfoToDB(Resource):
    def get(self):
        res = cur.execute("SELECT * FROM tasks")
        return res.fetchall()
    
    def put(self, todo, status):
        cur.execute("INSERT INTO tasks VALUES(?, ?)", todo, status)
        return {"status": "success"}
    
class Todo3(Resource):
    def get(self):
        return {"Error": 404, "msg": "Not found :("}, 404
    
class teapot(Resource):
    def get(self):
        return {"Error": 418, "msg": "I am a little teapot"}, 418

api.add_resource(Todo3, '/')
api.add_resource(teapot, "/teapot")

if __name__ == "__main__":
    app.run(debug=True)