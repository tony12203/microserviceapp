from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from models import db, User
from flasgger import Swagger

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

swagger = Swagger(app)

@app.route('/')
def index(): 
    return render_template('index.html') 

@app.route('/users', methods=['POST'])
def add_user(): 
    """
    Add a new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
    responses:
      201:
        description: User created
        schema:
          type: object
          properties:
            id:
              type: integer
    """
    data = request.get_json() 
    new_user = User(name=data['name'], email=data['email']) 
    db.session.add(new_user) 
    db.session.commit() 
    return jsonify({"id": new_user.id}), 201 

@app.route('/users', methods=['GET']) 
def get_users(): 
    """
    Get all users
    ---
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              email:
                type: string
    """
    users = User.query.all() 
    return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users]) 

@app.route('/users/<int:user_id>', methods=['PUT']) 
def update_user(user_id): 
    """
    Update a user
    ---
    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
    responses:
      200:
        description: User updated
        schema:
          type: object
          properties:
            message:
              type: string
    """
    data = request.get_json() 
    user = User.query.get_or_404(user_id) 
    user.name = data['name'] 
    user.email = data['email'] 
    db.session.commit() 
    return jsonify({"message": "User updated"}) 

@app.route('/users/<int:user_id>', methods=['DELETE']) 
def delete_user(user_id): 
    """
    Delete a user
    ---
    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: User deleted
        schema:
          type: object
          properties:
            message:
              type: string
    """
    user = User.query.get_or_404(user_id) 
    db.session.delete(user) 
    db.session.commit() 
    return jsonify({"message": "User deleted"}) 

if __name__ == '__main__':  # Fixed 'name' to '__name__'
    with app.app_context(): 
        db.create_all()  # Create database tables 
    app.run(debug=True)
