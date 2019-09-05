from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


## Models
class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Todo %r>' % self.description

## Serializers
class TodoSchema(ma.ModelSchema):
    class Meta:
        # Fields to expose
        fields = ["id", "description"]
        model: TodoModel

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {"self": ma.URLFor("id", id="<id>"), "collection": ma.URLFor("todos")}
    )


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


def abort_if_todo_doesnt_exist(todo_id):
    id_t = TodoModel().query.get(todo_id)
    if int(todo_id) not in id_t:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('description')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        todo = TodoModel.query.get(todo_id)
        return todo_schema.dump(todo)

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        todo_tmp = TodoModel.query.get(todo_id)
        db.session.delete(todo_tmp)
        db.session.commit()
        return '', 204

    def put(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        args = parser.parse_args()
        todo_schema.load(args, instance=TodoModel().query.get(todo_id))
        todo_tmp = TodoModel.query.get(todo_id)
        todo_tmp.description = args['description']
        db.session.commit()
        todo = TodoModel.query.get(todo_id)
        return todo, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        todos = TodoModel.query.all()
        return todos_schema.dump(todos)

    def post(self):
        args = parser.parse_args()
        todo_schema.dump({'description': args['description']})
        todo = TodoModel(description=args['description'])
        db.session.add(todo)
        db.session.commit()
        response = todo_schema.dump(todo)
        return response, 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)