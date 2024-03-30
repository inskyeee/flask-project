from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
import sqlite3

# Initializing the Flask application
app = Flask(__name__)
# Setting a secret key for session management and form protection (CSRF). Unfortunately, without it the form will not work.
app.config['SECRET_KEY'] = "1234"

# Creating raw db
def init_db():
    conn = sqlite3.connect('Flask-project/data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            student_number TEXT,
            email TEXT,
            grades TEXT,
            satisfaction TEXT,
            improvements TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Defining the form using Flask-WTF, which will be used in the data-collection route
class QuestionnaireForm(FlaskForm):
    # These are form fields with label and some of them have DataRequired validator to ensure the field is not submitted empty
    name = StringField('Name', validators=[DataRequired()])
    student_number = StringField('Student Number', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    grades = TextAreaField('Grades Obtained', validators=[DataRequired()])
    satisfaction = SelectField('Overall Satisfaction', choices=[('', 'Click to select'), ('very_satisfied', 'Very Satisfied'), ('satisfied', 'Satisfied'), ('neutral', 'Neutral'), ('dissatisfied', 'Dissatisfied'), ('very_dissatisfied', 'Very Dissatisfied')], default='')
    improvements = TextAreaField('Suggestions for Improvement')
    # Submit button for the form
    submit = SubmitField('Submit')

# Home page route
@app.route('/')
@app.route('/welcome')
def home():
    return render_template('welcome.html')

# Information route
@app.route('/information')
def information():
    return render_template('information.html')

# Data collection route with form, allowing both GET and POST request
@app.route('/data-collection', methods=['GET', 'POST'])
def data_collection():
    form = QuestionnaireForm() # Creating an instance of the form
    if form.validate_on_submit(): # If the form is submitted and validated
        # Saving data to db
        conn = sqlite3.connect('Flask-project/data.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO responses (name, student_number, email, grades, satisfaction, improvements)
            VALUES (?, ?, ?, ?, ?, ?)
                ''', (form.name.data, form.student_number.data, form.email.data, form.grades.data, form.satisfaction.data, form.improvements.data))
        conn.commit()
        conn.close()
        return redirect('/thankyou')
    # If the form is not submitted or not validated, render the form
    return render_template('data-collection.html', form=form)

# Thank you route
@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

# Running the application
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
