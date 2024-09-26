import json
import os
import csv
from sqlite3 import IntegrityError
from flask import Flask, request
from flask_session import Session
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_caching import Cache
from celery.schedules import crontab
from sqlalchemy import CheckConstraint, or_
from jobs import workers
from flask_jwt_extended import (
    JWTManager, create_access_token, get_jwt_identity, jwt_required
)
import redis
from sqlalchemy import func
from datetime import timedelta
from datetime import datetime
from flask_mail import Mail
from flask_mail import Message


app = Flask(__name__)

CORS(app, origins='http://localhost:8080')

app.config['JWT_SECRET_KEY'] = 'ihatemad2'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

jwt = JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'db.sqlite3')

app.config['SECRET_KEY'] = "ihatemad2"
app.config["SESSION_TYPE"] = "filesystem"
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
app.config['BROKER_CONNECTION_RETRY_ON_STARTUP'] = True
app.config['REDIS_HOST'] = 'localhost'
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = 0
Session(app)
db = SQLAlchemy(app)
api = Api(app)
app.app_context().push()

# Flask app configuration for MailHog
# http://localhost:8025/
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = "admin@example.com"
mail = Mail(app)
app.app_context().push()

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

celery = workers.celery

celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_connection_retry_on_startup=app.config[
        "BROKER_CONNECTION_RETRY_ON_STARTUP"]
)
celery.conf.timezone = 'Asia/Kolkata'

celery.Task = workers.ContextTask
app.app_context().push()


@celery.task()
def daily_reminder():
    users = User.query.filter(
        or_(User.pending_book_count == 0, User.approved_book_count == 0),
        User.pseudo_delete == False,
        User.role == 0
    ).all()
    for user in users:
        subject = "Library Reminder"
        recipients = [user.email]
    with mail.connect() as conn:
        message = f"""
            <html>
                <head>
                    <title>Library Reminder</title>
                </head>
                <body>
                    <h1>Hello {user.name}!</h1>
                    <p>Here is your library reminder.</p>
                    <p>You have not borrow any books for a long time. We kindly ask you to visit our library.</p>
                    <p>Thank You.</p>
                </body>
            </html>
            """
        msg = Message(recipients=recipients, subject=subject, html=message)
        conn.send(msg)
    return "Reminder sent to all inactive users"


@celery.task()
def monthly_report():
    users = User.query.filter_by(role=0, pseudo_delete=False).all()
    with mail.connect() as conn:
        for user in users:
            subject = "Monthly Reading Report"
            recipients = [user.email]
            message = f"""
            <html>
                <head>
                    <title>Monthly Reading Report</title>
                </head>
                <body>
                    <h1>Hello {user.name}!</h1>
                    <p>Here is your monthly reading report.</p>
                    <table>
                        <thead>
                            <tr>
                                <th>Book Name</th>
                                <th>Author</th>
                                <th>Section Name</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            read_books = Register.query.filter_by(
                user_id=user.id, request_status=3, pseudo_delete=False).all()
            for book in read_books:
                message += f"""
                        <tr>
                            <td>{book.book_name}</td>
                            <td>{book.author}</td>
                            <td>{book.section_name}</td>
                        </tr>
                """
            message += """
                        </tbody>
                    </table>
                    <p>Thank You.</p>
                </body>
            </html>
            """
            msg = Message(recipients=recipients, subject=subject, html=message)
            conn.send(msg)
    return "Monthly report sent to all users"


@celery.task()
def prepare_csv_file():
    data = []
    users = User.query.filter_by(pseudo_delete=False, role=0).all()
    books = Book.query.filter_by(pseudo_delete=False).all()
    sections = Section.query.filter_by(pseudo_delete=False).all()
    registers = Register.query.filter_by(pseudo_delete=False).all()
    for user in users:
        for book in books:
            for section in sections:
                for register in registers:
                    if user.id == register.user_id and book.id == register.book_id and section.id == book.section_id:
                        data.append(register.serialize(user.id))
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    librarian_email = User.query.filter_by(role=1).first().email
    with open('data.csv', 'rb') as file:
        msg = Message("Monthly Reading Report", recipients=[librarian_email],
                      attachments=[('data.csv', file.read())])
        mail.send(msg)
    os.remove('data.csv')
    return "Monthly reading report sent to librarian"


celery.conf.beat_schedule = {
    'my_monthly_task': {
        'task': "app.monthly_report",
        'schedule': crontab(hour=22, minute=25, day_of_month=3,
                            month_of_year='*/1'),
    },
    'my_daily_task': {
        'task': "app.daily_reminder",
        'schedule': crontab(hour=22, minute=25, day_of_week=5),
    },
    'my_quick_task': {
        'task': "app.daily_reminder",
        'schedule': crontab(minute='*/1'),
    }
    # Add more scheduled tasks as neede
}


# performing RUD operations
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.Integer, default=0)
    # increment on new request, decrement on return or approve or cancel or revoke
    pending_book_count = db.Column(db.Integer, default=0)
    # increment on approve, decrement on return or revoke
    approved_book_count = db.Column(db.Integer, default=0)
    # increment on return or revoke
    returned_book_count = db.Column(db.Integer, default=0)
    created_by = db.Column(db.Integer, default=1)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    Interests = db.Column(db.String)
    last_visited = db.Column(db.DateTime(
        timezone=True), default=datetime.now())
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    pseudo_delete = db.Column(db.Boolean, default=False)

    __table_args__ = (
        CheckConstraint('role >= 0', name='check_role'),
        CheckConstraint('pending_book_count >= 0',
                        name='check_pending_book_count'),
        CheckConstraint('approved_book_count >= 0',
                        name='check_approved_book_count'),
        CheckConstraint('returned_book_count >= 0',
                        name='check_returned_book_count'),
        CheckConstraint('created_by >= 0', name='check_created_by'),
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'Interests': self.Interests,
            'pending_book_count': self.pending_book_count,
            'approved_book_count': self.approved_book_count,
            'returned_book_count': self.returned_book_count,
            'last_visited': self.last_visited.isoformat(),
            'created_on': self.created_on.isoformat(),
            'created_by': self.created_by
        }


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    view_access_link = db.Column(db.String)
    edit_access_link = db.Column(db.String)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    # increament when someone return or autorevoke or manual revoke happens
    rank = db.Column(db.Integer, default=0)
    # increament whenever a new request is created for the book
    count_of_pending_req = db.Column(db.Integer, default=0)
    author = db.Column(db.String(50), nullable=False)
    section_name = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, default=1)
    pseudo_delete = db.Column(db.Boolean, default=False)

    def serialize(self, user_id=-1):
        data = {
            'id': self.id,
            'name': self.name,
            'view_access_link': self.view_access_link,
            'edit_access_link': self.edit_access_link,
            'description': self.description,
            'date': self.date.strftime('%Y-%m-%d'),
            'price': self.price,
            'stock': self.stock,
            'author': self.author,
            'section_name': self.section_name
        }
        book_aloc = Register.query.filter_by(book_id=self.id,
                                             user_id=user_id, pseudo_delete=False).first()
        if book_aloc:
            data['request_status'] = book_aloc.request_status
        else:
            data['request_status'] = -1
        return data


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, default=1)
    pseudo_delete = db.Column(db.Boolean, default=False)


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    book_name = db.Column(db.String(100), nullable=False)
    section_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    # 0-pending, 1-approved, 2-rejected, 3-returned
    request_status = db.Column(db.Integer, nullable=False,
                               default=0)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    date_issued = db.Column(db.DateTime)
    requested_date = db.Column(db.DateTime, default=datetime.now())
    return_date = db.Column(db.DateTime)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, default=1)
    pseudo_delete = db.Column(db.Boolean, default=False)

    def serialize(self):
        data = {
            'id': self.id,
            'username': self.username,
            'book_name': self.book_name,
            'section_name': self.section_name,
            'author': self.author,
            'request_status': self.request_status,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'date_issued': self.date_issued.strftime(
                '%Y-%m-%d') if self.date_issued else None,
            'requested_date': self.requested_date.strftime(
                '%Y-%m-%d') if self.requested_date else None,
            'return_date': self.return_date.strftime(
                '%Y-%m-%d') if self.return_date else None,
            'created_on': self.created_on.strftime(
                '%Y-%m-%d') if self.created_on else None
        }
        return data


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    review = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, default=1)
    pseudo_delete = db.Column(db.Boolean, default=False)


db.create_all()


try:
    exits = User.query.filter_by(email='admin@admin.com').first()
    if exits:
        pass
    else:
        new_user = User(name='Gurneet', password='Gurneet',
                        email='admin@admin.com', role=1)
        db.session.add(new_user)
        db.session.commit()
except IntegrityError:
    pass


def update_last_visited(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.last_visited = datetime.now()
        db.session.commit()


def find_user_by_email_and_name(email, name):
    return User.query.filter_by(email=email, name=name).first()


def verify_user_role(user_id, role_name):
    user = User.query.filter_by(id=user_id).first()
    if user.role == role_name:
        return True
    return False


# Resource for the librarian dashboard


class DashboardResource(Resource):
    @jwt_required()
    def get(self):
        section_count = Section.query.filter_by(pseudo_delete=False).count()
        if verify_user_role(get_jwt_identity(), 0):
            reqested_count = Register.query.filter_by(
                user_id=get_jwt_identity(),
                pseudo_delete=False, request_status=0).count()
        else:
            reqested_count = Register.query.filter_by(
                pseudo_delete=False, request_status=0).count()

        if verify_user_role(get_jwt_identity(), 0):
            allocated_book_count = Register.query.filter_by(
                request_status=1,
                user_id=get_jwt_identity(), pseudo_delete=False).count()
        else:
            allocated_book_count = Register.query.filter_by(
                request_status=1, pseudo_delete=False).count()

        book_count = Book.query.filter_by(pseudo_delete=False).count()
        if verify_user_role(get_jwt_identity(), 0):
            top_books = Book.query.filter_by(pseudo_delete=False).order_by(
                Book.rank.desc()).limit(5)
            top_books_list = [book.serialize() for book in top_books]
        else:
            top_books = Book.query.filter_by(pseudo_delete=False).order_by(
                Book.rank.desc()).limit(5)
            top_books_list = []
            for book in top_books:
                top_books_dictionay = {
                    "id": book.id,
                    "name": book.name,
                    "author": book.author,
                    "section_name": book.section_name
                }
                top_books_list.append(top_books_dictionay)

        if verify_user_role(get_jwt_identity(), 0):
            book_by_req = Register.query.filter_by(
                pseudo_delete=False, user_id=get_jwt_identity()
            ).order_by(Register.date_issued.desc()).limit(5)
            book_by_req_list = []
            for book in book_by_req:
                book_by_req_dictionay = {
                    "id": book.id,
                    "name": book.book_name,
                    "author": book.author,
                    "section_name": book.section_name
                }
                book_by_req_list.append(book_by_req_dictionay)
        else:
            book_by_req = Book.query.filter_by(pseudo_delete=False).order_by(
                Book.count_of_pending_req.desc()).limit(5)
            book_by_req_list = []
            for book in book_by_req:
                book_by_req_dictionay = {
                    "id": book.id,
                    "name": book.name,
                    "author": book.author,
                    "section_name": book.section_name
                }
                book_by_req_list.append(book_by_req_dictionay)

        inactive_users = User.query.filter_by(
            pending_book_count=0,
            approved_book_count=0, role=0).all()

        inactive_users_list = []
        for user in inactive_users:
            inactive_users_dictionay = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "pending_book_count": user.pending_book_count,
                "approved_book_count": user.approved_book_count
            }
            inactive_users_list.append(inactive_users_dictionay)

        active_users = User.query.filter(
            or_(User.approved_book_count > 0, User.pending_book_count > 0),
            User.role == 0).all()

        active_users_list = []
        for user in active_users:
            active_users_dictionay = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "pending_book_count": user.pending_book_count,
                "approved_book_count": user.approved_book_count
            }
            active_users_list.append(active_users_dictionay)

        dashboard_data_dictionay = {
            'section_count': section_count,
            'reqested_count': reqested_count,
            'allocated_book_count': allocated_book_count,
            'book_count': book_count,
            'top_books': top_books_list,
            'book_by_req': book_by_req_list,
            'inactive_users': inactive_users_list,
            'active_users': active_users_list
        }
        return dashboard_data_dictionay, 200

# Resource to track last login


class TrackLastLoginResource(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            # Update last login for the current user
            update_last_visited(current_user_id)
            return {"msg": "Last login date updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

# Resource for user signup


class SignUpResource(Resource):
    def post(self):
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return {"error": "User with this email already exists"}, 400

        # Create new user
        new_user = User(name=name, email=email, password=password, role=0)
        db.session.add(new_user)
        db.session.commit()

        return {"msg": "User signed up successfully"}, 200


# Resource for user profile

class UserResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user.serialize(), 200
        else:
            return {"error": "User not found"}, 404

    @jwt_required()
    def put(self):
        data = request.json
        id = data.get('id')
        name = data.get('name')
        email = data.get('email')
        interests = data.get('interests')

        user = User.query.filter_by(id=id).first()
        if not user:
            return {"error": "User not found"}, 404

        user.name = name
        user.email = email
        user.Interests = interests
        db.session.commit()
        return {"msg": "User details updated successfully"}, 200

# Resource for user login


class LoginResource(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(
            email=email, password=password, role=0).first()
        if user:
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token, "msg":
                    "User logged in successfully", "userName": user.name}, 200
        else:
            return {"error": "Invalid email or password"}, 400


# Resource for librarian login


class LibrarianLoginResource(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')

        librarian_user = User.query.filter_by(
            email=email, password=password, role=1).first()

        if librarian_user:
            access_token = create_access_token(identity=librarian_user.id)
            return {"accessToken": access_token, "msg":
                    "Librarian logged in successfully",
                    "userName": librarian_user.name}, 200
        else:
            return {"error": "Invalid librarian credentials"}, 401


# Resource for adding a new genre
class NewGenreResource(Resource):
    @jwt_required()
    def get(self, section_id):
        try:
            section = Section.query.filter_by(id=section_id,
                                              pseudo_delete=False).first()
            if section:
                return {"section_id": section.id,
                        "section_name": section.name,
                        "section_created_date":
                        section.date.strftime('%Y-%m-%d'),
                        "section_descp": section.description}, 200
            else:
                return {"error": "Section not found"}, 404
        except Exception as e:
            return {"error":
                    "An error occurred while fetching the section: "
                    + str(e)}, 500

    @jwt_required()
    def post(self):
        data = request.json
        current_user_id = get_jwt_identity()
        user = verify_user_role(current_user_id, 1)

        if user:
            try:
                section_name = data.get('name')
                section_created_date = data.get('date')
                section_descp = data.get('description')

                existing_section = Section.query.filter_by(name=section_name
                                                           ).first()
                if existing_section:
                    return {"error": "Section name already exists"}, 400
                else:
                    new_section = Section(
                        name=section_name,
                        date=datetime.strptime(section_created_date,
                                               '%Y-%m-%d'),
                        description=section_descp
                    )
                    db.session.add(new_section)
                    db.session.commit()
                    return {"msg": "Section added successfully"}, 200
            except Exception as e:
                return {"error": "An error occurred while \
                                 adding the section: "
                        + str(e)}, 500
        else:
            return {"error": "Unauthorized access"}, 401

    @jwt_required()
    def put(self, section_id):
        data = request.json
        current_user_id = get_jwt_identity()
        user = verify_user_role(current_user_id, 1)

        if user:
            try:
                section_name = data.get('section_name')
                section_created_date = data.get('section_created_date')
                section_descp = data.get('section_descp')

                section = Section.query.filter_by(id=section_id).first()
                if section:
                    section.name = section_name
                    section.date = datetime.strptime(
                        section_created_date, '%Y-%m-%d')
                    section.description = section_descp
                    db.session.commit()
                    return {"msg":
                            "Section updated successfully"}, 200
                else:
                    return {"error": "Section not found"}, 404
            except Exception as e:
                return {"error": "An error occurred while updating \
                        the section: " + str(e)}, 500
        else:
            return {"error": "Unauthorized access"}, 401

    @jwt_required()
    def delete(self, section_id):
        current_user_id = get_jwt_identity()
        user = verify_user_role(current_user_id, 1)

        if user:
            try:
                section = Section.query.filter_by(id=section_id).first()
                if section:
                    section.pseudo_delete = True
                    db.session.commit()
                    return {"msg": "Section deleted successfully"}, 200
                else:
                    return {"error": "Section not found"}, 404
            except Exception as e:
                return {"error": "An error occurred \
                                 deleting the section: " + str(e)}, 500
        else:
            return {"error": "Unauthorized access"}, 401


# Resource for fetching genres
class GenreResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = verify_user_role(current_user_id, 1)

        if user:
            try:
                genres = Section.query.filter_by(pseudo_delete=False).all()
                genres_list = []
                for genre in genres:
                    genres_list.append({
                        'genre_id': genre.id,
                        'genre_name': genre.name,
                        'genre_created_date': genre.date.strftime('%Y-%m-%d'),
                        'genre_descp': genre.description
                    })
                return genres_list, 200
            except Exception as e:
                return {"error":
                        "An error occurred while fetching genres: "
                        + str(e)}, 500
        else:
            return {"error": "Unauthorized access"}, 401


# Resource for fetching list of books


class BooksListResource(Resource):
    @jwt_required()
    def get(self):
        # # Check if the result is cached in Redis
        # cached_result = redis_client.get('books_list')
        # if cached_result:
        #     return json.loads(cached_result.decode('utf-8')), 200
        # If not cached, query the database
        books = Book.query.filter_by(pseudo_delete=False).all()
        current_user_id = get_jwt_identity()
        if verify_user_role(current_user_id, 0):
            books_serialized = [book.serialize(current_user_id
                                               ) for book in books]
        else:
            books_serialized = [book.serialize() for book in books]
        # Cache the result in Redis for 5 minutes
        redis_client.setex('books_list', 300, json.dumps(books_serialized))
        return books_serialized, 200

    @jwt_required()
    def post(self):
        data = request.json
        new_book = Book(
            name=data['book_name'], author=data['book_authors'], genre_id=data['genre_id'])
        db.session.add(new_book)
        db.session.commit()
        return {"msg": "Book added successfully"}, 201

# Resource for fetching information about books allocated to a user


class UserBooksResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        allocated_books = Register.query.filter_by(
            user_id=user_id,
            pseudo_delete=False
        ).filter(
            Register.request_status.in_((1, 3))
        ).all()
        myBooks = []
        returnedBooks = []
        user = User.query.filter_by(id=user_id).first()
        for allocated_book in allocated_books:
            date_issued = allocated_book.date_issued
            if date_issued and datetime.now() - date_issued >= timedelta(days=7):
                # auto revoke is happening here
                allocated_book.request_status = 3
                allocated_book.return_date = datetime.now()
                user.approved_book_count -= 1
                user.returned_book_count += 1
                book = Book.query.filter_by(
                    id=allocated_book.book_id).first()
                book.rank += 1
                db.session.commit()
        for allocated_book in allocated_books:
            if allocated_book.request_status == 1:
                myBooks.append({
                    'book_title': allocated_book.book_name,
                    'author': allocated_book.author,
                    'section': allocated_book.section_name,
                    'id': allocated_book.id
                })
            elif allocated_book.request_status == 3:
                feedback = Feedback.query.filter_by(
                    user_id=user.id,
                    book_id=allocated_book.book_id).first()
                if feedback:
                    returnedBooks.append({
                        'book_title': allocated_book.book_name,
                        'author': allocated_book.author,
                        'section': allocated_book.section_name,
                        'id': allocated_book.id,
                        'book_id': allocated_book.book_id,
                        'rate': feedback.rate,
                        'review': feedback.review
                    })
                else:
                    returnedBooks.append({
                        'book_title': allocated_book.book_name,
                        'author': allocated_book.author,
                        'section': allocated_book.section_name,
                        'book_id': allocated_book.book_id,
                        'id': allocated_book.id
                    })
        if myBooks or returnedBooks:
            return {'myBooks': myBooks, 'returnedBooks': returnedBooks}, 200
        else:
            return {"error": "User has no books allocated"}, 404

# Resource for allocating a book to a user


class AllocateBookResource(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        book_id = data.get('id')
        if not book_id:
            return {"error": "Both book_id and user_id are required"}, 400

        book = Book.query.filter_by(id=book_id).first()
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()

        if user.pending_book_count + user.approved_book_count >= 5:
            return {"error": "Cannot request more than 5 books"}, 400

        if not book:
            return {"error": "Book not found"}, 404
        else:
            book_allocation = Register(
                book_id=book_id, user_id=user.id,
                requested_date=datetime.now(),
                username=user.name, book_name=book.name,
                author=book.author, section_name=book.section_name,
                request_status=0)
            user.pending_book_count += 1
            book.count_of_pending_req += 1
            db.session.add(book_allocation)
            db.session.commit()
            return {"msg": "Book allocated successfully"}, 200

    @jwt_required()
    def put(self):
        data = request.json

        req_id = data.get('req_id')
        if not req_id:
            return {"error": "req_id is required"}, 400

        book_allocation = Register.query.filter_by(
            pseudo_delete=False, id=req_id).first()
        if not book_allocation:
            return {"error": "Book request not found"}, 404
        else:
            book_allocation.request_status = 1
            book_allocation.date_issued = datetime.now()
            user = User.query.filter_by(id=book_allocation.user_id).first()
            user.approved_book_count += 1
            user.pending_book_count -= 1
            db.session.commit()
            return {"msg": "Book request granted successfully"}, 200

    @jwt_required()
    def delete(self):
        try:
            data = request.json
            req_id = data.get('req_id')
            current_user_id = get_jwt_identity()
            if not req_id:
                return {"error": "req_id is required"}, 400

            book_allocation = Register.query.filter_by(id=req_id).first()
            if not book_allocation:
                return {"error": "Book request not found"}, 404
            else:
                user = User.query.filter_by(id=book_allocation.user_id).first()
                book_allocation.request_status = 2
                book_allocation.return_date = datetime.now()
                db.session.commit()
                user.pending_book_count -= 1
                db.session.commit()
                return {"msg": "Book request deleted successfully"}, 200
        except Exception as e:
            return {"error": "An error occurred while deleting the book \
                    request: " + str(e)}, 500


class TopReader(Resource):
    @jwt_required()
    def get(self):
        users = User.query.filter_by(role=0).all()
        top_readers = {"labels": [],
                       "datasets": [
            {
                "label": 'Readers',
                "data": []
            }
        ]
        }
        for user in users:
            top_readers["labels"].append(user.email.split('@')[0])
            top_readers["datasets"][0]["data"].append(user.approved_book_count)
        return top_readers


class UserActivity(Resource):
    @jwt_required()
    def get(self):
        users = User.query.filter_by(role=0).all()
        top_readers = {"labels": [],
                       "datasets": [
            {
                "label": 'Requested',
                "data": []
            },
            {
                "label": 'Approved',
                "data": []
            },
            {
                "label": 'Completed',
                "data": []
            }
        ]
        }
        for user in users:
            top_readers["labels"].append(user.email.split('@')[0])
            top_readers["datasets"][0]["data"].append(user.pending_book_count)
            top_readers["datasets"][1]["data"].append(user.approved_book_count)
            top_readers["datasets"][2]["data"].append(user.returned_book_count)
        return top_readers


class TopRequestedBooks(Resource):
    @jwt_required()
    def get(self):
        books = Book.query.filter_by(pseudo_delete=False).all()
        top_books = {"labels": [],
                     "datasets": [
            {
                "label": 'Most Requested Books',
                "data": []
            }
        ]
        }
        for book in books:
            top_books["labels"].append(book.name)
            top_books["datasets"][0]["data"].append(book.count_of_pending_req)
        return top_books


# Resource for approving a book request


class ApproveBookResource(Resource):
    @jwt_required()
    def put(self, req_id):
        try:
            if not user:
                return {"error": "Unauthorized access"}, 401

            book_allocation = Register.query.filter_by(id=req_id).first()
            if not book_allocation:
                return {"error": "Book request not found"}, 404

            user = User.query.filter_by(id=book_allocation.user_id).first()
            book_allocation.request_status = 1
            user.pending_book_count -= 1
            db.session.commit()
            return {"msg": "Book request approved successfully"}, 200
        except Exception as e:
            return {"error": "An error occurred while approving the book request: " + str(e)}, 500
# Resource for adding a new book


class NewBookResource(Resource):
    # Resource for adding a new book
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        user = verify_user_role(current_user_id, 1)

        if user:
            try:
                data = request.json
                book_name = data.get('book_title')
                existing_book = Book.query.filter_by(name=book_name).first()
                if existing_book:
                    return {"error": "Book with name already exists"}, 400
                else:
                    new_book = Book(
                        name=book_name,
                        view_access_link=data.get('book_view_link'),
                        edit_access_link=data.get('book_edit_link'),
                        description=data.get('book_description'),
                        date=datetime.strptime(data.get('book_creation_date'),
                                               '%Y-%m-%d'),
                        price=data.get('book_price'),
                        stock=data.get('book_stock'),
                        author=data.get('book_author'),
                        section_name=data.get('book_section_id')
                    )
                    db.session.add(new_book)
                    db.session.commit()
                    return {"msg": "Book added successfully"}, 200
            except Exception as e:
                return {"error": "An error occurred while adding the book: "
                        + str(e)}, 500
        else:
            return {"error": "Unauthorized access"}, 401

    # Resource for fetching a book by id
    @jwt_required()
    def get(self, book_id):
        current_user_id = get_jwt_identity()
        user = verify_user_role(current_user_id, 1)

        if user:
            try:
                book = Book.query.filter_by(id=book_id).first()
                if book:
                    book_data = {
                        'name': book.name,
                        'view_access_link': book.view_access_link,
                        'edit_access_link': book.edit_access_link,
                        'description': book.description,
                        'date': book.date.strftime('%Y-%m-%d'),
                        'price': book.price,
                        'stock': book.stock,
                        'author': book.author,
                        'section_name': book.section_name,
                    }
                    return book_data, 200
                else:
                    return {"error": "Book not found"}, 404
            except Exception as e:
                return {"error": "An error occurred while fetching the book: " + str(e)}, 500
        else:
            return {"error": "Unauthorized access"}, 401

    # Resource for updating a book
    @jwt_required()
    def put(self, book_id):
        current_user_id = get_jwt_identity()
        user = verify_user_role(current_user_id, 1)

        if user:
            try:
                data = request.get_json()
                name = data.get('name')
                view_access_link = data.get('view_access_link')
                edit_access_link = data.get('edit_access_link')
                description = data.get('description')
                date = data.get('date')
                price = data.get('price')
                stock = data.get('stock')
                author = data.get('author')
                section_name = data.get('section_name')

                book = Book.query.filter_by(id=book_id).first()
                if book:
                    book.name = name
                    book.view_access_link = view_access_link
                    book.edit_access_link = edit_access_link
                    book.edit_access_link = edit_access_link
                    book.description = description
                    book.date = datetime.strptime(date, '%Y-%m-%d')
                    book.price = price
                    book.stock = stock
                    book.author = author
                    book.section_name = section_name
                    db.session.commit()
                    return {"msg": "Book updated successfully"}, 200
                else:
                    return {"error": "Book not found"}, 404
            except Exception as e:
                return {"error": "An error occurred while updating the book: "
                        + str(e)}, 500
        else:
            return {"error": "Unauthorized access"}, 401

    @jwt_required()
    def delete(self, book_id):
        current_user_id = get_jwt_identity()
        user = verify_user_role(current_user_id, 1)

        if user:
            try:
                book = Book.query.filter_by(id=book_id).first()
                if book:
                    book.pseudo_delete = True
                    db.session.commit()
                    return {"msg": "Section deleted successfully"}, 200
                else:
                    return {"error": "Section not found"}, 404
            except Exception as e:
                return {"error": "An error occurred \
                                 deleting the section: " + str(e)}, 500
        else:
            return {"error": "Unauthorized access"}, 401


# Resource for fetching books for librarian


class BookResource(Resource):
    @jwt_required()
    def get(self):
        try:
            books = Book.query.filter_by(pseudo_delete=False).all()

            books_list = []
            for book in books:
                books_list.append({
                    'id': book.id,
                    'name': book.name,
                    'author': book.author,
                    'section_name': book.section_name,
                    'description': book.description,
                    'date': book.date.strftime("%Y-%m-%d"),
                    'price': book.price,
                    'view_access_link': book.view_access_link,
                    'edit_access_link': book.edit_access_link,
                    'stock': book.stock,
                })

            return books_list, 200
        except Exception as e:
            return {"error": "An error occurred while fetching books: "
                    + str(e)}, 500

# Resource for updating book details


class UpdateBookResource(Resource):
    @jwt_required()
    def put(self):
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(
            id=current_user_id, role=1).first()
        if not user:
            return {"error": "Unauthorized access"}, 401
        try:
            data = request.json
            book_id = data.get('book_id')
            book_name = data.get('book_name')
            book_authors = data.get('book_authors')

            book = Book.query.filter_by(book_id=book_id).first()
            if not book:
                return {"error": "Book not found"}, 404

            book.book_name = book_name
            book.book_authors = book_authors
            db.session.commit()

            return {"msg": "Book updated successfully"}, 200
        except Exception as e:
            return {"error": "Failed to update book: " + str(e)}, 500

# Resource for fetching allocated books by a user


class RequestedBooksResource(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            if verify_user_role(current_user_id, 0):
                user_request = Register.query.filter_by(
                    user_id=current_user_id, request_status=0,
                    pseudo_delete=False).all()
            else:
                user_request = Register.query.filter_by(
                    request_status=0, pseudo_delete=False).all()
            requested_books_list = [req.serialize() for req in user_request]
            return requested_books_list, 200
        except Exception as e:
            return {"error": "An error occurred while fetching requested\
                     books: "
                    + str(e)}, 500

    @jwt_required()
    def put(self):
        try:
            data = request.get_json()
            current_user_id = get_jwt_identity()
            user = User.query.filter_by(id=current_user_id).first()
            registration_id = data.get('registration_id')
            if not registration_id:
                return {"error": "registration_id is required"}, 400
            registration = Register.query.filter_by(id=registration_id).first()
            if not registration:
                return {"error": "Registration not found"}, 404

            book = Book.query.filter_by(id=registration.book_id).first()
            user.approved_book_count -= 1
            user.returned_book_count += 1
            book.rank += 1
            registration.return_date = datetime.now()
            registration.request_status = 3
            db.session.commit()

            return {"message": "Registration updated successfully"}, 200
        except Exception as e:
            return {"error": "An error occurred while updating registration: "
                    + str(e)}, 500


class FeedbackResource(Resource):
    @jwt_required()
    def get(self, feedback_id=None):
        try:
            if feedback_id:
                feedback = Feedback.query.filter_by(id=feedback_id).first()
                if feedback:
                    feedback_data = feedback.serialize()
                    return feedback_data, 200
                else:
                    return {"error": "Feedback not found"}, 404
            else:
                feedbacks = Feedback.query.all()
                feedbacks_list = [feedback.serialize()
                                  for feedback in feedbacks]
                return feedbacks_list, 200
        except Exception as e:
            return {"error": "An error occurred while fetching feedbacks: "
                    + str(e)}, 500

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            book_id = data.get('id')
            rate = data.get('rate')
            review = data.get('comments')
            if not book_id or not rate or not review:
                return {"error":
                        "User ID, book ID, rate, and review are required"}, 400
            feedback = Feedback(
                user_id=get_jwt_identity(), book_id=book_id, rate=rate,
                review=review)
            db.session.add(feedback)
            db.session.commit()
            return {"message": "Feedback added successfully"}, 200
        except Exception as e:
            return {"error": "An error occurred while adding feedback: "
                    + str(e)}, 500

    @jwt_required()
    def put(self, feedback_id):
        try:
            feedback = Feedback.query.filter_by(id=feedback_id).first()
            if not feedback:
                return {"error": "Feedback not found"}, 404
            data = request.get_json()
            feedback.user_id = data.get('user_id', feedback.user_id)
            feedback.book_id = data.get('book_id', feedback.book_id)
            feedback.rate = data.get('rate', feedback.rate)
            feedback.review = data.get('review', feedback.review)
            db.session.commit()
            return {"message": "Feedback updated successfully"}, 200
        except Exception as e:
            return {"error": "An error occurred while updating feedback: "
                    + str(e)}, 500

    @jwt_required()
    def delete(self, feedback_id):
        try:
            feedback = Feedback.query.filter_by(id=feedback_id).first()
            if not feedback:
                return {"error": "Feedback not found"}, 404
            db.session.delete(feedback)
            db.session.commit()
            return {"message": "Feedback deleted successfully"}, 200
        except Exception as e:
            return {"error": "An error occurred while deleting feedback: "
                    + str(e)}, 500


# Add resources to the API
api.add_resource(TrackLastLoginResource, '/api/track-last-login')
api.add_resource(SignUpResource, '/api/usersignup')
api.add_resource(LoginResource, '/api/userlogin')
api.add_resource(LibrarianLoginResource, '/api/librarianlogin')
api.add_resource(NewGenreResource, '/api/genres/new',
                 '/api/genres/new/<int:section_id>')
api.add_resource(GenreResource, '/api/genres')
api.add_resource(NewBookResource, '/api/books/new',
                 '/api/books/new/<int:book_id>')
api.add_resource(BooksListResource, '/api/books')
api.add_resource(UserBooksResource,
                 '/api/users/<int:user_id>/books', '/api/fetch_my_books')
api.add_resource(AllocateBookResource, '/api/books/allocate',
                 '/api/delete/request')
api.add_resource(TopReader, '/api/top/readers')
api.add_resource(TopRequestedBooks, '/api/top/books/requested')
api.add_resource(UserActivity, '/api/user/activity')
api.add_resource(BookResource, '/api/fetch/librarian/books')
api.add_resource(UpdateBookResource, '/api/books/update')
api.add_resource(RequestedBooksResource, '/api/books/requested',
                 '/api/return/book')
api.add_resource(FeedbackResource, '/api/add/feedback')
api.add_resource(UserResource, '/api/user/resource/manager')
api.add_resource(DashboardResource, '/api/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
