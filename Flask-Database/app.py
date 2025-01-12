from flask import Flask, request, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_session import Session
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token,jwt_required, get_jwt_identity

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['JWT_SECRET_KEY'] = 'THE_jwttttToken'

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
Session(app)
CORS(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)  # Add this line
    password = db.Column(db.String(100), nullable=False)
    messages_sent = db.relationship('Message', backref='sender', lazy=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_email = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')  # Collect username from input
    password = data.get('password')

    if not all([email, username, password]):
        return jsonify({'message': 'Email, username, and password are required'}), 400

    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({'message': 'Email or username already exists!'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):

        access_token = create_access_token(identity=user.email)
        return jsonify({'message': 'Login successful!'},access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 400

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender_email = data.get('sender_email')
    receiver_email = data.get('receiver_email')
    content = data.get('content')

    if not all([sender_email, receiver_email, content]):
        return jsonify({'message': 'Invalid input data'}), 400

    sender = User.query.filter_by(email=sender_email).first()
    if not sender:
        return jsonify({'message': 'Sender not found'}), 400

    receiver = User.query.filter_by(email=receiver_email).first()
    if not receiver:
        return jsonify({'message': 'Receiver not found'}), 400

    new_message = Message(sender_id=sender.id, receiver_email=receiver_email, content=content)
    db.session.add(new_message)
    db.session.commit()

    try:
        msg = Message(
            subject="New Message",
            recipients=[receiver_email],
            body=f"New message from {sender_email}: {content}"
        )
        mail.send(msg)
    except Exception as e:
        app.logger.error(f"Email error: {e}")
        return jsonify({'message': 'Message sent, but email notification failed'}), 200

    return jsonify({'message': 'Message sent successfully!'}), 200

@app.route('/get_messages/<email>', methods=['GET'])
def get_messages(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 400

    messages = db.session.query(Message, User.email).join(
        User, Message.sender_id == User.id
    ).filter(Message.receiver_email == email).all()

    return jsonify([
        {'sender_email': msg.email, 'content': message.content, 'timestamp': message.timestamp}
        for message, msg in messages
    ]), 200

if __name__ == '__main__':
    app.run(debug=True)
