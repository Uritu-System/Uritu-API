import shutil
from flask import Flask, jsonify, request
import base64
import os
import subprocess
from subprocess import call
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
    wavScpRoute = "/home/jose/Documents/TP2/Qformer/ConformerSpeechASR/egs/aishell/DATA/data/dev/wav.scp"
    wavScpRouteTest = "/home/jose/Documents/TP2/Qformer/ConformerSpeechASR/egs/aishell/DATA/data/test/wav.scp"

    #Writing wav.scp from dev
    write_file = open(wavScpRoute,'w')
    audioPath = "/home/jose/Documents/TP2/Uritu-API/static/audio_files/audio.wav"
    newWav = "audio.wav " + audioPath
    write_file.write(newWav + "\n")
    write_file.close()
    #Writing wav.scp from test
    write_fileTest = open(wavScpRouteTest,'w')
    write_fileTest.write(newWav + "\n")
    write_fileTest.close()
    stage = '--stage 5'
    expPath = "/home/jose/Documents/TP2/Qformer/ConformerSpeechASR/egs/aishell/paraformer/exp/baseline_train_asr_paraformer_conformer_12e_6d_2048_256_zh_word_exp1/decode_asr_transformer_noctc_1best"
    shutil.rmtree(expPath)
    try:
        subprocess.check_call(['./run.sh %s' % stage], shell=True, cwd="/home/jose/Documents/TP2/Qformer/ConformerSpeechASR/egs/aishell/paraformer/")
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    # To Do: add get audio xd
    predictionFile = "/home/jose/Documents/TP2/Qformer/ConformerSpeechASR/egs/aishell/paraformer/exp/baseline_train_asr_paraformer_conformer_12e_6d_2048_256_zh_word_exp1/decode_asr_transformer_noctc_1best/valid.acc.ave_10best.pb/dev/text"
    read_file = open(predictionFile,'r')
    lines = read_file.readlines()
    for line in lines:
        texto = line[10:]
        texto = texto.rstrip()
        predictions[0] = {'transcription': texto}
    read_file.close()
    print(predictions)
    return jsonify(predictions)

def getTranscripction(text):
    transcription = text
    return transcription

if __name__ == '__main__':
    app.run(debug=True, port=4000)
