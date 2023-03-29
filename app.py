from flask import Flask, render_template, url_for,request,redirect
from datetime import datetime
import openai
import os

# Load OpenAI API key from environment variable or file
if "OPENAI_API_KEY" in os.environ:
    api_key = os.environ["OPENAI_API_KEY"]
else:
    with open("openai_api_key.txt") as f:
        api_key = f.read().strip()

# Set OpenAI API key
openai.api_key = api_key
app = Flask(__name__)


def ai(event,suggestion,relationship,gender):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"My {relationship} is celebrating {gender}{event} and i am confused on the gift i will give her please help me and suggest a gift for {gender}. This is the description of the person: {suggestion}",
            max_tokens=2000
        )
        return response["choices"][0]["text"]
    except openai.error.APIConnectionError:
        return "connection error try again"


def img(description):
    response = openai.Image.create(
    prompt=f"Draw a gift image with the desciption: {description} and please, use a real image.",
    n=1,
    size="256x256",
    )
    return response["data"][0]["url"]

@app.route('/',methods=['GET', 'POST'])
def index():
    date = datetime.utcnow().year
    if request.method == 'POST':
        event = request.form['event']
        suggestion = request.form['suggest']
        gender = request.form['gender']
        relationship = request.form['relationship']
        new_task = ai(event=event, suggestion=suggestion, gender=gender, relationship=relationship)
        image = img(new_task)
        return render_template('index.html', task=new_task, image=image, date=date)
    else:
        new_task = ''
        return render_template("index.html", task=new_task, date=date)

if __name__ == "__main__":
    app.run(debug=True)