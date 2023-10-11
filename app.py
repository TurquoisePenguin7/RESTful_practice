from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from peewee import SqliteDatabase, Model, CharField

db = SqliteDatabase('test.db')

# Setting up peewee ORM
class Tasks(Model):
    task = CharField()
    status = CharField()

    # This model uses the "people.db" database.
    # We are setting the "database" variable as a reference to the db, since Peewee will automatically infer the database table name from the name of the class.
    class Meta:
        database = db

db.create_tables([Tasks])

app = Flask(__name__)
api = Api(app)

class DataBaseOperations(Resource):
    
    def get_arguments(self):
        values = reqparse.RequestParser()
        values.add_argument("id", type=int, default="") # will implement the changes for the id later
        values.add_argument("task", type=str, default="")
        values.add_argument("status", type=str, default="")
        args = values.parse_args()
        return args
    
    def get(self):
        return {"tasks": {tasks.id: {"task": tasks.task, "status": tasks.status} for tasks in Tasks.select()}}, 200
    
    def post(self):
        args = self.get_arguments()
        task = Tasks.create(task=args['task'], status=args['status'])
        task.save()
        return {'task': args["task"], "status": args["status"]}, 201
    
    def put(self):
        args = self.get_arguments()
        task_to_update = Tasks.get(Tasks.task == args['task'])
        task_to_update.status = args['status']
        task_to_update.save()
        return { "status": "successfully updated" }, 200
    
    def delete(self):
        args = self.get_arguments()
        try:
            task_to_delete = Tasks.get(Tasks.task == args['task'])
            task_to_delete.delete_instance()
        except Tasks.DoesNotExist:
            return {"failed": "Task doesn't exist"}, 400
        return {"success": {"Removed": {"task": args['task'], "status": args['status']}}}, 200
    
class root(Resource):
    def get(self):
        return {"Error": 404, "msg": "Not found :("}, 404
    
class teapot(Resource):
    def get(self):
        return {"Error": 418, "msg": "I am a little teapot"}, 418

api.add_resource(teapot, "/teapot")
api.add_resource(root, '/')
api.add_resource(DataBaseOperations,"/dbops")

if __name__ == "__main__":
    app.run(debug=True)
