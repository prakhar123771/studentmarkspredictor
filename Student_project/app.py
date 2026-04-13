from flask import Flask, render_template, request
import pickle
import numpy as np

# create app
app = Flask(__name__)

# load model
model = pickle.load(open('model.pkl', 'rb'))

# home page
@app.route('/')
def home():
    return render_template('index.html')

# predict page
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        study_hours = float(request.form['study_hours'])
        attendance = float(request.form['attendance'])
        sleep_hours = float(request.form['sleep_hours'])
        screen_time = float(request.form['screen_time'])
        subject_difficulty = float(request.form['subject_difficulty'])

        input_data = [[study_hours, attendance, sleep_hours, screen_time, subject_difficulty]]
        prediction = model.predict(input_data)[0]

        return render_template('predict.html', result=round(prediction, 2))

    return render_template('predict.html')

# about page
@app.route('/about')
def about():
    return render_template('about.html')

# contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# run app
if __name__ == '__main__':
    app.run(debug=True)