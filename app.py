from flask import Flask, request, jsonify, send_file, after_this_request
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = f"{uuid.uuid4()}.mp3"
    file_path = os.path.join('audio_files', filename)
    tts.save(file_path)
    return filename

@app.route('/speakit', methods=['POST'])
def tts():
    data = request.get_json() or request.args
    text = data.get('text')

    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    filename = speak(text)
    file_url = request.host_url + 'audio_files/' + filename
    return jsonify({"message": "Text has been spoken", "file_url": file_url}), 200

@app.route('/audio_files/<filename>', methods=['GET'])
def get_audio_file(filename):
    file_path = os.path.join('audio_files', filename)
    return send_file(file_path, mimetype='audio/mpeg')

if __name__ == '__main__':
    if not os.path.exists('audio_files'):
        os.makedirs('audio_files')
    app.run(debug=True)
