from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

# Load model and vectorizer
vector = pickle.load(open("vectorizer.pkl", "rb"))
model = pickle.load(open("phishing.pkl", "rb"))


@app.route('/', methods=['GET', 'POST'])
def index():

    prediction = ""
    url = ""

    if request.method == 'POST':

        # Get URL from form
        url = request.form.get('Url')

        # Empty input check
        if not url or url.strip() == "":
            prediction = "⚠️ Please enter a valid URL."
            return render_template(
                'index.html',
                prediction=prediction,
                url=url
            )

        try:

            # Clean URL
            cleaned_url = re.sub(
                r'https?://(www\.)?',
                '',
                url
            )

            # Convert URL into vector
            transformed_url = vector.transform([cleaned_url])

            # Model prediction
            predict = model.predict(transformed_url)[0]

            print("Prediction:", predict)
            print("Prediction Type:", type(predict))

            # --------------------------
            # Handle Different Outputs
            # --------------------------

            # If model returns string labels
            if str(predict).lower() == "bad":
                prediction = "⚠️ This is a Phishing Website"

            elif str(predict).lower() == "good":
                prediction = "✅ This is a Safe Website"

            # If model returns numbers
            elif predict == 0:
                prediction = "⚠️ This is a Phishing Website"

            elif predict == 1:
                prediction = "✅ This is a Safe Website"

            else:
                prediction = f"Unknown Prediction Result: {predict}"

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template(
        'index.html',
        prediction=prediction,
        url=url
    )


if __name__ == '__main__':
    app.run(debug=True)