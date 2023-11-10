from flask import Flask, jsonify, request
import base64
import os

from predictions import predictions

app = Flask(__name__)


@app.route('/predictions')
def getPredictions():
    # Access the request's json
    json_data = request.json
    # Check if 'audio' field is present
    if 'audio' not in json_data:
        return jsonify({"error": "Missing 'audio' field"}), 400
    # Get the audio data
    audio_data = json_data['audio']
    # Decode base64
    decoded_audio = base64.b64decode(audio_data)
    # save audio
    save_path = 'static/audio_files'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = os.path.join(save_path, 'audio.wav')
    with open(file_path, 'wb') as f:
        f.write(decoded_audio)
    # To Do: add get audio xd
    return jsonify(predictions)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
