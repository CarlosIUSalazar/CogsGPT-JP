from flask import Flask, render_template, request
import requests
import openai
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Set up OpenAI API credentials
load_dotenv()
#openai_organization = os.getenv('OPENAI_ORGANIZATION') This one is not necessary for this App
openai_api_key = os.getenv('OPENAI_API_KEY')
model_id = 'gpt-3.5-turbo'

# Define the Flask route that displays the form
@app.route('/')
def index():
    return render_template('form.html')

# Define the Flask route that handles the form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    print("form submitted")
    # Get the form data from the request
    patient_height = request.form.get('height', '')
    weight = request.form.get('weight', '')
    age = request.form.get('age', '')
    hippocampus = request.form.get('hippocampus', '')
    gender = request.form.get('gender', '')
    walk = request.form.get('walk', '')
    exercise = request.form.get('exercise', '')
    fruits_veggies = request.form.get('fruits_veggies', '')
    fish = request.form.get('fish', '')
    sleep = request.form.get('sleep', '')
    sleep_reason = request.form.getlist('sleep_reason[]')
    hypertension = request.form.get('hypertension', '')
    diabetes = request.form.get('diabetes', '')
    smoking = request.form.get('smoking', '')
    alcohol = request.form.get('alcohol', '')
    nervous = request.form.get('nervous', '')
    hopeless = request.form.get('hopeless', '')
    restless = request.form.get('restless', '')
    depressed = request.form.get('depressed', '')
    foolish = request.form.get('foolish', '')
    worthless = request.form.get('worthless', '')


    # Construct the mytext variable based on the form data
    mytext = f"Prepare some lifestyle advice for the prevention of dementia IN JAPANESE, for a person with the following characteristics: {patient_height}cm tall weights {weight}kg and is a {age}-year-old {gender}. This person hippocampus volume is {hippocampus} cubic mm. This person took the following lifestyle and medical history questionnaire and next to each question is the answer obtained. Your essay please separate it into はじめに, 運動, 睡眠, 食事, コミュニケーション, アルコール, 趣味, メンタルヘルス and 結論 sections. Give your answer fully in formal Japanese language"
    mytext += f"\nPhysical Activity:\nQ: How much do you walk everyday? A:{walk}."
    mytext += f"\nQ: In a week how many times you exercise more than 30 minutes? A:{exercise}."
    mytext += f"\nDiet:\nQ: Everyday how many portions of fruits and vegetables do you eat? A:{fruits_veggies}."
    mytext += f"\nQ: In a week, how much fish do you eat? A:{fish}."
    mytext += f"\nSleep:\nQ: In the past months, how would you qualify your own sleep? A:{sleep}."
    if sleep_reason:
        mytext += "\nQ: Which of the following reasons apply to your sleep? Select all that apply."
        for reason in sleep_reason:
            mytext += f"\n- {reason}"
    mytext += f"\nMedical History:\nQ: Have you ever been told you have hypertension? Or are you on treatment for hypertension? {hypertension}."
    mytext += f"\nQ: Have you ever been told you have diabetes? Or are you on treatment for diabetes? A:{diabetes}."
    mytext += f"\nQ: Do you smoke? A:{smoking}."
    mytext += f"\nQ: How much alcohol do you drink per day? A:{alcohol}."
    mytext += f"\nMental Health:\nQ: In the past month, did you feel nervous? A:{nervous}."
    mytext += f"\nQ: In the past month, did you feel hopeless? A:{hopeless}."
    mytext += f"\nQ: In the past month, did you feel Did you feel fidgety or restless? A:{restless}."
    mytext += f"\nQ: In the past month, did you feel depressed and like nothing could make you feel better? A:{depressed}."
    mytext += f"\nQ: In the past month, did you feel that anything you did was foolish? A:{foolish}."
    mytext += f"\nQ: In the past month, did you feel worthless? A:{worthless}."

    print("mytext", mytext)

    testtext = "why my cat is so cute, answer within 20 words"

    # Call the OpenAI API
    URL = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": mytext}],
        "temperature" : 1.0,
        "top_p":0.7,
        "n" : 1,
        "stream": False,
        "presence_penalty":0,
        "frequency_penalty":0,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    response = requests.post(URL, headers=headers, json=payload, stream=False)
    print("responseeeee", response)
    
    # Process the API response and return the result
    if response.ok:
        response_data = response.json()
        print("response_dataaaaaa", response_data)
        generated_text = response_data["choices"][0]["message"]["content"].strip()
        print("generated_textttt",generated_text)
        
        # Render the result template
        return render_template('results.html', generated_text=generated_text)
    else:
        return "Error calling OpenAI API"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)