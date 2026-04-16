from flask import Flask, render_template, request, jsonify
import pickle

# create app
app = Flask(__name__)

# load model
model = pickle.load(open('model.pkl', 'rb'))

# home page
@app.route('/')
def home():
    return render_template('index.html')


# predict page (frontend)
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # get input values
            study_hours = float(request.form['study_hours'])
            attendance = float(request.form['attendance'])
            sleep_hours = float(request.form['sleep_hours'])
            screen_time = float(request.form['screen_time'])
            subject_difficulty = float(request.form['subject_difficulty'])

            # 🔒 Input Validation
            if study_hours < 0 or sleep_hours < 0 or screen_time < 0:
                return render_template('predict.html', result="Invalid input! Values cannot be negative.")

            if attendance < 0 or attendance > 100:
                return render_template('predict.html', result="Attendance must be between 0 and 100.")

            if subject_difficulty < 1 or subject_difficulty > 10:
                return render_template('predict.html', result="Subject difficulty must be between 1 and 10.")

            # prediction
            input_data = [[study_hours, attendance, sleep_hours, screen_time, subject_difficulty]]
            prediction = model.predict(input_data)[0]

            # ✅ limit marks between 0–100
            prediction = max(0, min(100, prediction))

            # 🔥 Early Warning System Logic
            if prediction < 50:
                warning = "⚠️ High Risk: Poor academic performance expected!"
                suggestion = "Increase study hours, reduce screen time, improve attendance, follow strict schedule."
            elif prediction < 75:
                warning = "⚠️ Moderate Risk: You need improvement."
                suggestion = "Revise daily, focus on weak subjects, maintain consistency."
            else:
                warning = "✅ Low Risk: Good performance expected."
                suggestion = "Keep up the good work and focus on advanced topics."

            return render_template(
                'predict.html',
                result=round(prediction, 2),
                warning=warning,
                suggestion=suggestion
            )

        except Exception as e:
            return render_template('predict.html', result="Error: Invalid input format")

    return render_template('predict.html')


# ✅ API Endpoint (IMPORTANT for guidelines)
@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json()

        study_hours = float(data['study_hours'])
        attendance = float(data['attendance'])
        sleep_hours = float(data['sleep_hours'])
        screen_time = float(data['screen_time'])
        subject_difficulty = float(data['subject_difficulty'])

        # validation
        if study_hours < 0 or sleep_hours < 0 or screen_time < 0:
            return jsonify({"error": "Invalid input values"}), 400

        if attendance < 0 or attendance > 100:
            return jsonify({"error": "Attendance must be between 0 and 100"}), 400

        if subject_difficulty < 1 or subject_difficulty > 10:
            return jsonify({"error": "Subject difficulty must be between 1 and 10"}), 400

        input_data = [[study_hours, attendance, sleep_hours, screen_time, subject_difficulty]]
        prediction = model.predict(input_data)[0]

        # limit
        prediction = max(0, min(100, prediction))

        return jsonify({
            "predicted_marks": round(prediction, 2)
        })

    except Exception as e:
        return jsonify({"error": "Invalid input format"}), 400


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
