# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import stripe
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Initialize Flask app and configurations
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_impact.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key

# Initialize database and marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Stripe configuration
stripe.api_key = 'your_stripe_secret_key'

# Define User and Project models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    goal_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)

# Initialize database tables
@app.before_first_request
def create_tables():
    db.create_all()

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']  # In production, hash this password
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User  registered successfully"}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username, password=password).first()  # Verify password in production
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Project creation endpoint
@app.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    current_user = get_jwt_identity()
    title = request.json['title']
    description = request.json['description']
    goal_amount = request.json['goal_amount']
    
    new_project = Project(title=title, description=description, goal_amount=goal_amount)
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify({"message": "Project created successfully", "project": {"id": new_project.id, "title": new_project.title}}), 201

# Get all projects endpoint
@app.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{"id": project.id, "title": project.title, "current_amount": project.current_amount} for project in projects]), 200

# Donation processing endpoint
@app.route('/donate/<int:project_id>', methods=['POST'])
@jwt_required()
def donate(project_id):
    amount = request.json['amount']
    project = Project.query.get_or_404(project_id)
    
    # Process payment with Stripe
    try:
        stripe.Charge.create(
            amount=int(amount * 100),  # Amount in cents
            currency='usd',
            source=request.json['source'],
            description=f'Donation to {project.title}'
        )
        project.current_amount += amount
        db.session.commit()
        return jsonify({"message": "Donation successful", "current_amount": project.current_amount}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get project details endpoint
@app.route('/projects/<int:project_id>', methods =['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "goal_amount": project.goal_amount,
        "current_amount": project.current_amount
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
