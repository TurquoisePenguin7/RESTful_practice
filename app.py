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

class ArgumentHandler():
    """A helper class to handle the arguments, shortening the code substantially."""
    @staticmethod
    def get_arguments():
        values = reqparse.RequestParser()
        values.add_argument("id", type=int, default="") # will implement the changes for the id later
        values.add_argument("task", type=str, default="")
        values.add_argument("status", type=str, default="")
        args = values.parse_args()
        return args

class TaskListAPI(Resource):
    """Basic API entry, provides with GET and POST requests on sending and retrieving the entries."""
    
    def get(self):
        return {"tasks": {tasks.id: {"task": tasks.task, "status": tasks.status} for tasks in Tasks.select()}}, 200
    
    def post(self):
        args = ArgumentHandler.get_arguments()
        task = Tasks.create(task=args['task'], status=args['status'])
        task.save()
        return {'task': args["task"], "status": args["status"]}, 201

class TaskAPI(Resource):
    """Part of the API that works with each entry individually, supports GET, PUT, DELETE on each entry."""
    
    def get(self, taskID):
        """A class method to retrieve the specified entry"""
        try:
            task_id = Tasks.get(Tasks.id == taskID)
            return {"id": task_id.id, "task": task_id.task, "status": task_id.status}, 200
        except Tasks.DoesNotExist:
            return {"failed": "Task doesn't exist"}, 400
    
    def put(self, taskID):
        """A class method to update the specified entry"""
        args = ArgumentHandler.get_arguments()
        try:
            task_to_update = Tasks.get(Tasks.id == taskID)
            task_to_update.status = args['status']
            task_to_update.save()
            return { "status": "successfully updated" }, 200
        except Tasks.DoesNotExist:
            return {"failed": "Task doesn't exist, double-check your id number"}, 400

    def delete(self, taskID):
        """A class method to remove the specified entry"""
        args = ArgumentHandler.get_arguments()
        try:
            task_to_delete = Tasks.get(Tasks.id == taskID)
            task_to_delete.delete_instance()
        except Tasks.DoesNotExist:
            return {"failed": "Task doesn't exist"}, 400
        return {"success": {"Removed": {"task": args['task'], "status": args['status']}}}, 200


api.add_resource(TaskListAPI,"/api/tasks", "/api/tasks/")
api.add_resource(TaskAPI,"/api/tasks/<int:taskID>")

if __name__ == "__main__":
    app.run(debug=True)
