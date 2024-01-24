from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Upload page
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        flash('File uploaded successfully')

        return redirect(url_for('index'))

    flash('Invalid file format. Allowed formats are png, jpg, jpeg, gif')
    return redirect(request.url)

# Print and schedule page
@app.route('/print_schedule', methods=['GET', 'POST'])
def print_schedule():
    if request.method == 'POST':
        # Handle scheduling logic here
        date_str = request.form.get('print_date')
        time_str = request.form.get('print_time')

        print_datetime = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')

        # Implement scheduling mechanism (e.g., using Celery)
        flash(f'Scheduled printing for {print_datetime}')

    return render_template('print_schedule.html')

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True)
