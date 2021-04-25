from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# init app
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)

# models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    status = db.Column(db.Boolean)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('category', lazy=True))

    def __init__(self, name, category, status=False):
        self.name = name
        self.category = category
        self.status = status

    def __repr__(self):
        return f'{self.name}'
    
    def is_valid(self):
        if self.name is not None and self.category is not None and self.status is not None:
            return True
        return False


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f'{self.name}'
    
    def is_valid(self):
        if self.name is not None:
            return True
        return False

# schemas
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'status', 'category_id')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


# routes
@app.route('/api/tasks/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()

    if len(tasks) == 0:
        return jsonify({"message": "No Content"}), 204

    return tasks_schema.jsonify(tasks), 200


@app.route('/api/tasks/<int:id>/', methods=['GET'])
def get_task(id):

    if request.method != 'GET':
        return jsonify({"message": "Method not allowed"}), 405

    if type(id) != 'int':
        return jsonify({"message": "Error, the id must be a number"}), 400

    task = Task.query.get(id)

    if task is None:
        return jsonify({"message": "No Found"}), 404

    return task_schema.jsonify(task), 200


@app.route('/api/tasks/', methods=['POST'])
def save_task():

    if request.method != 'POST':
        return jsonify({"message": "Method not allowed"}), 405

    name = request.json['name']
    category_id = request.json['category_id']
    status = request.json['status']

    if name is None:
        return jsonify({"message": "Peticion invalida, faltan datos"}), 400
    
    if category_id is None:
        return jsonify({"message": "Peticion invalida, faltan datos"}), 400


    category = Category.query.get(category_id)


    if status is not None:
        task = Task(name=name, category=category, status=status)
    else:
        task = Task(name=name, category=category)


    if task.is_valid():
        try:
            db.session.add(task)
            db.session.commit()
        except:
            return jsonify({"message": "Duplicado"}), 500 
        
        return task_schema.jsonify(task), 201
    
    return jsonify({"message": "Error al guardar"}), 500


@app.route('/api/tasks/<int:id>/', methods=['PUT'])
def update_task(id):

    if type(id) != 'int':
        return jsonify({"message": "Error, the id must be a number"}), 400

    old_task = Task.query.get(id)

    name = request.json['name']
    status = request.json['status']
    category_id = request.json['category_id']

    category = Category.query.get(category_id)

    if name is not None:
        old_task.name = name
    if status is not None:
        old_task.status = status
    if category is not None:
        old_task.category = category

    if old_task.is_valid():
        db.session.add(old_task)
        db.session.commit()
        
        return task_schema.jsonify(old_task), 201
    
    return jsonify({"message": "Error al actualizar"}), 500


@app.route('/api/tasks/<int:id>/', methods=['DELETE'])
def delete_task(id):

    if type(id) != 'int':
        return jsonify({"message": "Error, the id must be a number"}), 400

    task = Task.query.get(id)

    if task is not None:
        
        db.session.delete(task)
        db.session.commit()

        return task_schema.jsonify(task), 200

    else:
        return jsonify({"message": "Not Found"}), 404

    return jsonify({"message": "Error al eliminar"}), 500


@app.route('/api/tasks/clean-all/', methods=['DELETE'])
def delete_all():
    tasks = Task.query.all()

    if len(tasks) == 0:
        return jsonify({"message": "No content"}), 204

    for task in tasks:
        if task is not None:
            db.session.delete(task)
            db.session.commit()
    
    return tasks_schema.jsonify(tasks)


@app.route('/api/categories/', methods=['GET'])
def get_categories():
    categories = Category.query.all()

    if len(categories) == 0:
        return jsonify({"message": "No Content"}), 204

    return categories_schema.jsonify(categories)


@app.route('/api/categories/<int:id>', methods=['GET'])
def get_category(id):

    if type(id) != 'int':
        return jsonify({"message": "Error, the id must be a number"}), 400

    category = Category.query.get(id)

    if category is None:
        return jsonify({"message": "Not Found"}), 404
    

    return category_schema.jsonify(category), 200
    
    


@app.route('/api/categories/', methods=['POST'])
def save_category():
    name = request.json['name']

    category = Category(name=name)

    if category.is_valid():
        db.session.add(category)
        db.session.commit()

        return category_schema.jsonify(category), 201
    
    return jsonify({'message': 'Error de servidor'}), 500


@app.route('/api/categories/<int:id>/', methods=['PUT'])
def update_category(id):

    if request.method != 'PUT':
        return jsonify({"message": "Method not allowed"}), 405

    if type(id) != 'int':
        return jsonify({"message": "Error, the id must be a number"}), 400
    
    category = Category.query.get(id)

    if category is None:
        return jsonify({"message": "Not Found"}), 404

    name = request.json['name']

    category.name = name

    if category.is_valid():
        db.session.add(category)
        db.session.commit()

        return category_schema.jsonify(category), 201

    return jsonify({"message": "Error de servidor"}), 500


@app.route('/api/categories/<int:id>/', methods=['DELETE'])
def delete_category(id):
    
    if request.method != 'DELETE':
        return jsonfiy({"message": "Method not allowed"}), 405
    
    if type(id) != 'int':
        return jsonify({"message": "Error, the id must be a number"}), 400
    
    category = Category.query.get(id)

    if category is None:
        return jsonify({"message": "Not Found"}), 404
    
    try:
        db.session.delete(category)
        db.session.commit()

        return category_schema.jsonify(category), 200

    except:
        return jsonify({"message": "Internal Server Error"}), 500


    


if __name__ == '__main__':
    app.run(debug=True)
