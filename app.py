from flask import Flask, request, redirect, render_template, flash, session,  send_file
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename




app = Flask(__name__)
app.secret_key = "secret_key"  # Used for flash messages and session management

# Initialize the database
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()



# Manually initialize the database on the first request
@app.route('/')

def index():
  
    return render_template('index.html')  # A simple homepage
@app.route('/choose')
def choose():
    try:
        conn = sqlite3.connect('students.db')
        conn.execute('SELECT * FROM students LIMIT 1')  # Test query
    except sqlite3.OperationalError:
        init_db()  # Initialize the database if not found
    return render_template('choose.html')  

# Route for student registration 
@app.route('/register', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']

        # Insert into database
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO students (name, email, age)
            VALUES (?, ?, ?)
        ''', (name, email, age))
        conn.commit()
        conn.close()

        flash('Student registered successfully!')
        return redirect('/login')  # Redirect to the list of students

    return render_template('register.html')

# Route to display all students
@app.route('/students', methods=['GET'])
def get_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    students = c.fetchall()
    conn.close()
    return render_template('students.html', students=students)

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']

        # Validate login against the database
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute('SELECT * FROM students WHERE name = ? AND email = ?', (name, email))
        student = c.fetchone()  # Get the first matching student

        if student:
            # Store the student's ID and name in the session
            session['student_id'] = student[0]
            session['student_name'] = student[1]
            flash('Login successful!', 'success')
            return redirect('/dashboard')  # Redirect to the dashboard after login
        else:
            flash('Invalid name or email!', 'error')
            return render_template('login.html')  # Reload the login page with an error message
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'student_id' not in session:
        return redirect('/login')  # Redirect to login if not logged in

    cards = [
        {"title": "FOS LMS", "description": "Faculty Of Science Learning Management System", "icon": "bi-person-circle", "link": "#"},
        {"title": "Library System", "description": "Manage your books and library activities", "icon": "bi-book", "link": "/studentbooks"},
        {"title": "Student Portal", "description": "Access your grades and profile", "icon": "bi-person", "link": "#"},
        {"title": "Course Registration", "description": "Register for courses every semester", "icon": "bi-pencil", "link": "#"},
        {"title": "Exam Schedule", "description": "Check your exam timetable", "icon": "bi-calendar", "link": "#"},
        {"title": "Faculty Dashboard", "description": "Manage faculty related tasks", "icon": "bi-chalkboard", "link": "#"},
        {"title": "Grades Portal", "description": "View and manage your grades", "icon": "bi-file-earmark-check", "link": "#"},
        {"title": "Student Activities", "description": "Explore extracurricular activities", "icon": "bi-people", "link": "#"},
        {"title": "Research System", "description": "Access research papers and publications", "icon": "bi-journal-text", "link": "#"},
        {"title": "Support Desk", "description": "Contact for technical support", "icon": "bi-telephone", "link": "#"}
    ]
    return render_template('dashboard.html', cards=cards)


# Logout route
@app.route('/logout')
def logout():
    session.pop('student_id', None)  # Remove student from session
    session.pop('student_name', None)
    flash('You have been logged out.', 'info')
    return redirect('/login')  # Redirect to login page after logout

# @app.route('/studentbooks', methods=['GET'])
# def list_books():
#     with sqlite3.connect(DATABASE) as conn:
#         cursor = conn.cursor()
#         cursor.execute('SELECT id, title, author, catagory, isbn, filename FROM library')
#         books = cursor.fetchall()
#     return render_template('studentbooks.html', books=books)

# # Route to download a book
# # Route to download a book
# @app.route('/download/<int:book_id>', methods=['GET'])
# def download_book(book_id):
#     with sqlite3.connect(DATABASE) as conn:
#         cursor = conn.cursor()
#         # Corrected query to fetch from the 'library' table, not 'books'
#         cursor.execute('SELECT filename FROM library WHERE id = ?', (book_id,))
#         book = cursor.fetchone()
#         if book:
#             filename = book[0]
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             if os.path.exists(file_path):
#                 return send_file(file_path, as_attachment=True)
#             else:
#                 flash('File not found on the server!', 'danger')
#                 return redirect('/studentbooks')
#         else:
#             flash('Book not found!', 'danger')
#             return redirect('/studentbooks')





###############################################
#Admin route codes
def init_db():
    conn = sqlite3.connect('administrative.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS administrative (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            password pasword NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/adminindex')
def admin_index():
    try:
        conn = sqlite3.connect('administrative.db')
        conn.execute('SELECT * FROM administrative LIMIT 1')  
    except sqlite3.OperationalError:
        init_db()  # Initialize the database if not found
    return render_template('adminindex.html')  

# Route for admin registration 
@app.route('/adminregister', methods=['GET', 'POST'])
def register_register():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        password = request.form.get('password')

        # Insert into database
        conn = sqlite3.connect('administrative.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO administrative (name, email, age, password)
            VALUES (?, ?, ?, ?)
        ''', (name, email, age, password))
        conn.commit()
        conn.close()

        flash('Admin registered successfully!')
        return redirect('/adminlogin')  # Redirect to the list of admins

    return render_template('adminregister.html')


@app.route('/administrative', methods=['GET'])
def get_admins():
    conn = sqlite3.connect('administrative.db')
    c = conn.cursor()
    c.execute('SELECT * FROM administrative')
    administrative = c.fetchall()
    conn.close()
    return render_template('admins.html', administrative=administrative)

# Route for login page
@app.route('/adminlogin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        # Get form data
       
        email = request.form['email']
        password = request.form.get('password')

        # Validate login against the database
        conn = sqlite3.connect('administrative.db')
        c = conn.cursor()
        c.execute('SELECT * FROM administrative WHERE email = ? AND password = ?', ( email, password))
        administrative = c.fetchone()  

        if administrative:
            # Store the admin's ID and name in the session
            session['admin_id'] = administrative[0]
            session['admin_email'] =administrative[1]
            flash('Login successful!', 'success')
            return redirect('/admindashboard')  # Redirect to the dashboard after login
        else:
            flash('Invalid email or password!', 'error')
            return render_template('adminlogin.html')  # Reload the login page with an error message
    
    return render_template('adminlogin.html')

@app.route('/admindashboard')
def dashboard_admin():
    if 'admin_id' not in session:
        return redirect('/adminlogin')  # Redirect to login if not logged in

    cards = [
        {"title": "FOS LMS", "description": "Faculty Of Science Learning Management System", "icon": "bi-person-circle", "link": "#"},
        {"title": "Library System", "description": "Manage your books and library activities", "icon": "bi-book", "link": "/libraryadmin"},
        {"title": "Student Portal", "description": "Access your grades and profile", "icon": "bi-person", "link": "#"},
        {"title": "Course Registration", "description": "Register for courses every semester", "icon": "bi-pencil", "link": "#"},
        {"title": "Exam Schedule", "description": "Check your exam timetable", "icon": "bi-calendar", "link": "#"},
        {"title": "Faculty Dashboard", "description": "Manage faculty related tasks", "icon": "bi-chalkboard", "link": "#"},
        {"title": "Grades Portal", "description": "View and manage your grades", "icon": "bi-file-earmark-check", "link": "#"},
        {"title": "Student Activities", "description": "Explore extracurricular activities", "icon": "bi-people", "link": "#"},
        {"title": "Research System", "description": "Access research papers and publications", "icon": "bi-journal-text", "link": "#"},
        {"title": "Support Desk", "description": "Contact for technical support", "icon": "bi-telephone", "link": "#"}
    ]
    return render_template('admindashboard.html', cards=cards)


# Logout route
@app.route('/adminlogout')
def logout_admin():
    session.pop('admin_id', None)  # Remove student from session
    session.pop('admin_email', None)
    flash('You have been logged out.', 'info')
    return redirect('/adminlogin')  # Redirect to login page after logout




@app.route('/libraryadmin')
def library_admin():
    cards = [
        {"title": "Add Books", "description": "Using this interface for adding the books", "icon": "bi-person-circle", "link": "/addbook"},
        {"title": " Book", "description": "All books display here", "icon": "bi-book", "link": "/books"},
        {"title": "Delete Book", "description": "Outdated books for deleting", "icon": "bi-person", "link": "/books"},
        {"title": "Reporting", "description": "This is reporting part", "icon": "bi-pencil", "link": "/books"},
 
       
    ]

    return render_template('libraryadmin.html', cards=cards) 


# Configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
DATABASE = 'library.db'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create the folder for storing PDFs if it doesn't exist

# Allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize the database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                catagory TEXT NOT NULL,
                ISBN INTEGER NOT NULL,
                filename TEXT NOT NULL
            )
        ''')
    conn.commit()

init_db()

#  Admin Routes
@app.route('/admin/books', methods=['GET'])
def admin_list_books():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, author, catagory, isbn, filename FROM library')
        books = cursor.fetchall()
    return render_template('admin_books.html', books=books)  # Admin-specific template

@app.route('/admin/addbook', methods=['GET', 'POST'])
def admin_add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        catagory = request.form.get('catagory')
        isbn = request.form.get('isbn')
        file = request.files.get('file')

        # Validate inputs
        if not title or not author or not catagory or not isbn or not file:
            flash('All fields are required!', 'danger')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Only PDF files are allowed!', 'danger')
            return redirect(request.url)

        # Secure the file name and save
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save book metadata to the database
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO library (title, author, catagory, isbn, filename) 
                VALUES (?, ?, ?, ?, ?)
            ''', (title, author, catagory, isbn, filename))
        conn.commit()

        flash('Book uploaded successfully!', 'success')
        return redirect('/admin/books')

    return render_template('addbook.html')


# # Route to display the book upload form
# @app.route('/admin/addbook', methods=['GET', 'POST'])
# def add_book():
#     if request.method == 'POST':
#         title = request.form.get('title')
#         author = request.form.get('author')
#         catagory = request.form.get('catagory')
#         isbn = request.form.get('isbn')
#         file = request.files.get('file')

#         # Validate inputs
#         if not title or not author or not catagory or not isbn or not file:
#             flash('All fields are required!', 'danger')
#             return redirect(request.url)

#         if not allowed_file(file.filename):
#             flash('Only PDF files are allowed!', 'danger')
#             return redirect(request.url)

#         # Secure the file name and save
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#         # Save book metadata to the database
#         with sqlite3.connect(DATABASE) as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 INSERT INTO library (title, author, catagory, isbn, filename) 
#                 VALUES (?, ?, ?, ?, ?)
#             ''', (title, author, catagory, isbn, filename))
#         conn.commit()

#         flash('Book uploaded successfully!', 'success')
#         return redirect('/books')

#     return render_template('addbook.html')

# Route to display all books
@app.route('/books', methods=['GET'])
def list_books():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, author, catagory, isbn, filename FROM library')
        books = cursor.fetchall()
    return render_template('books.html', books=books)

# Route to download a book
# Route to download a book
@app.route('/download/<int:book_id>', methods=['GET'])
def download_book(book_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Corrected query to fetch from the 'library' table, not 'books'
        cursor.execute('SELECT filename FROM library WHERE id = ?', (book_id,))
        book = cursor.fetchone()
        if book:
            filename = book[0]
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
            else:
                flash('File not found on the server!', 'danger')
                return redirect('/books')
        else:
            flash('Book not found!', 'danger')
            return redirect('/books')

# Route to delete a book
@app.route('/admin/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        # Fetch the file name to delete from storage
        cursor.execute('SELECT filename FROM library WHERE id = ?', (book_id,))
        book = cursor.fetchone()
        if book:
            filename = book[0]
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Delete the file from storage if it exists
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Delete the record from the database
            cursor.execute('DELETE FROM library WHERE id = ?', (book_id,))
            conn.commit()
            flash('Book deleted successfully!', 'success')
        else:
            flash('Book not found!', 'danger')    
           
        return render_template('books.html')


if __name__ == '__main__':
    app.run(debug=True)


