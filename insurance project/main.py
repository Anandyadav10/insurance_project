from flask import Flask, render_template, request
import joblib
import numpy as np

# ==========================
# LOAD TRAINED MODEL
# ==========================
# Replace with your trained insurance model file
model = joblib.load('insurance_joblib')

app = Flask(__name__)

# ==========================
# ROUTES
# ==========================

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/project')
def project():
    return render_template("project.html")


# ==========================
# DICTIONARIES (ENCODING)
# ==========================

gender_dict = {'male': 0, 'female': 1}
smoker_dict = {'yes': 1, 'no': 0}
region_dict = {'northeast': 0, 'northwest': 1, 'southeast': 2, 'southwest': 3}


# ==========================
# PREDICTION ROUTE
# ==========================

@app.route('/predict', methods=['GET', 'POST'])
def predict():

    if request.method == 'POST':

        # ===== GET FORM DATA =====
        age = int(request.form['age'])
        gender = request.form['gender']
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = request.form['smoker']
        region = request.form['region']

        print("Insurance data received ✅")

        # ===== ENCODING =====
        gender = gender_dict[gender]
        smoker = smoker_dict[smoker]
        region = region_dict[region]

        # ===== FEATURE ORDER (MUST MATCH TRAINING) =====
        features = [[
            age,
            gender,
            bmi,
            children,
            smoker,
            region
        ]]

        # ===== PREDICTION =====
        prediction = model.predict(features)[0]

        result = f"Estimated Insurance Charges: ₹ {round(prediction,2)}"

        return render_template('project.html', prediction=result)

    return render_template('project.html')


# ==========================
# RUN APP
# ==========================

if __name__ == '__main__':
    app.run(debug=True)