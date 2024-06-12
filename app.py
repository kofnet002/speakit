from flask import Flask, request, jsonify
from gtts import gTTS
import playsound
import os
import uuid

app = Flask(__name__)

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = f"{uuid.uuid4()}.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


@app.route('/speakit', methods=['POST'])
def tts():
    data = request.get_json() or request.args.get('text')

    text = data.get('text')

    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    speak(text)
    return jsonify({"message": "Text has been spoken"}), 200

if __name__ == '__main__':
    app.run()
