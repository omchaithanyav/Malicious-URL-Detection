from flask import Flask, request, render_template
import validators
import numpy as np
import pickle
from keras.preprocessing.sequence import pad_sequences
import playsound
import os
from gtts import gTTS

num = 1

def voice(text):
    global num

    num += 1
    toSpeak = gTTS(text=text, lang='en', slow=False)

    file = str(num) + ".mp3"
    toSpeak.save(file)

    playsound.playsound(file, True)
    os.remove(file)


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/prediction', methods=['POST'])
def prediction():

    url = str(request.form['url'])

    model = pickle.load(open('models/gbc.pkl', 'rb'))
    Tokenizer = pickle.load(open('models/tokenizer.pkl', 'rb'))

    valid = validators.url(url)
    if(valid==True):
        tokens = Tokenizer.texts_to_sequences([url])
        tokens = pad_sequences(tokens, maxlen=100)
        pred = model.predict(np.array(tokens))
        classes = ['Safe url', 'Malicious url']
        result = classes[pred[0]]
        voice(result)
        return render_template('result.html', output="{} - is {}".format(url, result))
    else:
        voice("Entered url is Invalid")
        return render_template('result.html', output=("Entered url is Invalid"))


if __name__ == '__main__':

    app.run(debug=True, port = int(os.environ.get('PORT',5000)))