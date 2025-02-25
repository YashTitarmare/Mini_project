# app.py

'''import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
'''


from flask import Flask, render_template,request,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from config import Config  # user define model of name config  wiht class Config
from models import db, Task, Birthday, MovieAlert,User # user define model of name models wiht  multiples class and varible

#from werkzeug.security import generate_password_hash, check_password_hash

#import birthday_scheduler

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all() 


@app.route('/')
def index():
    return render_template('index.html')   # make sure that the 




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # checking the user  already exists or not first to extute the first statment after  this  is true 

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or Email already exists!', 'danger')
            return redirect(url_for('register'))  # Redirect to register if user exists

        # create a new user
        new_user = User(username=username, email=email, password=password)
        try:  # erro handing
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))  
        except Exception as e:  # excepted erro
            db.session.rollback()    # roll back when the email or password is word 
                                # if not give this the exit the seation 
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('register')) 
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and (user.password, password):
            session['user_id'] = user.id  # checking in the session user_id wiht database id filter by username ?
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()  
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))


# Protect routes using a custom decorator
from functools import wraps  #  its use 

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dashboard')
@login_required
def dashboard():
     
        username = session.get('username')  

        return render_template('dashboard.html', username=username)




@app.route('/profile')
@login_required
def profile():
        email = session.get('email')  
        return render_template('profile.html', email=email)



@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')
        due_date = request.form.get('due_date')

        new_task = Task(
            title=title, 
            description=description, 
            due_date=due_date, 
            user_id=session['user_id']  # Associate with logged-in user
        )
        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding task: {str(e)}", "danger")
        
        return redirect(url_for('tasks'))

    all_tasks = Task.query.filter_by(user_id=session['user_id']).all()  # Fetch user-specific tasks
    return render_template('tasks.html', tasks=all_tasks)


# Update other routes similarly to filter by `user_id` where applicable.








'''@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')
        due_date = request.form.get('due_date')

        print(f"Received Title: {title}, Description: {description}, Due Date: {due_date}")

        new_task = Task(title=title, description=description, due_date=due_date)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")
        except Exception as e:
            db.session.rollback()  # Rollback on error
            print(f"Error adding task: {str(e)}")  # Log the error
            flash(f"Error adding task: {str(e)}", "danger")
        
        return redirect(url_for('tasks'))

    all_tasks = Task.query.all()
    return render_template('tasks.html', tasks=all_tasks)'''


# add 
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    # Ensure the user is logged in and has a valid user_id in the session
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to add a task.", "danger")
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']

        # Create a new task and associate it with the logged-in user
        new_task = Task(title=title, description=description, due_date=due_date, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        
        flash("Task added successfully!", "success")
        return redirect(url_for('tasks'))  # Or redirect to the dashboard or task list

    return render_template('add_task.html')



# edit for task 
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required

def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.due_date = request.form['due_date']
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit_task.html', task=task)
# del  for task 
@app.route('/delete_task/<int:task_id>', methods=['POST'])  #dynamic 
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)  # the fuction is priovde the two condtion at onces 
                                            # .query.get to to id and or 404 if no thier
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))







# Brithday

'''@app.route('/birthdays', methods=['GET', 'POST'])
@login_required
def birthdays():
    if request.method == 'POST':
        name = request.form['name']
        date_of_birth = request.form['date']
        message = request.form.get('message')
        
        # Save the new birthday reminder to the database
        new_birthday = Birthday(name=name, date_of_birth=date_of_birth, message=message)
        db.session.add(new_birthday)
        db.session.commit()
        
        flash("Birthday reminder added successfully!", "success")
        return redirect(url_for('birthdays'))
      
 # Retrieve all birthdays to display
    birthdays = Birthday.query.all()
    print("Birthdays list content:", birthdays)  # This will show all objects in the list
    for birthday in birthdays:
        print("Birthday name:", birthday.name)
        print("Birthday date_of_birth:", birthday.date_of_birth)
    return render_template('birthdays.html', birthdays=birthdays)'''




@app.route('/birthdays', methods=['GET', 'POST'])
@login_required
def birthdays():
    if request.method == 'POST':
        name = request.form['name']
        date_of_birth = request.form['date']
        message = request.form.get('message')

        new_birthday = Birthday(
            name=name, 
            date_of_birth=date_of_birth, 
            message=message,
            user_id=session['user_id']  
        )
        try:
            db.session.add(new_birthday)
            db.session.commit()
            flash("Birthday reminder added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding birthday reminder: {str(e)}", "danger")
        
        return redirect(url_for('birthdays'))

    user_birthdays = Birthday.query.filter_by(user_id=session['user_id']).all()
    return render_template('birthdays.html', birthdays=user_birthdays)







"""@app.route('/add_birthday', methods=['GET', 'POST'])
def add_birthday():
    if request.method == 'POST':
        name = request.form['name']
        date_of_birth = request.form['date']
        subject = request.form['subject']
        message = request.form['message']
        email = request.form['email']
         # New column
        
        if 'user_id' not in session:
            flash('You need to log in first', 'danger')
            return redirect(url_for('login'))  

        user_id = session['user_id']

        new_birthday = Birthday(name=name, date_of_birth=date_of_birth, 
                                subject=subject, message=message, 
                                email=email, user_id=user_id,user_email=user.email,user_password=user.password)
        db.session.add(new_birthday)
        db.session.commit()
        
        flash("Birthday reminder added successfully!", "success")
        return redirect(url_for('birthdays'))  # Redirect to the birthdays page

    return render_template('add_birthday.html')"""




@app.route('/add_birthday', methods=['GET', 'POST'])
def add_birthday():
    if request.method == 'POST':
        name = request.form['name']
        date_of_birth = request.form['date']
        subject = request.form['subject']
        message = request.form['message']
        email = request.form['email']
        
        # Ensure the user is logged in
        if 'user_id' not in session:
            flash('You need to log in first', 'danger')
            return redirect(url_for('login'))

        # Fetch the user ID from the session
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if not user:
            flash('User not found. Please log in again.', 'danger')
            return redirect(url_for('login'))
        
        # Create a new Birthday record
        new_birthday = Birthday(
            name=name,
            date_of_birth=date_of_birth,
            subject=subject,
            message=message,
            email=email,
            user_email=user.email,
            user_password=user.password,
            user_id=user.id  # Set the user_id explicitly
        )
        db.session.add(new_birthday)
        db.session.commit()
        
        flash("Birthday reminder added successfully!", "success")
        return redirect(url_for('birthdays'))

    return render_template('add_birthday.html')



@app.route('/edit_birthday/<int:birthday_id>', methods=['GET', 'POST'])
@login_required

def edit_birthday(birthday_id):
    birthday = Birthday.query.get_or_404(birthday_id)
    if request.method == 'POST':
        birthday.name = request.form['name']
        birthday.date_of_birth = request.form['date']
        db.session.commit()
        return redirect(url_for('dashboard'))  # Redirect to the dashboard or birthdays page
    return render_template('edit_birthday.html', birthday=birthday)















@app.route('/delete_birthday/<int:birthday_id>', methods=['POST'])
@login_required
def delete_birthday(birthday_id):
    birthday = Birthday.query.get_or_404(birthday_id)
    db.session.delete(birthday)
    db.session.commit()
    return redirect(url_for('birthdays'))  # Redirect after deletion

















# Movie 

'''@app.route('/movies', methods=['GET', 'POST'])
@login_required

def movies():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        release_date = request.form['release_date']
        
        # Save the new movie alert to the database
        new_movie = MovieAlert(movie_name=movie_name, release_date=release_date)
        db.session.add(new_movie)
        db.session.commit()
        
        flash("Movie alert added successfully!", "success")
        return redirect(url_for('movies'))

    # Retrieve all movies to display
    all_movies = MovieAlert.query.all()
    return render_template('movies.html', movies=all_movies)'''





@app.route('/movies', methods=['GET', 'POST'])
@login_required
def movies():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        release_date = request.form['release_date']
        
        # Save the new movie alert to the database, associating it with the logged-in user
        new_movie = MovieAlert(
            movie_name=movie_name, 
            release_date=release_date,
            user_id=session['user_id']  # Associate with the logged-in user
        )
        try:
            db.session.add(new_movie)
            db.session.commit()
            flash("Movie alert added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding movie alert: {str(e)}", "danger")
        
        return redirect(url_for('movies'))

    # Retrieve all movie alerts for the logged-in user
    user_movies = MovieAlert.query.filter_by(user_id=session['user_id']).all()
    return render_template('movies.html', movies=user_movies)




@app.route('/add_movie', methods=['GET', 'POST'])
@login_required

def add_movie():
    if 'user_id' not in session:
        flash("You need to log in first", "danger")
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in

    if request.method == 'POST':
        movie_name = request.form['title']
        release_date = request.form['release_date']
        
        # Get the user_id from the session
        user_id = session['user_id']

        # Create the new movie with user_id
        new_movie = MovieAlert(movie_name=movie_name, release_date=release_date, user_id=user_id)
        db.session.add(new_movie)
        db.session.commit()
        flash("Movie alert added successfully!", "success")
        return redirect(url_for('movies'))

    return render_template('add_movie.html')




@app.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required

def edit_movie(movie_id):

    movie = MovieAlert.query.get_or_404(movie_id)
    if request.method == 'POST':
        movie.title = request.form['title']
        movie.release_date = request.form['release_date']
        db.session.commit()
        return redirect(url_for('dashboard'))  # Redirect to the dashboard or movies page
    return render_template('edit_movie.html', movie=movie)


@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
@login_required

def delete_movie(movie_id):
    movie = MovieAlert.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('movies'))  # Redirect after deletion

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
















'''
use ti check the the poper database connect or not 
@app.route('/test-insert', methods=['GET', 'POST'])
def test_insert():
    if request.method == 'POST':
        new_task = Task(title="Test Task", description="This is a test", due_date="2024-11-30")
        try:
            db.session.add(new_task)
            db.session.commit()
            return "Insert successful!"
        except Exception as e:
            db.session.rollback()  # Rollback if there's an error
            print(f"Insert failed: {str(e)}")  # Log the error
            return f"Insert failed: {str(e)}"

    return 
    the // show this is comment part 
        //<form method="POST">
          //  <button type="submit">Test Insert</button>  
        //</form>
    '''















