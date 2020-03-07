from flask_restful import Api, Resource, reqparse, fields, marshal, abort
from flask_restful.inputs import regex, datetime_from_iso8601
from datetime import datetime
from api import app, db, auth
from api.models import User, Task
from flask import jsonify,g
from collections import OrderedDict

api = Api(app, catch_all_404s=True)

tasks_fields = {
    'content': fields.String,
    'done': fields.Boolean,
    "begin_time": fields.DateTime,
    "end_time": fields.DateTime,
    'uri': fields.Url('tasks')
}
response_list_fields = {
    "status": fields.String,
    "message": fields.String,
    "data": {}
}
parser = reqparse.RequestParser()
parser.add_argument('content', type=str,
                    help='No task content provided', location='json')
parser.add_argument('done', type=bool,
                    help='No task state provided', location='json')
parser.add_argument('begin_time', type=datetime_from_iso8601,
                    help='Use iso8601', location='json')
parser.add_argument('end_time', type=datetime_from_iso8601,
                    help='Use iso8601', location='json')


class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location="json")
        self.reqparse.add_argument('password', type=str, location="json")

    def post(self):
        args = self.reqparse.parse_args()
        if args['username'] == None or args['password'] == None:
            abort(400)
        if User.query.filter(User.username == args['username']).first():
            abort(400, message="用户名已经存在")
        u = User()
        u.username = args['username']
        u.hash_password(args["password"])
        db.session.add(u)
        db.session.commit()
        return {
            "state": 0,
            "message": "注册成功",
            "data": {"username": u.username}
        }


class TaskListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = parser.copy()
        self.reqparse.add_argument('put_done', type=bool,
                                   help="Give which done to switch", location=['json'])
        self.reqparse.add_argument('get_done', type=bool,
                                   help="Give which done to get", location=['json'])
        self.reqparse.add_argument('delete_done', type=bool,
                                   help="Give which done to delete", location=['json'])
        super(TaskListAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        user = g.user
        if args["get_done"] != None:
            task_list = user.task.filter(Task.done == args["get_done"]).order_by(Task.begin_time, Task.end_time).all()
        else:
            task_list = user.task.order_by(Task.begin_time, Task.end_time).all()
        rep = OrderedDict()
        rep["status"] = 0
        rep["message"] = "Get All Task You Want"
        rep["data"] = OrderedDict()
        for i in range(1, len(task_list)+1):
            task = task_list[i - 1]
            inf = {
                "id": task.id,
                "content": task.content,
                "begin_time": task.begin_time,
                "end_time": task.end_time,
                "done": task.done
            }
            rep["data"]["task %s" % str(i)] = inf
        return jsonify(rep)

    def post(self):
        args = self.reqparse.parse_args()
        task = Task(args)
        try:
            db.session.add(task)
            db.session.commit()
            return {
                "status": 0,
                "message": "success",
                "data": marshal(args, tasks_fields)
            }
        except:
            db.session.rollback()
            return {
                "status": 400,
                "message": "failed",
                "data": marshal(args, tasks_fields)
            }

    def delete(self):
        args = self.reqparse.parse_args()
        if args["delete_done"] != None:
            g.user.task.filter(Task.done == args["done"]).delete()
            db.session.commit()
        else:
            g.user.task.filter().delete()
            db.session.commit()
        return {
            "state": 0,
            "message": "Delete All you want"
        }

    def put(self):
        args = self.reqparse.parse_args()
        if args["put_done"] != None:
            g.user.task.filter().update({Task.done: args["put_done"]})
            db.session.commit()
        return {
            "state": 0,
            "message": "put All {}".format(str(args["put_done"]))
        }


class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("id", type=int, required=True,
                                   help="No Task id given", location='json')
        self.reqparse.add_argument("done", type=bool,
                                   help="No Task done given", location='json')
        super(TaskAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        id = args["id"]
        task = g.user.task.filter(Task.id == id).first()
        if task:
            return jsonify({
                "state": 0,
                "message": "Got it",
                "data": {
                    "id": task.id,
                    "content": task.content,
                    "begin_time": task.begin_time,
                    "end_time": task.end_time,
                    "done": task.done
                }
            })
        else:
            abort(400)

    def put(self):
        args = self.reqparse.parse_args()
        id = args["id"]
        done = args["done"]
        task = g.user.task.filter(Task.id == id).first()
        if not task:
            abort(400)
        if done != None:
            task.done = done
        else:
            task.done = not task.done
        db.session.commit()
        return jsonify({
            "state": 0,
            "message": "Put it",
            "data": {
                "id": task.id,
                "content": task.content,
                "begin_time": task.begin_time,
                "end_time": task.end_time,
                "done": task.done
            }
        })

    def delete(self):
        args = self.reqparse.parse_args()
        id = args["id"]
        t = g.user.task.filter(Task.id == id).first()
        if not t:
            abort(400)
        db.session.delete(t)
        db.session.commit()
        return jsonify({
            "state": 0,
            "messagpe": "Delete it",
            "data": {}
        })


api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/task', endpoint='task')
api.add_resource(UserAPI, '/users', endpoint='user')
