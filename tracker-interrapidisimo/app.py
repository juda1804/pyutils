# app.py

from flask import Flask, request, jsonify

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import time

app = Flask(__name__)

def limpiar_cadena_personalizada(cadena):
    reemplazos = {
        '_2B': '+',
        '_2F': '/',
        '_3D': '='
    }
    for key, value in reemplazos.items():
        cadena = cadena.replace(key, value)
    return cadena

def rastrear_guia(numero_de_guia):
    # Configurar opciones para ejecutar Firefox en modo headless
    options = Options()
    options.headless = False  # Cambia a True para ejecutar en modo headless
    # options.add_argument("--headless")  # Activa el modo headless de manera explícita
    # options.add_argument("--disable-gpu")  # Deshabilita la GPU (opcional, por si acaso)
    # options.add_argument("--no-sandbox")  # Agrega esta opción si estás ejecutando en un entorno sin UI

    service = FirefoxService(executable_path='/usr/bin/geckodriver')  # Asegúrate de que esta sea la ruta correcta

    # Inicia el webdriver de Firefox
    driver = webdriver.Firefox(service=service, options=options)

    try:
        # URL del sitio web
        encrypted_track_id = "_2BY9HZx3rBZstOr_2BSlpkRTEqyp_2BI_2F6QHHC5qQ_2FRWbzEPoNw_2FsVfXXUNLoWN7FPb6EZZhDl6WumK3MALRbuW5fIA_3D_3D"
        url = 'https://www3.interrapidisimo.com:8082/SiguetuEnvio/shipment/'+encrypted_track_id
        driver.get(url)

        # Espera dinámicamente a que el campo del número de guía sea visible
        input_guide = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'inputGuide'))
        )

        # Limpia el campo antes de ingresar el número de la guía
        input_guide.clear()
        input_guide.send_keys(numero_de_guia)

        # # Encuentra el elemento <a> dentro del div con la clase 'search-button'
        # elemento = driver.find_element(By.CSS_SELECTOR, '.search-button')

        # Encuentra el elemento <a> dentro del div con la clase 'search-button'
        print("se va a buscar", flush=True)
        elemento = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.right-button'))
        )

        elemento.click()

        print("se va a buscar 2", flush=True)

        # print("El elemento fue encontrado y es visible.", flush=True)
        # # Obtén las coordenadas del elemento
        # location = elemento.location
        #
        # print("El elemento" + str(location), flush=True)
        #
        # x = location['x']
        # y = location['y']
        #
        # # Imprime las coordenadas con conversión a cadena
        # print("x: " + str(x), flush=True)
        # print("y: " + str(y), flush=True)
        #
        # # Imprime ambas coordenadas juntas
        # print("x: " + str(x) + " y: " + str(y), flush=True)
        # # Mueve el mouse a las coordenadas y haz clic
        # ActionChains(driver).move_by_offset(x, y).click().perform()
        time.sleep(1)

        # Captura la URL actual
        current_url = driver.current_url
        print("current_url" + current_url, flush=True)
        # Extrae el último path parameter de la URL
        guia_encrypted = current_url.split('/')[-1]

        print("encripted:" + guia_encrypted)
        resultado = limpiar_cadena_personalizada(guia_encrypted)
        # Muestra el último path parameter
        return {"guia_encrypted": resultado}

    except NoSuchElementException:
        print("El elemento no fue encontrado en la página.", flush=True)
    except TimeoutException:
        print("El elemento no fue encontrado o no es visible dentro del tiempo esperado.", flush=True)
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Cierra el navegador
        driver.quit()

@app.route('/rastrear', methods=['POST'])
def rastrear():
    data = request.json
    numero_de_guia = data.get('numero_de_guia')
    if not numero_de_guia:
        return jsonify({"error": "El número de guía es requerido"}), 400

    resultado = rastrear_guia(numero_de_guia)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
