# Import necessary modules from Flask
# Import secure_filename to safely store file names
# Import os module for operating system dependent functionality
# Import Config class from config module
# Import database and models from models module

from flask import Flask, render_template, request, redirect, url_for  
from werkzeug.utils import secure_filename  
import os  
from config import Config  
from models import db, Note, Task  

# Initialize Flask application
# Load configuration from Config object
# # Initialize the database with the Flask app

app = Flask(__name__)  
app.config.from_object(Config)  
db.init_app(app)  

# Create all database tables
with app.app_context():
    db.create_all()  

# Define the folder for uploading files and create it if it doesn't exist
## Set permissions for the upload folder
upload_folder = os.path.join(os.path.dirname(__file__), 'static/uploads')
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
    os.chmod(upload_folder, 0o775)  

@app.route('/')
def index():
    return render_template('index.html')  # Render the index.html template

#creates tasks
@app.route('/add/', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        # Retrieve form data
        task_name = request.form['name']
        description = request.form['description']
        due_date = request.form['due_date']
        level = request.form['level']
        
        # Create a new task and add it to the database
        new_task = Task(name=task_name, description=description, date=due_date, priority_level=level)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('view_tasks'))  # Redirect to the view_tasks route
    return render_template('add_task.html')  # Render the add_task.html template for GET requests

@app.route('/view/')
def view_tasks():
    tasks = Task.query.all()  # Query all tasks from the database
    return render_template('view_tasks.html', tasks=tasks)  # Render the view_tasks.html template with tasks

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)  # Get task by ID or return 404 if not found
    if request.method == 'POST':
        # Update task attributes with form data
        task.name = request.form['name']
        task.description = request.form['description']
        task.date = request.form['due_date']
        task.priority_level = request.form['level']
        
        db.session.commit()  # Commit the changes to the database
        return redirect(url_for('view_tasks'))  # Redirect to the view_tasks route
    return render_template('edit_task.html', task=task)  # Render the edit_task.html template with task data

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)  # Get task by ID or return 404 if not found
    db.session.delete(task)  # Delete the task from the database
    db.session.commit()  # Commit the changes to the database
    return redirect(url_for('view_tasks'))  # Redirect to the view_tasks route

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)  # Get task by ID or return 404 if not found
    task.completion_status = 'completed'  # Update task completion status
    db.session.commit()  # Commit the changes to the database
    return redirect(url_for('view_tasks'))  # Redirect to the view_tasks route

@app.route('/my_video/')
def my_video():
    return render_template('video.html')  # Render the video.html template

@app.route('/info/')
def info():
    return render_template('info.html')  # Render the info.html template

# Helper function to check if a file is allowed based on its extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']  

@app.route('/add_note/', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        note_type = request.form['type']
        if note_type == 'text':
            text = request.form['text']
            new_note = Note(note_type='text', content=text)  # Create a new text note
        else:
            file = request.files['file']
            if 'file' not in request.files:
               flash('No file part')
               return redirect('add_note.html')  # Redirect if no file part is present
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)  # Secure the filename
                file_path = os.path.join(upload_folder, filename)
                try:
                    print(f"Saving file to {upload_folder}")
                    with open(file_path, 'wb') as f:
                        f.write(file.read())  # Save the file to the upload folder
                except Exception as e:
                    print(f"Error saving file: {e}")
                    return str(e)  # Return error message if saving fails
                new_note = Note(note_type=note_type, content=filename)  # Create a new file note
        db.session.add(new_note)
        db.session.commit()  # Commit the new note to the database
        return redirect(url_for('view_notes'))  # Redirect to the view_notes route
    return render_template('add_note.html')  # Render the add_note.html template for GET requests

@app.route('/view_note/')
def view_notes():
    notes = Note.query.all()  # Query all notes from the database
    return render_template('view_notes.html', notes=notes)  # Render the view_notes.html template with notes

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)  # Get note by ID or return 404 if not found
    db.session.delete(note)  # Delete the note from the database
    db.session.commit()  # Commit the changes to the database
    return redirect(url_for('view_notes'))  # Redirect to the view_notes route

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)  # Run the Flask application
