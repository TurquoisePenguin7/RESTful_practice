from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from peewee import SqliteDatabase, Model, CharField

db = SqliteDatabase('test.db')

class Tasks(Model):
    task = CharField()
    status = CharField()
    
    class Meta:
        database = db

db.create_tables([Tasks])

app = Flask(__name__)
api = Api(app)

class addInfoToDB(Resource):
    def get(self):
        return {"tasks": {tasks.task: tasks.status for tasks in Tasks.select()}}, 200
    
    def post(self):
        values = reqparse.RequestParser()
        values.add_argument("task", type=str, default="")
        values.add_argument("status", type=str, default="")
        args = values.parse_args()
        task = Tasks.create(task=args['task'], status=args['status'])
        task.save()
        return {'task': args["task"], "status": args["status"]}, 201
    
class root(Resource):
    def get(self):
        return {"Error": 404, "msg": "Not found :("}, 404
    
class teapot(Resource):
    def get(self):
        return {"Error": 418, "msg": "I am a little teapot"}, 418

api.add_resource(teapot, "/teapot")
api.add_resource(root, '/')
api.add_resource(addInfoToDB,"/add")

if __name__ == "__main__":
    app.run(debug=True)