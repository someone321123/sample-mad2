import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime, timedelta
from celery import Celery
from celery.schedules import crontab
import matplotlib.pyplot as plt
import io
import base64
from sqlalchemy import distinct, func
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template


current_dir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3")
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
# Configured Celery to use Redis as the message broker and scheduler
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()




# Initialize Celery
celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])


# Configure Celery to use Redis as the message broker
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',  # Set timezone to Indian Standard Time (IST)
)




# maintains the login system
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(80), nullable=False)


class Section(db.Model):
    __tablename__ = 'section'
    section_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    section_name = db.Column(db.String(50), nullable=False)
    section_description = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    book_count = db.Column(db.Integer, default=0)


class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    book_name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(50))
    sec_id = db.Column(db.Integer, db.ForeignKey("section.section_id"), nullable=False)


class Requested(db.Model):
    __tablename__ = 'requested'
    req_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    no_of_days = db.Column(db.Integer, nullable=False)


class Granted(db.Model):
    __tablename__ = 'granted'
    req_id = db.Column(db.Integer, db.ForeignKey("requested.req_id"), primary_key=True, unique=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    date_issued = db.Column(db.DateTime, default=datetime.now)
    return_date = db.Column(db.DateTime, default=lambda: datetime.now() + timedelta(days=7))


class Completed(db.Model):
    __tablename__ = 'completed'
    req_id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id"), nullable=False)
    date_issued = db.Column(db.DateTime, default=datetime.now)
    date_returned = db.Column(db.DateTime, default=lambda: datetime.now() + timedelta(days=7))


class UserActivity(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),primary_key=True, nullable=False, unique=True)
    last_login = db.Column(db.DateTime)


@app.route('/')
def index():
    daily_reminder()
    monthly_report()
    auto_revoke_access()
    return render_template("index.html")




SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "code.techiesd@gmail.com"
SENDER_PASSWORD = "dummypass"

@celery.task
def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True

@celery.task
def daily_reminder():
    # Adjusted query to fetch users who haven't logged in for a day
    users = (User.query.join(UserActivity, User.id == UserActivity.user_id, isouter=True).filter((UserActivity.last_login < datetime.now() - timedelta(days=1)) |(UserActivity.last_login == None)).all())
    # users = User.query.all() 
 
    for user in users:
        if user.id != 1:
            with open("templates/daily-reminder.html") as file:
                template = Template(file.read())

                message = template.render(data=user)

            send_email(user.email, subject="Daily Reminder", message=message)
    


# send monthly report on the first day of every month
def monthly_report():
    
    # Fetching the librarian
    user = User.query.order_by(User.id).first()

    today = datetime.now()

    if today.day == 1:
        start_date = today.replace(day=1)
        end_date = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    
        granted_count = db.session.query(Granted).filter(Granted.date_issued >= start_date, Granted.date_issued <= end_date).count()
        completed_count = db.session.query(Completed).filter(Completed.date_returned >= start_date, Completed.date_returned <= end_date).count()
        
        with open("templates/monthly-report.html") as file:
            template = Template(file.read())

            message = template.render(data=user, granted_count=granted_count+completed_count, completed_count=completed_count, start_date=start_date)

        send_email(user.email, subject="Monthly report", message=message)





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')

        # Check if the user is the librarian (first user in the table)
        librarian = User.query.order_by(User.id).first()

        if librarian.username == username and checkpw(password.encode('utf-8'), librarian.password.encode('utf-8')):
            login_user(librarian)  # Logs in the librarian
            return redirect(url_for('librarian'))

        user = User.query.filter_by(username=username).first()

        if user and checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)  # Logs in the user
            # Check if the user has already logged in before
            user_activity = UserActivity.query.filter_by(user_id=user.id).first()
            if user_activity:
                user_activity.last_login = datetime.now()  # Update the last login time
            else:
                user_activity = UserActivity(user_id=user.id, last_login=datetime.now())
                db.session.add(user_activity)
            db.session.commit()
            return redirect(url_for('home', userid=user.id))  # Redirect to home page after successful login
        else:
            # error_message = "Invalid username or password. Please try again."
            return redirect(url_for("index") + "#/invalid-login")
    return render_template("index.html")



#The register function maintains user registration, it adds new user form entries to the user database.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('Username')
        name = request.form.get('Name')
        email = request.form.get('Email')
        password = request.form.get('Password')

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            # error_message = "Username already exists. Please choose a different username."
            return redirect(url_for("index") + "#/existing-username")
        if existing_email:
            # error_message = "Email already exists. Please use a different email."
            return redirect(url_for("index") + "#/existing-email")

        hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
        
        new_user = User(username=username, name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("index") + "#/login")

    return render_template("index.html")





@app.route('/add-section', methods=['POST'])
@login_required
def add_section():
    if request.method == 'POST':
        section_name = request.form.get('SectionName')
        section_description = request.form.get('SecDesc')
        date_created = datetime.now()
        book_count = 0

        new_section = Section(section_name=section_name, section_description=section_description,
                              date_created=date_created, book_count=book_count)
        db.session.add(new_section)
        db.session.commit()

        return redirect(url_for('librarian'))  # Redirect to librarian dashboard after adding section
    


@app.route('/edit-section', methods=['GET', 'POST'])
@login_required
def edit_section():
    if request.method == 'POST':
        section_id = request.form.get('SectionID')
        section_name = request.form.get('SectionName')
        section_description = request.form.get('SecDesc')

        section = Section.query.get(section_id)
        if not section:
            return "Section not found", 404

        section.section_name = section_name
        section.section_description = section_description
        db.session.commit()

        return redirect(url_for('librarian'))  # Redirect to librarian dashboard after editing section



@app.route('/edit-book', methods=['GET', 'POST'])
@login_required
def edit_book():
    if request.method == 'POST':
        section_id = request.form.get('SectionID')
        book_id = request.form.get('BookID')
        book_name = request.form.get('BookName')
        author = request.form.get('AuthorName')

        book = Book.query.get(book_id)
        if not book:
            return "Book not found", 404
        
        book.book_id = book_id
        book.book_name = book_name
        book.author = author
        db.session.commit()

        return redirect(url_for('view_section', section_id=section_id))


@app.route('/add-book', methods=['POST'])
@login_required
def add_book():
    if request.method == 'POST':
        book_name = request.form.get('bookName')
        author_name = request.form.get('authorName')
        section_name = request.form.get('sectionName')

        section = Section.query.filter_by(section_name=section_name).first()
        if not section:
            return "Section not found", 404

        new_book = Book(book_name=book_name, author=author_name, sec_id=section.section_id)
        db.session.add(new_book)
        db.session.commit()

        # Update the book count of the section
        section.book_count += 1
        db.session.commit()

        return redirect(url_for('librarian'))  # Redirect to librarian dashboard after adding book

    return redirect(url_for('librarian'))  # Redirect to librarian dashboard if request method is not POST


@app.route('/add-book-2', methods=['POST'])
@login_required
def add_book2():
    if request.method == 'POST':
        book_name = request.form.get('bookName')
        author_name = request.form.get('authorName')
        section_name = request.form.get('sectionName')

        section = Section.query.filter_by(section_name=section_name).first()
        if not section:
            return "Section not found", 404

        new_book = Book(book_name=book_name, author=author_name, sec_id=section.section_id)
        db.session.add(new_book)
        db.session.commit()

        # Update the book count of the section
        section.book_count += 1
        db.session.commit()

        section_id = new_book.sec_id

        return redirect(url_for('view_section', section_id=section_id))  # Redirect to librarian dashboard after adding book

    return redirect(url_for('view_section', section_id=section_id))  # Redirect to librarian dashboard if request method is not POST




@app.route('/view-section/<int:section_id>', methods=['GET'])
@login_required
def view_section(section_id):
    section = Section.query.get(section_id)
    if not section:
        return "Section not found", 404

    books = Book.query.filter_by(sec_id=section_id).all()
    return render_template("books.html", section=section, books=books)



@app.route('/delete-book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return "Book not found", 404

    section_id = book.sec_id
    db.session.delete(book)
    db.session.commit()

    section = Section.query.get(section_id)
    if section:
        section.book_count -= 1
        db.session.commit()

    return redirect(url_for('view_section', section_id=section_id))





@app.route('/accept-request', methods=['POST'])
@login_required
def accept_request():
    if request.method == 'POST':
        req_id = request.form.get('req_id')
        user_id = request.form.get('user_id')
        book_id = request.form.get('book_id')
        no_of_days = int(request.form.get('no_of_days'))

        return_date = datetime.now() + timedelta(days=no_of_days)

        new_granted_request = Granted(req_id=req_id, user_id=user_id, book_id=book_id,
                                      date_issued=datetime.now(), return_date=return_date)
        db.session.add(new_granted_request)

        requested_request = Requested.query.get(req_id)
        if requested_request:
            db.session.delete(requested_request)

        db.session.commit()

        # revoke_access.apply_async(args=[req_id], eta=return_date)

        # if return_date <= datetime.now():
        #     revoke_request(req_id)

        return redirect(url_for('lib_borrow')) 
    
    


@app.route('/reject-request', methods=['POST'])
@login_required
def reject_request():
    if request.method == 'POST':
        # Extract request details from the form data
        req_id = request.form.get('req_id')

        # Delete the request from the 'requested' table
        requested_request = Requested.query.get(req_id)
        if requested_request:
            db.session.delete(requested_request)
            db.session.commit()

        return redirect(url_for('lib_borrow'))  # Redirect to borrow requests page after rejecting request
    

@app.route('/cancel-request', methods=['POST'])
@login_required
def cancel_request():
    if request.method == 'POST':
        # Extract request details from the form data
        req_id = request.form.get('req_id')
    
    # Delete the request from the 'requested' table
        requested_request = Requested.query.get(req_id)
        if requested_request:
            db.session.delete(requested_request)
            db.session.commit()

    return redirect(url_for('my_books', userid=requested_request.user_id))




@app.route('/revoke-request/<int:req_id>', methods=['POST'])
@login_required
def revoke_request(req_id):
    if request.method == 'POST':
        # Fetch the granted request from the database
        granted_request = Granted.query.get(req_id)
        
        if granted_request:
            # Copy the granted request to the completed table with today's date as the return date
            new_completed_request = Completed(req_id=granted_request.req_id,
                                              user_id=granted_request.user_id,
                                              book_id=granted_request.book_id,
                                              date_issued=granted_request.date_issued,
                                              date_returned=datetime.now())
            db.session.add(new_completed_request)
            db.session.commit()

            # Delete the granted request from the granted table
            db.session.delete(granted_request)
            db.session.commit()

        return redirect(url_for('lib_borrow'))  # Redirect to borrow requests page after revoking request



# Celery task for revoking access to the book on the return date
@celery.task
def auto_revoke_access():
    granted_requests = Granted.query.all()
    for request in granted_requests:
        if request.return_date <= datetime.now():
            new_completed_request = Completed(req_id=request.req_id,user_id=request.user_id,book_id=request.book_id,date_issued=request.date_issued,date_returned=datetime.now())

            db.session.add(new_completed_request)
            db.session.commit()

            db.session.delete(request)
            db.session.commit()



@app.route('/borrow-requests')
@login_required
def lib_borrow():
    auto_revoke_access()
    # Fetch pending requests from the database
    users = User.query.all()
    books = Book.query.all()
    pending_requests = Requested.query.all()
    granted_requests = Granted.query.all()
    completed_requests = Completed.query.all()
    return render_template("lib-borrow.html", pending_requests=pending_requests, granted_requests=granted_requests, completed_requests=completed_requests, books=books, users=users)



# Define the Celery beat schedule for periodic tasks
celery.conf.beat_schedule = {
    'daily-reminder-task': {
        'task': 'your_module.daily_reminder',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
    'monthly-report-task': {
        'task': 'your_module.monthly_report',
        'schedule': crontab(hour=0, minute=0),  # Run monthly on the 1st day at midnight
    },
    'auto-revoke-access-task': {
        'task': 'your_module.auto_revoke_access',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
}



@app.route('/librarian', methods=['GET', 'POST'])
@login_required
def librarian():
    sections = Section.query.all()

    search_query = request.args.get('search')
    if search_query:
        sections = Section.query.filter((Section.section_name.ilike(f"%{search_query}%"))).all()
    return render_template("librarian.html", sections=sections)


# Add a new route for deleting sections
@app.route('/delete-section', methods=['POST'])
@login_required
def delete_section():
    if request.method == 'POST':
        section_id = request.form.get('section_id')
        section = Section.query.get(section_id)
        if section:
            db.session.delete(section)
            db.session.commit()
            return redirect(url_for('librarian'))  # Redirect to librarian dashboard after deleting section
        else:
            # Handle the case where the section does not exist
            return "Section not found", 404

    return redirect(url_for('librarian'))  # Redirect to librarian dashboard if request method is not POST



@app.route('/request-book', methods=['POST'])
@login_required
def request_book():
    if request.method == 'POST':
        user_id = request.form.get('UserID')
        book_id = request.form.get('BookID')
        no_of_days = request.form.get('Days')

        # Check if the user has already requested the book
        existing_request = Requested.query.filter_by(user_id=user_id, book_id=book_id).first()
        if existing_request:
            return redirect(url_for('home', userid=user_id) + '#/already-requested')
        
        granted_request = Granted.query.filter_by(user_id=user_id, book_id=book_id).first()
        if granted_request:
            return redirect(url_for('home', userid=user_id) + '#/granted-request')
        

        # Check the total number of pending and granted requests for the user
        total_requests = Requested.query.filter_by(user_id=user_id).count() + \
                         Granted.query.filter_by(user_id=user_id).count()
        
        #denies to place more than 5 book requests at a time
        if total_requests == 5:
            return redirect(url_for('home', userid=user_id) + '#/max-request-limit-reached')


        # Create a new entry in the 'requested' table
        new_request = Requested(user_id=user_id, book_id=book_id, no_of_days=no_of_days)
        db.session.add(new_request)
        db.session.commit()

        return redirect(url_for('home', userid=user_id))  # Redirect to the home page after successful request




@app.route('/my-books/<int:userid>')
@login_required
def my_books(userid):
    user = User.query.get(userid)
    if not user:
        return "User not found", 404

    # Query the database to get the books associated with the user
    granted_requests = Granted.query.filter_by(user_id=userid).all()
    pending_requests = Requested.query.filter_by(user_id=userid).all()
    completed_requests = Completed.query.filter_by(user_id=userid).all()
    books = Book.query.all()

    return render_template("mybooks.html", user=user, pending_requests=pending_requests, granted_requests=granted_requests, completed_requests=completed_requests, books=books)





@app.route('/user-revoke-request/<int:req_id>', methods=['POST'])
@login_required
def user_revoke_request(req_id):
    if request.method == 'POST':
        # Fetch the granted request from the database
        granted_request = Granted.query.get(req_id)
        
        if granted_request:
            # Copy the granted request to the completed table with today's date as the return date
            new_completed_request = Completed(req_id=granted_request.req_id,
                                              user_id=granted_request.user_id,
                                              book_id=granted_request.book_id,
                                              date_issued=granted_request.date_issued,
                                              date_returned=datetime.now())
            db.session.add(new_completed_request)
            db.session.commit()

            # Delete the granted request from the granted table
            db.session.delete(granted_request)
            db.session.commit()

        return redirect(url_for('my_books', userid=granted_request.user_id))  # Redirect to borrow requests page after revoking request




@app.route('/home/<int:userid>', methods=['GET', 'POST'])
@login_required
def home(userid):
    # Query all sections and their respective books
    sections = Section.query.all()
    sections_with_books = []
    for section in sections:
        books = Book.query.filter_by(sec_id=section.section_id).all()
        sections_with_books.append({'section': section, 'books': books})

    search_query = request.args.get('search')
    if search_query:
        sections_with_books = []
        for section in sections:
            books = Book.query.filter((Book.sec_id == section.section_id) & (Book.book_name.ilike(f"%{search_query}%"))).all()
            if books:
                sections_with_books.append({'section': section, 'books': books})

    users = User.query.filter_by(id=userid).first()
    return render_template('home.html', userid=userid, username=users.username, sections_with_books=sections_with_books)




# This function is basically for summarizing the highest requested books and sections and plotting graphs for it using matplotlib
@app.route('/lib-summary')
def lib_summary():
    top_books = db.session.query(Book.book_name, 
                                 db.func.count(distinct(Requested.req_id)).label('requested_count'),
                                 db.func.count(distinct(Granted.req_id)).label('granted_count'),
                                 db.func.count(distinct(Completed.req_id)).label('completed_count')) \
                    .outerjoin(Requested, Book.book_id == Requested.book_id) \
                    .outerjoin(Granted, Book.book_id == Granted.book_id) \
                    .outerjoin(Completed, Book.book_id == Completed.book_id) \
                    .group_by(Book.book_id) \
                    .order_by(db.func.count(distinct(Requested.req_id)) + 
                              db.func.count(distinct(Granted.req_id)) + 
                              db.func.count(distinct(Completed.req_id)).desc()) \
                    .limit(8) \
                    .all()
    
    top_books_data = [{'book_name': book[0], 
                       'total_requests': book[1] + book[2] + book[3]} 
                      for book in top_books]
    

    # Plotting the graph
    book_names = [book['book_name'] for book in top_books_data]
    total_requests = [book['total_requests'] for book in top_books_data]
    
    plt.figure(figsize=(10, 6))
    plt.barh(book_names, total_requests, color='skyblue')
    plt.xlabel('Total Requests')
    plt.ylabel('Book Name')
    plt.title(' Most Requested Books')
    plt.gca().invert_yaxis()  # Invert y-axis to display top book at the top
    plt.tight_layout()

    # Save plot to a bytes object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url1 = base64.b64encode(img.getvalue()).decode()



    top_sections = {}
    for book in top_books_data:
        section_name = Section.query.join(Book, Book.sec_id == Section.section_id).filter(Book.book_name == book['book_name']).first().section_name
        if section_name in top_sections:
            top_sections[section_name] += book['total_requests']
        else:
            top_sections[section_name] = book['total_requests']

    top_sections_sorted = sorted(top_sections.items(), key=lambda x: x[1], reverse=True)[:4]



    # Plotting the pie chart for top requested sections
    section_names = [section[0] for section in top_sections_sorted]
    request_counts = [section[1] for section in top_sections_sorted]

    plt.figure(figsize=(8, 8))
    plt.pie(request_counts, labels=section_names, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Top Requested Sections')

    # Save plot to a bytes object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Convert bytes object to base64 encoded string
    plot_url2 = base64.b64encode(img.getvalue()).decode()

    return render_template('libsummary.html', top_books=top_books_data, plot_url1=plot_url1, top_sections=top_sections_sorted, plot_url2=plot_url2)



#logs out the user or librarian
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)