from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

openai.api_key = ""

@app.route('/')
def index():
    return render_template('index.html')

app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio_file' not in request.files:
        return render_template('index.html', error='No audio file selected.')

    audio_file = request.files['audio_file']

    if audio_file.filename == '':
        return render_template('index.html', error='Audio file is empty.')

        audio_path = f'tmp/{audio_file.filename}'
        audio_file.save(audio_path)

        try:
            transcription = transcribe_audio(audio_path)
            return render_template('index.html', transcription = transcription)

        except Exception as e:
            return render_template('index.html', error = str(e))

def transcribe_audio(audio_path):
    file = open(audio_path, "rb")

    response = openai.Audio.transcribe("whisper-1", file)

    transcription = response["text"]

    return transcription

if __name__ == '__main__':
    os.makedirs('tmp', exist_ok=True)

    app.run(debug=True)