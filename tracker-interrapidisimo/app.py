from flask import Flask, request, jsonify
import ssl

print(ssl.OPENSSL_VERSION)

import interservice

app = Flask(__name__)

@app.route('/rastrear', methods=['POST'])
def rastrear():
    print('Rastrear')
    # print(
    #     interservice.limpiar_cadena_personalizada("_2BY9HZx3rBZstOr_2BSlpkRTEqyp_2BI_2F6QHHC5qQ_2FRWbzEPoNw_2FsVfXXUNLoWN7FPb6EZZhDl6WumK3MALRbuW5fIA_3D_3D"))
    data = request.json
    numero_de_guia = data.get('numero_de_guia')
    if not numero_de_guia:
        return jsonify({"error": "El número de guía es requerido"}), 400
    resultado = interservice.rastrear_guia(numero_de_guia)
    return jsonify(resultado)

@app.route('/novedades', methods=['POST'])
def rastrear_novedades():
    print('Novedades')
    # Obtiene el número de guía desde los parámetros del cuerpo de la solicitud
    data = request.get_json()
    numero_guia = data.get('numero_guia')

    print('numero de guia a rastrear' + numero_guia)
    if not numero_guia:
        return jsonify({'error': 'El número de guía es requerido'}), 400

    # Llama a la función obtener_novedades para obtener la información
    resultado = interservice.obtener_novedades(numero_guia)

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
