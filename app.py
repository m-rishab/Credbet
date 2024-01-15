from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('models/model.pkl', 'rb'))

def extract_numeric_part(term_str):
    return ''.join(filter(str.isdigit, term_str))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/individual', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])

        # gender
        if gender == "Male":
            male = 1
        else:
            male = 0
        
        # married
        if married == "Yes":
            married_yes = 1
        else:
            married_yes = 0

        # dependents
        if dependents == '1':
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif dependents == '2':
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif dependents == "3+":
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0  

        # education
        if education == "Not Graduate":
            not_graduate = 1
        else:
            not_graduate = 0

        # employed
        if employed == "Yes":
            employed_yes = 1
        else:
            employed_yes = 0

        # property area
        if area == "Semiurban":
            semiurban = 1
            urban = 0
        elif area == "Urban":
            semiurban = 0
            urban = 1
        else:
            semiurban = 0
            urban = 0

        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome + CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)

        # Extract numerical part from 'Loan_Amount_Term'
        loan_term_str = request.form['Loan_Amount_Term']
        loan_term_numeric = extract_numeric_part(loan_term_str)

        # Convert to float
        Loan_Amount_Term = float(loan_term_numeric)

        prediction = model.predict([[credit, ApplicantIncomelog, LoanAmountlog, Loan_Amount_Term, totalincomelog, male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes, semiurban, urban]])

        if prediction == "N":
            prediction = "No"
        else:
            prediction = "Yes"

        return render_template("individual.html", prediction_text="Loan status is {}".format(prediction))
    else:
        return render_template("individual.html")

if __name__ == "__main__":
    app.run(debug=True)
