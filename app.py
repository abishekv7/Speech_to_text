import json
import os

import requests
import speech_recognition as sr
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='template')
context_set = ""


# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'GET':
#         val = str(request.args.get('text'))
#         data = json.dumps({"sender": "Rasa", "message": val})
#         headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#         res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data, headers=headers)
#         res = res.json()
#         val = res[0]['text']
#     return render_template('index.html', val=val)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        f = request.files['audio_data']
        f.save('audio.wav')
        print('file uploaded successfully')
        re = sr.Recognizer()
        command = f"ffmpeg -i audio.wav audio1.wav"
        os.system(command)
        with sr.AudioFile('audio1.wav') as source:
            audio_listened = re.record(source)
            # try converting it to text
            try:
                text = re.recognize_google(audio_listened)
                print(text)
                data = json.dumps({"sender": "Rasa", "message": text})
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data, headers=headers)
                res = res.json()
                val = res[0]['text']
            except sr.UnknownValueError as e:
                print("Error:", str(e))
        # return the text for all chunks detected
        os.remove('audio.wav')
        os.remove('audio1.wav')
        result = {'botText': val, 'meText': text}
        print(val)
        response = app.response_class(response=json.dumps(result),
                                      status=200,
                                      mimetype='application/json')
        return response
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
