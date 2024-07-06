from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from config import Config
from models import db, Note, Task

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

upload_folder = os.path.join(os.path.dirname(__file__), 'static/uploads')
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
    os.chmod(upload_folder, 0o775)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add/', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task_name = request.form['name']
        description = request.form['description']
        due_date = request.form['due_date']
        level = request.form['level']
        new_task = Task(name=task_name, description=description, date=due_date, priority_level=level)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('view_tasks'))
    return render_template('add_task.html')

@app.route('/view/')
def view_tasks():
    tasks = Task.query.all()
    return render_template('view_tasks.html', tasks=tasks)

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.name = request.form['name']
        task.description = request.form['description']
        task.date = request.form['due_date']
        task.priority_level = request.form['level']
        db.session.commit()
        return redirect(url_for('view_tasks'))
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('view_tasks'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completion_status = 'completed'
    db.session.commit()
    return redirect(url_for('view_tasks'))

@app.route('/my_video/')
def my_video():
    return render_template('video.html')

@app.route('/info/')
def info():
    return render_template('info.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']  

@app.route('/add_note/', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        note_type = request.form['type']
        if note_type == 'text':
            text = request.form['text']
            new_note = Note(note_type='text', content=text)
        else:
            file = request.files['file']
            if 'file' not in request.files:
               flash('No file part')
               return redirect('add_note.html')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_folder, filename)
                try:
                    print(f"Saving file to {upload_folder}")
                    with open(file_path, 'wb') as f:
                        f.write(file.read())
                except Exception as e:
                    print(f"Error saving file: {e}")
                    return str(e)
                new_note = Note(note_type=note_type, content=filename)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('view_notes'))
    return render_template('add_note.html')

@app.route('/view_note/')
def view_notes():
    notes = Note.query.all()
    return render_template('view_notes.html', notes=notes)
@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('view_notes'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

