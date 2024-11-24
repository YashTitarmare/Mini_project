# app.py

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from flask import Flask, render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Task, Birthday, MovieAlert

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


with app.app_context():
    db.create_all() 



@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/tasks', methods=['GET', 'POST'])
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
    return render_template('tasks.html', tasks=all_tasks)


# add 
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        new_task = Task(title=title, description=description, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
        #return redirect(url_for('dashboard'))
    return render_template('add_task.html')


# edit for task 
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
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
@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))






# Brithday

@app.route('/birthdays', methods=['GET', 'POST'])
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
    return render_template('birthdays.html', birthdays=birthdays)


@app.route('/add_birthday', methods=['GET', 'POST'])
def add_birthday():
    if request.method == 'POST':
        name = request.form['name']
        date_of_birth = request.form['date']

        new_birthday = Birthday(name=name, date_of_birth=date_of_birth)
        db.session.add(new_birthday)
        db.session.commit()
        #return redirect(url_for('dashboard'))
    return render_template('add_birthday.html')


@app.route('/edit_birthday/<int:birthday_id>', methods=['GET', 'POST'])
def edit_birthday(birthday_id):
    birthday = Birthday.query.get_or_404(birthday_id)
    if request.method == 'POST':
        birthday.name = request.form['name']
        birthday.date_of_birth = request.form['date']
        db.session.commit()
        return redirect(url_for('dashboard'))  # Redirect to the dashboard or birthdays page
    return render_template('edit_birthday.html', birthday=birthday)

@app.route('/delete_birthday/<int:birthday_id>', methods=['POST'])
def delete_birthday(birthday_id):
    birthday = Birthday.query.get_or_404(birthday_id)
    db.session.delete(birthday)
    db.session.commit()
    return redirect(url_for('birthdays'))  # Redirect after deletion

















# Movie 

@app.route('/movies', methods=['GET', 'POST'])
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
    return render_template('movies.html', movies=all_movies)



@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movie_name = request.form['title']
        release_date = request.form['release_date']
        new_movie = MovieAlert(movie_name=movie_name, release_date=release_date)
        db.session.add(new_movie)
        db.session.commit()
        #return redirect(url_for('dashboard'))
    return render_template('add_movie.html')



@app.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):

    movie = MovieAlert.query.get_or_404(movie_id)
    if request.method == 'POST':
        movie.title = request.form['title']
        movie.release_date = request.form['release_date']
        db.session.commit()
        return redirect(url_for('dashboard'))  # Redirect to the dashboard or movies page
    return render_template('edit_movie.html', movie=movie)


@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    movie = MovieAlert.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('dashboard'))  # Redirect after deletion


















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














if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
