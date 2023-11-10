from flask import Flask, jsonify

from predictions import predictions

app = Flask(__name__)


@app.route('/predictions')
def getPredictions():
    # crear un decoder base64 o linear16
    # TO DO if que compruebe si existe el audio.wap y que no sea nulo
    # then actualizaar con el archivo enviado
    # Else cree con el archivo enviado
    # Enviar el script
    # Devolver el string mediante jsonify
    return jsonify(predictions)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
